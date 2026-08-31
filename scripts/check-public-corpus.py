#!/usr/bin/env python3
"""Fail closed on public-corpus, notation, and source-archive invariants."""

from __future__ import annotations

import argparse
import html
import hashlib
import json
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
import unicodedata
from collections.abc import Iterator
from pathlib import Path, PurePosixPath
from typing import NoReturn, Sequence

ROOT = Path(__file__).resolve().parents[1]
PRINCIPAL = Path("paper/kourovka-18-68.tex")
RENDERED = Path("paper/kourovka-18-68.pdf")
ARCHIVE_MANIFEST = Path("SOURCE-MANIFEST.txt")
MAX_ARCHIVE_FILE = 64 * 1024 * 1024
MAX_ARCHIVE_TOTAL = 256 * 1024 * 1024


def fail(message: str) -> NoReturn:
    raise RuntimeError(f"public corpus check failed: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def safe_path(name: str) -> Path:
    require("\\" not in name, f"non-POSIX path spelling: {name}")
    pure = PurePosixPath(name)
    require(not pure.is_absolute(), f"absolute path: {name}")
    require(pure.parts and all(part not in {"", ".", ".."} for part in pure.parts),
            f"unsafe path: {name}")
    return Path(*pure.parts)


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-s", "-z"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "git could not enumerate tracked files")
    entries = result.stdout.split(b"\0")
    require(entries and entries[-1] == b"", "malformed Git path stream")
    paths: list[Path] = []
    for raw in entries[:-1]:
        try:
            prefix, encoded = raw.split(b"\t", 1)
            mode, _object_id, stage = prefix.decode("ascii").split()
            name = encoded.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as error:
            fail(f"malformed Git entry: {error}")
        path = safe_path(name)
        require(stage == "0", f"unmerged Git entry: {path}")
        require(mode in {"100644", "100755"},
                f"tracked entry is not a regular file: {path} ({mode})")
        paths.append(path)
    require(PRINCIPAL in paths, f"principal manuscript {PRINCIPAL} is not tracked")
    require(len(paths) == len(set(paths)), "duplicate tracked paths")
    return sorted(paths, key=lambda item: item.as_posix())


def load_paths_file(path: Path) -> list[Path]:
    source = path if path.is_absolute() else ROOT / path
    require(not source.is_symlink(), f"path allowlist is a symbolic link: {path}")
    require(source.is_file(), f"missing path allowlist: {path}")
    paths: list[Path] = []
    seen: set[Path] = set()
    for number, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        item = safe_path(line)
        require(item not in seen, f"duplicate allowlist path at line {number}: {item}")
        seen.add(item)
        paths.append(item)
    require(paths == sorted(paths, key=lambda item: item.as_posix()),
            "path allowlist must be sorted")
    require(PRINCIPAL in paths, f"principal manuscript {PRINCIPAL} is not allowlisted")
    return paths


def require_regular(root: Path, path: Path) -> Path:
    full = root / path
    require(not full.is_symlink(), f"symbolic link is not allowed: {path}")
    try:
        mode = full.stat().st_mode
    except OSError as error:
        fail(f"could not inspect listed file {path}: {error}")
    require(stat.S_ISREG(mode), f"listed entry is not a regular file: {path}")
    return full


def read_text(root: Path, path: Path) -> str:
    data = require_regular(root, path).read_bytes()
    require(b"\0" not in data, f"unexpected binary file: {path}")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        fail(f"text is not UTF-8 ({path}): {error}")


def extract_pdf(root: Path, path: Path) -> str:
    full = require_regular(root, path)
    executable = shutil.which("pdftotext")
    require(executable is not None, "pdftotext is required to scan PDFs")
    result = subprocess.run(
        [executable, "-layout", str(full), "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, f"could not extract PDF {path}")
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError as error:
        fail(f"PDF text is not UTF-8 ({path}): {error}")


def process_patterns() -> list[re.Pattern[str]]:
    """Reject explicit process artifacts without banning ordinary role nouns."""

    fragments = [
        r"\bpeer[- ]" + r"revi" + r"ew(?:ed|ing)?\b",
        r"\bref" + r"eree(?:s|ing)?\b",
        r"\brevi" + r"ewer(?:s)?\b",
        r"\baud" + r"itor(?:s|ing)?\b",
        r"\binternal\s+(?:adversarial|agent|mathematical)\s+" + r"revi" + r"ew\b",
        r"\badversarial\s+" + r"revi" + r"ew\b",
        r"\brevi" + r"ew\s+rounds?\b",
        r"\bhard[- ]" + r"final\b",
        r"\bacceptance[- ]" + r"level\b",
        r"\brele" + r"ase\s+candidate\b",
        r"\bproof\s+" + r"candidate\b",
        r"\bclaimed\s+complete\s+solution\b",
        r"\b(?:pending|awaiting)\s+(?:eval" + r"uation|appro" + r"val|vali" + r"dation|revi" + r"ew)\b",
        r"\bsign[- ]" + r"off\b",
        r"\bhuman\s+(?:appro" + r"val|vali" + r"dation|veri" + r"fication)\b",
        r"\bneeds?\s+hum" + r"an\b",
        r"\b(?:appro" + r"val|vali" + r"dation)\s+(?:is\s+)?required\b",
        r"\bmust\s+be\s+(?:appro" + r"ved|vali" + r"dated|revi" + r"ewed)\b",
        r"\b(?:vali" + r"dation|veri" + r"fication|appro" + r"val|revi" +
        r"ew)\s+(?:is\s+)?assigned\s+to\b",
        r"\b(?:assigned|designated)\s+(?:rea" + r"der|special" + r"ist|ex" + r"pert|revi" +
        r"ewer|ref" + r"eree|aud" + r"itor|person)\b",
        r"\brole\s+matrix\b",
        r"\bpending[- ]eval" + r"uation\s+table\b",
        r"\breader\s+test\b",
        r"\bresponsible\s+for\s+(?:appro" + r"ving|vali" + r"dating|veri" +
        r"fying|revi" + r"ewing|rele" + r"asing|publi" + r"shing|submi" +
        r"tting)\b",
        r"\b(?:rele" + r"ase|publi" + r"cation|submi" + r"ssion|readi" +
        r"ness)\s+(?:lead|manager|owner|coordinator|chair)\b",
    ]
    return [re.compile(item, re.IGNORECASE | re.DOTALL) for item in fragments]


POLICY_TEX_COMMAND = re.compile(r"\\[A-Za-z]+\*?")
POLICY_WORD_BREAK = re.compile(r"[^0-9A-Za-z]+")


def normalize_policy_text(text: str) -> str:
    """Normalize markup, Unicode, hyphenation, and punctuation for prose checks."""

    normalized = unicodedata.normalize("NFKC", html.unescape(text))
    normalized = POLICY_TEX_COMMAND.sub(" ", normalized)
    normalized = normalized.replace("_", " ").replace("-", " ")
    normalized = POLICY_WORD_BREAK.sub(" ", normalized)
    return " ".join(normalized.casefold().split())


def policy_windows(text: str, path: Path) -> Iterator[str]:
    """Yield normalized sentence and adjacent-sentence windows.

    Source code is kept line-local so fragments used to define this policy do
    not synthesize prose.  Public prose receives both sentence-local and
    adjacent-sentence views so a line break cannot separate a dependency from
    its publication state.
    """

    if path.suffix.lower() in {".py", ".sh"} or path.name == "Makefile":
        for line in text.splitlines():
            window = normalize_policy_text(line)
            if window:
                yield window
        return

    chunks = [
        chunk.strip()
        for chunk in re.split(r"(?<=[.!?])(?:[\"')\]]*)\s+|\n[ \t]*\n|\n", text)
        if chunk.strip()
    ]
    normalized = [normalize_policy_text(chunk) for chunk in chunks]
    for index, window in enumerate(normalized):
        if window:
            yield window
        if index + 1 < len(normalized):
            pair = " ".join((window, normalized[index + 1])).strip()
            if pair:
                yield pair


PUBLICATION_SIGNAL = re.compile(
    r"\b(?:rele" + r"as(?:e|es|ed|ing)|publi" + r"(?:sh|shes|shing|cation)|"
    r"submi" + r"(?:t|ts|tted|ssion)|preprint|manuscript|readi" + r"ness|ready|"
    r"circulat(?:e|es|ed|ing|ion)|deposit|upload|public\s+update|comple" +
    r"tion)\b|\b(?:be|been|being|is|are|was|were|get|gets|got|may\s+be|"
    r"can\s+be|will\s+be)\s+published\b"
)
AUTHORIZATION_SIGNAL = re.compile(
    r"\b(?:consen" + r"t|authori" + r"z(?:e|es|ed|ing|ation)|assen" + r"t|"
    r"appro" + r"v(?:e|es|ed|ing|al)|permission|endorsement|clearance|"
    r"certif(?:y|ies|ied|ication)|sign\s+off|signs?|signed|concurrence|"
    r"green\s+light|go\s+ahead)\b"
)
CONDITION_SIGNAL = re.compile(
    r"\b(?:after|before|until|unless|once|when|only\s+if|only\s+after|"
    r"depends?\s+(?:on|upon)|requi" + r"r(?:e|es|ed|ing|ement)|awaits?|"
    r"subject\s+to|contingent\s+(?:on|upon)|conditional\s+(?:on|upon)|"
    r"pending|must|may\s+not|will\s+not|cannot|withheld|blocked|deferred)\b"
)
ACTOR_SIGNAL = re.compile(
    r"\b(?:person|individual|hum" + r"an|rea" + r"der|special" + r"ist|ex" +
    r"pert|revi" + r"ewer|ref" + r"eree|aud" + r"itor|mathematician|"
    r"lead|manager|owner|coordinator|chair|committee|panel|board|editor|"
    r"third\s+party|decision\s+maker)\b"
)
HUMAN_ACTION_SIGNAL = re.compile(
    r"\b(?:decid(?:e|es|ed|ing|decision)|determin(?:e|es|ed|ing|ation)|"
    r"check(?:s|ed|ing)?|inspect(?:s|ed|ing|ion)?|read(?:s|ing)?|"
    r"verif(?:y|ies|ied|ication)|vali" + r"dat(?:e|es|ed|ing|ion)|"
    r"confirm(?:s|ed|ing|ation)?|assess(?:es|ed|ing|ment)|"
    r"revi" + r"ew(?:s|ed|ing)?|vote(?:s|d|ing)?)\b"
)
DECISION_ACTION_SIGNAL = re.compile(
    r"\b(?:decid(?:e|es|ed|ing|decision)|determin(?:e|es|ed|ing|ation)|"
    r"vote(?:s|d|ing)?)\b"
)
ASSIGNMENT_SIGNAL = re.compile(
    r"\b(?:assi" + r"gn(?:s|ed|ing|ment)?|designat(?:e|es|ed|ing|ion)|"
    r"appoint(?:s|ed|ing|ment)?|nominat(?:e|es|ed|ing|ion)|"
    r"task(?:s|ed|ing)?|charg(?:e|es|ed|ing)|delegat(?:e|es|ed|ing|ion)|"
    r"entrust(?:s|ed|ing)?)\b"
)
PROCESS_TASK_SIGNAL = re.compile(
    r"\b(?:rele" + r"ase|publi" + r"cation|submi" +
    r"ssion|readi" + r"ness|check|veri" + r"fication|vali" + r"dation|"
    r"eval" + r"uation|revi" + r"ew|appro" + r"val|authori" + r"zation)\b"
)
RESPONSIBILITY_SIGNAL = re.compile(
    r"\b(?:responsible\s+for|in\s+charge\s+of|owns?\s+the\s+(?:decision|call)|"
    r"has\s+the\s+(?:final|last)\s+(?:say|word)|decision\s+belongs\s+to|"
    r"rests?\s+in\s+the\s+hands\s+of)\b"
)


def human_gate_sentence(text: str, path: Path) -> str | None:
    """Return a normalized structural public-status gate or task allocation."""

    for window in policy_windows(text, path):
        public_state = bool(PUBLICATION_SIGNAL.search(window))
        approval_action = bool(AUTHORIZATION_SIGNAL.search(window))
        condition = bool(CONDITION_SIGNAL.search(window))
        actor = bool(ACTOR_SIGNAL.search(window))
        action = bool(HUMAN_ACTION_SIGNAL.search(window))
        if ASSIGNMENT_SIGNAL.search(window) and PROCESS_TASK_SIGNAL.search(window):
            return window
        if public_state and approval_action:
            return window
        if public_state and RESPONSIBILITY_SIGNAL.search(window):
            return window
        if public_state and actor and DECISION_ACTION_SIGNAL.search(window):
            return window
        if public_state and actor and action and condition:
            return window
    return None


def disclosure_patterns() -> list[re.Pattern[str]]:
    terms = [
        r"\bgen" + r"erative\b",
        r"\bartificial\s+intel" + r"ligence\b",
        r"\blanguage\s+mod" + r"els?\b",
        r"\blarge\s+language\s+mod" + r"els?\b",
        r"\bL" + r"LMs?\b",
        r"\bChat" + r"GPT\b",
        r"\bCod" + r"ex\b",
        r"\bOpen" + r"A" + r"I\b",
        r"\bAnthro" + r"pic\b",
        r"\bCla" + r"ude\b",
        r"\bGem" + r"ini\b",
        r"\bCo" + r"pilot\b",
        r"\bGr" + r"ok\b",
        r"\bLl" + r"ama\b",
        r"\bMis" + r"tral\b",
        r"\bPerplex" + r"ity\b",
        r"\bDeep" + r"Seek\b",
        r"\bG" + r"PT[- ]?[0-9][0-9A-Za-z.]*\b",
        r"\bmachine[- ]generated\b",
        r"\bchat" + r"bots?\b",
        r"\b(?:neural|machine[- ]learning|foundation|trans" +
        r"former)[- ](?:te" + r"xt[- ])?"
        r"(?:models?|systems?|generators?|tools?)\b",
        r"\b(?:neural\s+)?te" + r"xt\s+generators?\b",
        r"\bmodel[- ]assisted\s+(?:drafting|writing|editing|research)\b",
        r"\balgorithmic\s+(?:drafting|writing|editing)\b",
        r"\bautomated\s+(?:drafting|writing|editing)\b",
        r"(?<![A-Za-z0-9])A" + r"I(?![A-Za-z0-9])",
    ]
    return [re.compile(item, re.IGNORECASE) for item in terms]


DISCLOSURE_FORM_A = re.compile(
    r"\b(?:writing|authoring|editorial|text|prose)\s+"
    r"(?:bo" + r"t|robot|assistant|agent|engine|generator|tool|system|service)\b|"
    r"\b(?:bo" + r"t|robot|assistant|agent|engine|generator|tool|system|service)\s+"
    r"(?:for\s+)?(?:writing|authoring|editing|drafting|text|prose)\b"
)
DISCLOSURE_FORM_B = re.compile(
    r"\bsynthe" +
    r"tic\s+(?:te" + r"xt|prose|content|writing|authoring|language)\b"
)
DISCLOSURE_FORM_C = re.compile(
    r"\b(?:automated|algorithmic|neural|predictive|transformer|foundation)\s+"
    r"(?:writing|authoring|editing|drafting|text|language|prose)\b"
)


def structural_disclosure(text: str, path: Path) -> str | None:
    for window in policy_windows(text, path):
        if (
            DISCLOSURE_FORM_A.search(window)
            or DISCLOSURE_FORM_B.search(window)
            or DISCLOSURE_FORM_C.search(window)
        ):
            return window
    return None


TEX_GROUP_COMMAND_RE = re.compile(
    r"\\(?:Gamma|Delta|Sigma|Omega|Lambda|Phi|Psi|Theta|Pi|operatorname|"
    r"mathrm|mathbf|mathbb|mathcal|mathfrak|mathscr|mathsf|Aut|Inn|Out|"
    r"Syl|Soc|Core|Norm|Cent|Normalizer|Centralizer|GL|SL|PSL|PGL|Sp|PSp|"
    r"PSU|GU|SU)(?![A-Za-z])"
)
BARE_GROUP_SYMBOL_RE = re.compile(r"(?<![A-Za-z\\])[A-Z](?![a-z])")
PLAIN_GROUP_NAME_RE = re.compile(
    r"\b(?:Aut|Inn|Out|Soc|Core|Norm|Cent|Normalizer|Centralizer|Sym|Alt|"
    r"Syl|GL|SL|PSL|PGL|Sp|PSp|PSU|GU|SU)\b"
)
TEX_SIZE_COMMAND_RE = re.compile(
    r"\\(?:left|right|bigl|bigr|Bigl|Bigr|biggl|biggr|Biggl|Biggr|big|Big)\b"
)
TEX_COLON_COMMAND_RE = re.compile(
    r"\\+(?:colon|mathcolon|ratio|textcolon)\b", re.IGNORECASE
)
TEX_MATH_CLASS_COLON_RE = re.compile(
    r"\\+(?:mathord|mathop|mathbin|mathrel|mathopen|mathclose|mathpunct|"
    r"mathinner)\s*\{\s*(?:\\+(?:colon|mathcolon|ratio|textcolon)\b|:)\s*\}",
    re.IGNORECASE,
)
RAW_BAR_COMMAND_RE = re.compile(r"\\+(?:vert|mid)\b|\\+\|")
ALL_BAR_COMMAND_RE = re.compile(r"\\+(?:lvert|rvert|vert|mid)\b|\\+\|")
ENCODED_SQUARE_DELIMITERS = (
    (re.compile(r"\\+(?:lbrack|lBrack|Lbrack|llbracket|textlbrack)\b"), "["),
    (re.compile(r"\\+(?:rbrack|rBrack|Rbrack|rrbracket|textrbrack)\b"), "]"),
)


def _escaped(text: str, offset: int) -> bool:
    backslashes = 0
    offset -= 1
    while offset >= 0 and text[offset] == "\\":
        backslashes += 1
        offset -= 1
    return backslashes % 2 == 1


def _square_spans(text: str) -> Iterator[tuple[int, int]]:
    stack: list[int] = []
    for offset, character in enumerate(text):
        if character == "[" and not _escaped(text, offset):
            stack.append(offset)
        elif character == "]" and not _escaped(text, offset) and stack:
            yield stack.pop(), offset + 1


def _bar_spans(text: str, *, ignore_markdown_cells: bool = False) -> Iterator[tuple[int, int]]:
    start: int | None = None
    for offset, character in enumerate(text):
        if character != "|" or _escaped(text, offset):
            continue
        if ignore_markdown_cells:
            left = text[offset - 1] if offset else " "
            right = text[offset + 1] if offset + 1 < len(text) else " "
            if left.isspace() and right.isspace():
                continue
        if start is None:
            start = offset
        else:
            yield start, offset + 1
            start = None


def _top_level_colons(content: str) -> list[int]:
    braces = 0
    parentheses = 0
    colons: list[int] = []
    for offset, character in enumerate(content):
        if _escaped(content, offset):
            continue
        if character == "{":
            braces += 1
        elif character == "}" and braces:
            braces -= 1
        elif character == "(":
            parentheses += 1
        elif character == ")" and parentheses:
            parentheses -= 1
        elif character == ":" and braces == 0 and parentheses == 0:
            colons.append(offset)
    return colons


def _group_expression(expression: str, *, allow_identity: bool = False) -> bool:
    normalized = " ".join(expression.replace("$", " ").split())
    if not normalized or len(normalized) > 1000:
        return False
    if allow_identity and normalized in {"1", "{1}", "\\{1\\}"}:
        return True
    if any(token in normalized for token in ("http://", "https://", '"', "=")):
        return False
    return bool(
        TEX_GROUP_COMMAND_RE.search(normalized)
        or PLAIN_GROUP_NAME_RE.search(normalized)
        or BARE_GROUP_SYMBOL_RE.search(normalized)
    )


def _decode_index_tokens(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", html.unescape(text))
    normalized = TEX_SIZE_COMMAND_RE.sub("", normalized)
    for pattern, replacement in ENCODED_SQUARE_DELIMITERS:
        normalized = pattern.sub(replacement, normalized)
    while True:
        replaced = TEX_MATH_CLASS_COLON_RE.sub(":", normalized)
        if replaced == normalized:
            break
        normalized = replaced
    normalized = TEX_COLON_COMMAND_RE.sub(":", normalized)
    return normalized


def _delimited_indices(
    text: str, spans: Iterator[tuple[int, int]]
) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    for start, end in spans:
        content = text[start + 1 : end - 1]
        for colon in _top_level_colons(content):
            left = content[:colon]
            right = content[colon + 1 :]
            if _group_expression(left) and _group_expression(right, allow_identity=True):
                findings.append((start, text[start:end]))
                break
    return findings


def find_square_delimited_indices(text: str) -> list[tuple[int, str]]:
    normalized = _decode_index_tokens(text)
    return _delimited_indices(normalized, _square_spans(normalized))


def find_raw_bar_indices(
    text: str, *, include_lr: bool = False, markdown: bool = False
) -> list[tuple[int, str]]:
    normalized = _decode_index_tokens(text)
    pattern = ALL_BAR_COMMAND_RE if include_lr else RAW_BAR_COMMAND_RE
    normalized = pattern.sub("|", normalized)
    return _delimited_indices(
        normalized, _bar_spans(normalized, ignore_markdown_cells=markdown)
    )


def find_sized_indices(text: str) -> list[str]:
    findings: list[str] = []
    for line in text.splitlines():
        if not TEX_SIZE_COMMAND_RE.search(line):
            continue
        if find_square_delimited_indices(line) or find_raw_bar_indices(line, include_lr=True):
            findings.append(line)
    return findings


def find_textual_indices(text: str) -> list[str]:
    normalized = _decode_index_tokens(text)
    findings: list[str] = []
    for match in re.finditer(r"\b(?:subgroup\s+)?index\b", normalized, re.IGNORECASE):
        tail = re.split(r"[.!?;\n]", normalized[match.end() :], maxsplit=1)[0]
        if tail.lstrip().startswith(":"):
            continue
        candidate = tail.split("=", 1)[0]
        if re.search(r"\\lvert\b.*\\rvert\b", candidate):
            continue
        for colon in _top_level_colons(candidate):
            if _group_expression(candidate[:colon]) and _group_expression(
                candidate[colon + 1 :], allow_identity=True
            ):
                findings.append(candidate)
                break
    return findings


def check_path_policy(paths: Sequence[Path]) -> None:
    forbidden_tokens = {
        "revi" + "ew",
        "revi" + "ews",
        "revi" + "ewer",
        "revi" + "ewers",
        "ref" + "eree",
        "ref" + "erees",
        "aud" + "it",
        "aud" + "itor",
        "role" + "-matrix",
        "rea" + "der-test",
        "pending" + "-evaluation",
        "sign" + "-off",
    }
    for path in paths:
        normalized_parts = [
            re.sub(r"[^a-z0-9]+", "-", part.lower()).strip("-")
            for part in path.parts
        ]
        for part in normalized_parts:
            words = set(filter(None, part.split("-")))
            require(part not in forbidden_tokens,
                    f"forbidden process artifact path: {path}")
            require(not words.intersection(forbidden_tokens),
                    f"forbidden process artifact path: {path}")


def check_git_metadata() -> None:
    """Apply the public-text policy to every commit reachable from HEAD."""

    head = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD^{commit}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if head.returncode != 0:
        return
    result = subprocess.run(
        [
            "git", "log", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce%x00%s%x00",
            "HEAD",
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, "git could not inspect public commit metadata")
    fields = result.stdout.decode("utf-8", errors="strict").split("\0")
    require(fields and fields[-1].strip() == "", "malformed Git metadata stream")
    fields = fields[:-1]
    require(len(fields) % 6 == 0, "malformed Git metadata field inventory")
    identity = ("Richie Sater", "15129476+RichieSater@users.noreply.github.com")
    for offset in range(0, len(fields), 6):
        commit, author, author_email, committer, committer_email, subject = fields[offset:offset + 6]
        require((author, author_email) == identity,
                f"unexpected author identity in commit {commit[:12]}")
        require((committer, committer_email) == identity,
                f"unexpected committer identity in commit {commit[:12]}")
        for pattern in process_patterns():
            require(pattern.search(subject) is None,
                    f"process language in commit {commit[:12]}")
        metadata_path = Path("commit-subject.txt")
        require(human_gate_sentence(subject, metadata_path) is None,
                f"person-dependent status in commit {commit[:12]}")
        for pattern in disclosure_patterns():
            require(pattern.search(subject) is None,
                    f"disclosure terminology in commit {commit[:12]}")
        require(structural_disclosure(subject, metadata_path) is None,
                f"disclosure terminology in commit {commit[:12]}")


def check_text(path: Path, text: str, *, rendered_manuscript: bool = False) -> None:
    for pattern in process_patterns():
        require(pattern.search(text) is None, f"process/gate language in {path}")
    require(human_gate_sentence(text, path) is None,
            f"person-dependent status in {path}")

    if path != PRINCIPAL and not rendered_manuscript:
        for pattern in disclosure_patterns():
            require(pattern.search(text) is None,
                    f"disclosure terminology outside principal manuscript: {path}")
        require(structural_disclosure(text, path) is None,
                f"disclosure terminology outside principal manuscript: {path}")

    require(not find_square_delimited_indices(text),
            f"square-delimited subgroup index in {path}")
    require(not find_textual_indices(text),
            f"unbarred textual subgroup index in {path}")
    require(not find_sized_indices(text),
            f"manually sized subgroup index delimiters in {path}")

    if path.suffix.lower() == ".tex":
        require(not find_raw_bar_indices(text),
                f"raw-bar subgroup index in LaTeX text: {path}")
    elif path.suffix.lower() == ".md":
        for line in text.splitlines():
            if line.startswith(("    ", "\t")):
                continue
            require(not find_raw_bar_indices(line, markdown=True),
                    f"raw-bar subgroup index in LaTeX text: {path}")


def check_disclosure(principal: str) -> None:
    heading = "\\section*{" + "Gen" + "erative-" + "A" + "I disclosure}"
    bibliography = "\\begin{" + "thebibliography}"
    expected = (
        "Gen" + "erative-" + "A" + "I tools " + "were used for literature search, "
        "proof exploration, code generation, drafting, and critical checking; the author "
        "checked and takes responsibility for the manuscript's arguments, citations, and "
        "computations."
    )
    require(principal.count(heading) == 1, "principal disclosure heading count is not one")
    require(principal.count(bibliography) == 1, "principal bibliography boundary count")
    start = principal.index(heading)
    body_start = start + len(heading)
    end = principal.index(bibliography, body_start)
    body = re.sub(r"\s+", " ", principal[body_start:end]).strip()
    require(body == expected, "principal disclosure must be the one canonical sentence")
    outside = principal[:start] + principal[end:]
    for pattern in disclosure_patterns():
        require(pattern.search(outside) is None,
                "additional disclosure terminology in principal manuscript")
    require(structural_disclosure(outside, PRINCIPAL) is None,
            "additional disclosure terminology in principal manuscript")


def scan_tree(root: Path, paths: Sequence[Path], label: str) -> None:
    require(len(paths) == len(set(paths)), f"duplicate paths in {label}")
    check_path_policy(paths)
    principal = ""
    scanned = 0
    for path in paths:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            text = extract_pdf(root, path)
            check_text(path, text, rendered_manuscript=(path == RENDERED))
            scanned += 1
            continue
        if suffix in {".gz", ".tgz", ".zip", ".tar"}:
            fail(f"uninspected nested archive in {label}: {path}")
        text = read_text(root, path)
        check_text(path, text)
        if path == PRINCIPAL:
            principal = text
        scanned += 1
    require(principal != "", f"principal manuscript missing from {label}")
    check_disclosure(principal)
    print(f"PUBLIC CORPUS PASSED: {scanned} files scanned ({label})")


def extract_source_archive(
    archive: Path, destination: Path
) -> tuple[Path, list[Path], dict[Path, str], set[int]]:
    require(not archive.is_symlink(), f"source archive is a symbolic link: {archive}")
    require(archive.is_file(), f"missing source archive: {archive}")
    try:
        handle = tarfile.open(archive, mode="r:gz")
    except (tarfile.ReadError, OSError) as error:
        fail(f"could not open source archive {archive}: {error}")
    with handle:
        members = handle.getmembers()
        require(members, "source archive is empty")
        top_names: set[str] = set()
        files: list[Path] = []
        modes: dict[Path, str] = {}
        mtimes: set[int] = set()
        seen_members: set[str] = set()
        total_size = 0
        for member in members:
            require(member.name not in seen_members, f"duplicate archive member: {member.name}")
            seen_members.add(member.name)
            path = safe_path(member.name.rstrip("/"))
            top_names.add(path.parts[0])
            require(member.isdir() or member.isfile(),
                    f"non-regular archive member: {member.name}")
            require(member.uid == 0 and member.gid == 0,
                    f"nonzero archive ownership: {member.name}")
            require(member.uname == "" and member.gname == "",
                    f"named archive ownership: {member.name}")
            mtimes.add(int(member.mtime))
            if member.isdir():
                require(member.mode == 0o755, f"unexpected directory mode: {member.name}")
                continue
            require(member.mode in {0o644, 0o755},
                    f"unexpected regular-file mode: {member.name}")
            require(member.size <= MAX_ARCHIVE_FILE,
                    f"archive member too large: {member.name}")
            total_size += member.size
            require(total_size <= MAX_ARCHIVE_TOTAL, "source archive exceeds size limit")
            relative = Path(*path.parts[1:])
            require(relative.parts, f"top-level archive member is not a directory: {member.name}")
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            stream = handle.extractfile(member)
            require(stream is not None, f"could not read archive member: {member.name}")
            data = stream.read(MAX_ARCHIVE_FILE + 1)
            require(len(data) == member.size, f"short archive member: {member.name}")
            target.write_bytes(data)
            target.chmod(member.mode)
            files.append(relative)
            modes[relative] = "100755" if member.mode == 0o755 else "100644"
        require(len(top_names) == 1, "source archive must have one top-level directory")
        top = next(iter(top_names))
        root = destination / top
        require(root.is_dir(), "source archive top level is not a directory")
        require(len(files) == len(set(files)), "duplicate relative paths in source archive")
        return root, sorted(files, key=lambda item: item.as_posix()), modes, mtimes


def git_output(arguments: Sequence[str], context: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, context)
    return result.stdout


def verify_commit_binding(
    commit: str, entries: dict[Path, tuple[str, str]]
) -> None:
    require(commit != "0" * 40, "source-manifest commit is the all-zero identifier")
    resolved = git_output(
        ["rev-parse", "--verify", f"{commit}^{{commit}}"],
        "source-manifest commit is not available in the local Git object store",
    ).decode("ascii", errors="strict").strip()
    require(resolved == commit, "source-manifest commit did not resolve exactly")
    raw_tree = git_output(
        ["ls-tree", "-r", "-z", commit],
        "could not inspect source-manifest commit tree",
    )
    tree: dict[Path, tuple[str, str]] = {}
    chunks = raw_tree.split(b"\0")
    require(chunks and chunks[-1] == b"", "malformed Git tree stream")
    for raw in chunks[:-1]:
        try:
            prefix, encoded_name = raw.split(b"\t", 1)
            mode, object_type, object_id = prefix.decode("ascii").split()
            path = safe_path(encoded_name.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as error:
            fail(f"malformed Git tree entry: {error}")
        require(object_type == "blob", f"non-blob Git tree entry: {path}")
        require(mode in {"100644", "100755"}, f"non-regular Git mode: {path}")
        require(path not in tree, f"duplicate Git tree path: {path}")
        tree[path] = (mode, object_id)
    require(set(tree) == set(entries), "source manifest does not inventory the Git tree")
    for path, (digest, mode) in entries.items():
        tree_mode, object_id = tree[path]
        require(tree_mode == mode, f"source manifest and Git mode disagree: {path}")
        blob = git_output(["cat-file", "blob", object_id], f"could not read Git blob: {path}")
        require(hashlib.sha256(blob).hexdigest() == digest,
                f"source manifest and Git blob disagree: {path}")


def verify_source_manifest(
    root: Path, paths: Sequence[Path], modes: dict[Path, str]
) -> tuple[int, dict[str, str], dict[str, object]]:
    require(ARCHIVE_MANIFEST in paths, "source archive has no manifest")
    text = read_text(root, ARCHIVE_MANIFEST)
    lines = text.splitlines()
    require("" in lines, "source manifest has no header separator")
    separator = lines.index("")
    header_lines = lines[:separator]
    entry_lines = [line for line in lines[separator + 1:] if line]
    header: dict[str, str] = {}
    for line in header_lines:
        parts = line.split("=", 1)
        require(len(parts) == 2, "malformed source-manifest header")
        key, value = parts
        require(key not in header, f"duplicate source-manifest header: {key}")
        header[key] = value
    require(set(header) == {
        "schema_version", "publication_status", "source_date_epoch",
        "snapshot_kind", "source_commit", "hash_algorithm", "entry_format",
    }, "source-manifest header inventory")
    require(header["schema_version"] == "1", "source-manifest schema")
    require(header["publication_status"] == "preprint", "source-manifest status")
    require(header["source_date_epoch"].isdigit(), "source-manifest epoch")
    require(header["snapshot_kind"] in {"working-tree", "git-commit"},
            "source-manifest snapshot kind")
    if header["snapshot_kind"] == "git-commit":
        require(re.fullmatch(r"[0-9a-f]{40}", header["source_commit"]) is not None,
                "source-manifest commit")
    else:
        require(header["source_commit"] == "none",
                "working-tree manifest must not claim a source commit")
    require(header["hash_algorithm"] == "SHA-256", "source-manifest hash algorithm")
    require(header["entry_format"] == "sha256 git-mode path",
            "source-manifest entry format")

    entries: dict[Path, tuple[str, str]] = {}
    entry_pattern = re.compile(r"([0-9a-f]{64})  (100644|100755)  (.+)")
    for line in entry_lines:
        match = entry_pattern.fullmatch(line)
        require(match is not None, "malformed source-manifest entry")
        digest, mode, name = match.groups()
        path = safe_path(name)
        require(path != ARCHIVE_MANIFEST, "manifest must not hash itself")
        require(path not in entries, f"duplicate source-manifest path: {path}")
        entries[path] = (digest, mode)
    require(list(entries) == sorted(entries, key=lambda item: item.as_posix()),
            "source-manifest entries are not sorted")
    expected = sorted((path for path in paths if path != ARCHIVE_MANIFEST),
                      key=lambda item: item.as_posix())
    require(list(entries) == expected, "source-manifest inventory mismatch")
    for path, (digest, mode) in entries.items():
        require(hashlib.sha256((root / path).read_bytes()).hexdigest() == digest,
                f"source-manifest digest mismatch: {path}")
        require(modes.get(path) == mode, f"source-manifest mode mismatch: {path}")
    require(modes.get(ARCHIVE_MANIFEST) == "100644", "source-manifest file mode")

    try:
        metadata = json.loads(read_text(root, Path("artifact-metadata.json")))
    except json.JSONDecodeError as error:
        fail(f"malformed authoritative metadata in source archive: {error}")
    require(isinstance(metadata, dict), "source-archive metadata root is not an object")
    require(str(metadata.get("source_date_epoch")) == header["source_date_epoch"],
            "manifest and authoritative epoch disagree")
    require(metadata.get("publication_status") == header["publication_status"],
            "manifest and authoritative status disagree")
    version = metadata.get("artifact_version")
    expected_stem = (
        "kourovka-18-68-preprint"
        if version is None
        else f"kourovka-18-68-v{version}"
    )
    require(metadata.get("source_archive_stem") == expected_stem,
            "source-archive stem in authoritative metadata")
    if header["snapshot_kind"] == "git-commit":
        verify_commit_binding(header["source_commit"], entries)
    return int(header["source_date_epoch"]), header, metadata


def scan_archive(archive: Path, expected: Sequence[Path] | None) -> None:
    with tempfile.TemporaryDirectory(prefix="k186-public-archive-") as directory:
        root, paths, modes, mtimes = extract_source_archive(archive, Path(directory))
        if expected is not None:
            expected_paths = sorted([*expected, ARCHIVE_MANIFEST], key=lambda item: item.as_posix())
            require(paths == expected_paths, "source archive does not match explicit allowlist")
        epoch, header, metadata = verify_source_manifest(root, paths, modes)
        suffix = "-working-tree" if header["snapshot_kind"] == "working-tree" else ""
        expected_top = f"{metadata['source_archive_stem']}{suffix}"
        require(root.name == expected_top, "source archive top-level name disagrees with metadata")
        require(archive.name == f"{expected_top}-source.tar.gz",
                "source archive filename disagrees with metadata and snapshot kind")
        require(mtimes == {epoch}, "archive member timestamps disagree with manifest")
        scan_tree(root, paths, f"extracted archive {archive.name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths-file", type=Path,
                        help="scan this explicit sorted allowlist instead of Git's inventory")
    parser.add_argument("--archive", type=Path,
                        help="safely extract and scan a .tar.gz source archive")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    expected = load_paths_file(args.paths_file) if args.paths_file else None
    if args.archive:
        scan_archive(args.archive, expected)
        return
    check_git_metadata()
    paths = expected if expected is not None else tracked_paths()
    scan_tree(ROOT, paths, "explicit allowlist" if expected is not None else "tracked working tree")


if __name__ == "__main__":
    main()
