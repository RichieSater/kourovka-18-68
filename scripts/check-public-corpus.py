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
        r"\bresponsible\s+for\s+(?:check" + r"ing|eval" + r"uating|appro" +
        r"ving|vali" + r"dating|veri" + r"fying|revi" + r"ewing|rele" +
        r"asing|publi" + r"shing|submi" + r"tting)\b",
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


def policy_windows(text: str, path: Path, *, adjacent: bool = True) -> Iterator[str]:
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
        if adjacent and index + 1 < len(normalized):
            pair = " ".join((window, normalized[index + 1])).strip()
            if pair:
                yield pair


PUBLICATION_SIGNAL = re.compile(
    r"\b(?:rele" + r"as(?:e|es|ed|ing)|publi" + r"(?:sh|shes|shing|cation)|"
    r"submi" + r"(?:t|ts|tted|ssion)|readi" + r"ness|ready|"
    r"circulat(?:e|es|ed|ing|ion)|post(?:s|ed|ing)?|deposit|upload|"
    r"public\s+update|comple" + r"tion)\b|\bgo(?:es|ing|ne)?\s+(?:online|live)\b|"
    r"\bappear(?:s|ed|ing)?\s+(?:online|publicly)\b|"
    r"\b(?:make|makes|made|making)\s+(?:the\s+)?(?:preprint|manuscript|work)\s+"
    r"(?:public|available)\b|\b(?:be|been|being|is|are|was|were|get|gets|got|may\s+be|"
    r"can\s+be|will\s+be)\s+published\b"
)
CONDITION_SIGNAL = re.compile(
    r"\b(?:after|before|until|unless|once|when|whenever|if|provided\s+that|"
    r"only\s+if|only\s+after|without|"
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
    r"rests?\s+in\s+the\s+hands\s+of|at\s+[^.!?]{1,80}\s+discretion|"
    r"(?:on|upon|under)\s+[^.!?]{1,80}\s+(?:say\s+so|verdict|recommendation)|"
    r"controls?\s+whether|decides?\s+whether|has\s+(?:the\s+)?final\s+decision|"
    r"follows?\s+[^.!?]{1,80}\s+decision|"
    r"(?:is|are|be|been|being)\s+(?:decided|determined|controlled)\s+by)\b"
)
PUBLIC_APPROVAL_GATE_SIGNAL = re.compile(
    r"\b(?:after|before|until|unless|once|when|whenever|if|provided\s+that|"
    r"with|upon|on|under|at|needs?|tied\s+to|"
    r"only\s+if|only\s+after|depends?\s+(?:on|upon)|requires?|awaits?|"
    r"subject\s+to|contingent\s+(?:on|upon)|conditional\s+(?:on|upon))\b"
    r"[^.!?]{0,100}\b(?:consen" + r"t|authori" + r"zation|assen" + r"t|"
    r"appro" + r"val|permission|endorsement|clearance|signature|verdict|"
    r"say\s+so|recommendation|judg(?:e)?ment|blessing|discretion|pleasure|"
    r"thumbs?\s+up|green\s+light|go\s+ahead)\b|"
    r"\b(?:if|unless|once|when|whenever|provided\s+that|after|before|until)\s+"
    r"(?!(?:manuscript|preprint|proof|result|theorem|classification|equation|"
    r"invariant|calculation|software|script|checker|test)\b)"
    r"(?:the\s+)?[a-z][a-z0-9'-]*\s+(?:agree(?:s|d)|signs?|signed|"
    r"appro" + r"v(?:e|es|ed)|authori" + r"z(?:e|es|ed)|endorse(?:s|d)?|"
    r"certif(?:y|ies|ied)|confirms?|confirmed|says?\s+yes|nods?)\b|"
    r"\b(?:consen" + r"t|authori" + r"zation|assen" + r"t|appro" + r"val|"
    r"permission|endorsement|clearance|signature)\b[^.!?]{0,100}\b"
    r"(?:required|needed|mandatory|must)\b"
)
PROPER_NAME_RE = re.compile(r"(?<![A-Za-z])([A-Z][a-z]+(?:-[A-Z]?[a-z]+)*)\b")
NONPERSON_PROPER_NAMES = {
    "A", "After", "An", "Appendix", "Article", "Before", "Classification",
    "Build", "Check", "Corollary", "Equation", "Figure", "If", "Install",
    "Group", "Lemma", "Lean", "Manuscript", "Magma", "Mathematica", "Paper",
    "Preprint", "Proposition", "Publication", "Python", "Release", "Research", "Result",
    "Rocq", "Run", "Rust", "Sage", "Section", "See", "Software", "Submission", "Table", "The",
    "Tectonic", "Theorem", "Third-party", "This", "TomLib", "When", "Whenever",
}
TASK_OWNERSHIP_SIGNAL = re.compile(
    r"\b(?:proof\s+)?(?:check(?:ing)?|veri" + r"fication|vali" + r"dation|"
    r"eval" + r"uation|revi" + r"ew)\s+(?:is|remains|becomes)\s+[^.!?]{1,80}\s+"
    r"(?:job|duty|responsibility|assignment)\b|"
    r"\b[^.!?]{1,80}\s+(?:job|duty|responsibility|assignment)\s+(?:is|includes)\s+"
    r"(?:proof\s+)?(?:check(?:ing)?|veri" + r"fication|vali" + r"dation|"
    r"eval" + r"uation|revi" + r"ew)\b"
)
TASK_ASSIGNMENT_SIGNAL = re.compile(
    r"\b[^.!?]{0,80}\s+(?:will\s+)?(?:perform(?:s|ed|ing)?|conduct(?:s|ed|ing)?|"
    r"oversee(?:s|ing)?|handle(?:s|d|ing)?|undertak(?:e|es|ing)|carries\s+out)\s+"
    r"(?:the\s+)?(?:proof\s+)?(?:check(?:ing)?|veri" + r"fication|vali" +
    r"dation|eval" + r"uation|revi" + r"ew)\b|"
    r"\b[^.!?]{0,80}\s+(?:will\s+)?(?:check(?:s|ed|ing)?|verif(?:y|ies|ied|ying)|"
    r"vali" + r"dat(?:e|es|ed|ing)|eval" + r"uat(?:e|es|ed|ing)|revi" +
    r"ew(?:s|ed|ing)?)\s+(?:the\s+)?proof\b|"
    r"\b[^.!?]{0,80}\s+has\s+(?:the\s+)?responsibility\s+for\s+"
    r"(?:proof\s+)?(?:check(?:ing)?|veri" + r"fication|vali" + r"dation|"
    r"eval" + r"uation|revi" + r"ew)\b|"
    r"\b[^.!?]{0,80}\s+is\s+responsible\s+for\s+(?:proof\s+)?"
    r"(?:check(?:ing)?|veri" + r"fication|vali" + r"dation|eval" +
    r"uation|revi" + r"ew)\b|"
    r"\b[^.!?]{0,80}\s+(?:has\s+been|was|is|will\s+be)\s+asked\s+to\s+"
    r"(?:check|verify|vali" + r"date|eval" + r"uate|revi" + r"ew)\s+"
    r"(?:the\s+)?proof\b|"
    r"\b[^.!?]{0,80}\s+is\s+(?:the\s+)?(?:proof\s+)?"
    r"(?:checker|verifier|validator|evaluator)\b|"
    r"\b(?:proof\s+)?(?:check(?:ing)?|veri" + r"fication|vali" + r"dation|"
    r"eval" + r"uation|revi" + r"ew)\s+(?:falls|belongs)\s+to\b"
)
AUTOMATED_CHECK_SIGNAL = re.compile(
    r"\b(?:deterministic\s+)?(?:algorithm|script|checker|tests?|command|program|"
    r"software|tool|system|workflow|pipeline|ci|build|computation|certificate|"
    r"gap|lean|rocq|rust|python|sage|magma|mathematica)\s+(?:automatically\s+)?"
    r"(?:check(?:s|ed|ing)?|inspect(?:s|ed|ing)?|verif(?:y|ies|ied|ying)|"
    r"vali" + r"dat(?:e|es|ed|ing)|assess(?:es|ed|ing)?|perform(?:s|ed|ing)?|"
    r"conduct(?:s|ed|ing)?|oversee(?:s|ing)?|handle(?:s|d|ing)?|carries\s+out)\b|"
    r"\b(?:check(?:s|ed|ing)?|inspect(?:s|ed|ing)?|verif(?:y|ies|ied|ying)|"
    r"vali" + r"dat(?:e|es|ed|ing)|assess(?:es|ed|ing)?)\b[^.!?]{0,100}\b"
    r"(?:by|using|via|with)\s+(?:a\s+|the\s+)?(?:algorithm|script|checker|tests?|"
    r"command|program|software|tool|system|workflow|pipeline|ci|build|computation|"
    r"certificate|gap|lean|rocq|rust|python|sage|magma|mathematica)\b"
)
FINAL_PROOF_TASK_SIGNAL = re.compile(
    r"\b(?:final|last)\s+(?:proof\s+)?"
    r"(?:check|veri" + r"fication|vali" + r"dation|eval" + r"uation)\b|"
    r"\b(?:check(?:ing)?|veri" + r"f(?:y|ying)|vali" + r"dat(?:e|ing)|"
    r"eval" + r"uat(?:e|ing))\s+(?:the\s+)?(?:final|last)\s+proof\b"
)


def raw_policy_chunks(text: str, path: Path) -> list[str]:
    if path.suffix.lower() in {".py", ".sh"} or path.name == "Makefile":
        return [line for line in text.splitlines() if line.strip()]
    return [
        chunk.strip()
        for chunk in re.split(r"(?<=[.!?])(?:[\"')\]]*)\s+|\n[ \t]*\n|\n", text)
        if chunk.strip()
    ]


def contains_person_name(raw: str) -> bool:
    for match in PROPER_NAME_RE.finditer(unicodedata.normalize("NFKC", raw)):
        name = match.group(1)
        prefix = raw[:match.start()]
        if not prefix.strip() or re.search(r"[.!?]\s*$", prefix):
            continue
        if name in NONPERSON_PROPER_NAMES:
            continue
        suffix = raw[match.end():match.end() + 40]
        if re.match(r"['’]s\s+(?:theorem|lemma|result|classification|paper|article)\b",
                    suffix, re.IGNORECASE):
            continue
        return True
    return False


def human_gate_sentence(text: str, path: Path) -> str | None:
    """Return a normalized structural public-status gate or task allocation."""

    source_code = path.suffix.lower() in {".py", ".sh"} or path.name == "Makefile"
    if not source_code:
        chunks = raw_policy_chunks(text, path)
        for index, raw in enumerate(chunks):
            candidates = [raw]
            if index + 1 < len(chunks):
                candidates.append(raw + ". " + chunks[index + 1])
            for candidate in candidates:
                window = normalize_policy_text(candidate)
                if not PUBLICATION_SIGNAL.search(window) or not contains_person_name(candidate):
                    continue
                if (
                    CONDITION_SIGNAL.search(window)
                    or RESPONSIBILITY_SIGNAL.search(window)
                    or PUBLIC_APPROVAL_GATE_SIGNAL.search(window)
                ):
                    return window
    for window in policy_windows(text, path):
        public_state = bool(PUBLICATION_SIGNAL.search(window))
        condition = bool(CONDITION_SIGNAL.search(window))
        actor = bool(ACTOR_SIGNAL.search(window))
        action = bool(HUMAN_ACTION_SIGNAL.search(window))
        if ASSIGNMENT_SIGNAL.search(window) and PROCESS_TASK_SIGNAL.search(window):
            return window
        if FINAL_PROOF_TASK_SIGNAL.search(window):
            return window
        if TASK_OWNERSHIP_SIGNAL.search(window):
            return window
        task_allocation = TASK_ASSIGNMENT_SIGNAL.search(window)
        automated_allocation = AUTOMATED_CHECK_SIGNAL.search(window)
        if task_allocation and not automated_allocation:
            return window
        if public_state and PUBLIC_APPROVAL_GATE_SIGNAL.search(window):
            return window
        if public_state and RESPONSIBILITY_SIGNAL.search(window):
            return window
        if public_state and actor and DECISION_ACTION_SIGNAL.search(window):
            return window
        if (
            not source_code
            and public_state
            and action
            and condition
            and not AUTOMATED_CHECK_SIGNAL.search(window)
        ):
            return window
    return None


def disclosure_patterns() -> list[re.Pattern[str]]:
    terms = [
        r"\bgen" + r"erative\b",
        r"\bartificial\s+intel" + r"ligence\b",
        r"\blanguage\s+mod" + r"els?\b",
        r"\blarge\s+language\s+mod" + r"els?\b",
        r"\bL" + r"LMs?\b",
        r"\bChat" + r"G" + r"PT\b",
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
DISCLOSURE_AGENT_SIGNAL = re.compile(
    r"\b(?:mod" + r"el|net" + r"work|net|bo" + r"t|robot|assistant|agent|"
    r"engine|generator|service|transformer)\b"
)
DISCLOSURE_QUALIFIED_AGENT_SIGNAL = re.compile(
    r"\b(?:machine\s+intelligen(?:ce|t)|language|neural|statistical|predictive|"
    r"deep\s+learning|"
    r"automated|algorithmic|foundation|autoregressive|gen" + r"erative)\s+"
    r"(?:mod" + r"el|net" + r"work|net|algor" + r"ithm|soft" + r"ware|program|tool|"
    r"system|application|bo" + r"t|robot|assistant|agent|engine|generator|service|"
    r"transformer)\b"
)
DISCLOSURE_VENDOR_SIGNAL = re.compile(
    r"\b(?:Cod" + r"ex|Open" + r"A" + r"I|Anthro" + r"pic|Cla" + r"ude|"
    r"Gem" + r"ini|Co" + r"pilot|Gr" + r"ok|Ll" + r"ama|Mis" + r"tral|"
    r"Perplex" + r"ity|Deep" + r"Seek|G" + r"P" + r"T(?:[- ]?[0-9][0-9A-Za-z.]*)?)\b",
    re.IGNORECASE,
)
DISCLOSURE_TECHNOLOGY_SIGNAL = re.compile(
    r"\b(?:machine\s+learning|artificial\s+intelligence|gen" + r"erative\s+"
    r"(?:a\s+i|technology|software))\b"
)
DISCLOSURE_ACTION_SIGNAL = re.compile(
    r"\b(?:draft(?:s|ed|ing)?|writ(?:e|es|ing)|wrote|edit(?:s|ed|ing)?|"
    r"revis(?:e|es|ed|ing)|generat(?:e|es|ed|ing)|assist(?:s|ed|ing)?|"
    r"author(?:s|ed|ing)?|produc(?:e|es|ed|ing)|compos(?:e|es|ed|ing)|"
    r"creat(?:e|es|ed|ing)?|rewrit(?:e|es|ten|ing)|rewrote|"
    r"synthesi[sz](?:e|es|ed|ing)|paraphras(?:e|es|ed|ing)|"
    r"polish(?:es|ed|ing)?|proofread(?:s|ing)?|correct(?:s|ed|ing)?|"
    r"prepar(?:e|es|ed|ing)?)\b"
)
DISCLOSURE_CONTENT_SIGNAL = re.compile(
    r"\b(?:prose|te" + r"xt(?!\s+(?:files?|data|corpus|encoding|extraction)\b)|"
    r"manuscript(?!\s+(?:index|table|source|file)\b)|documentation|wording|copy|"
    r"drafting|writing|editing|authoring|paragraph|section|article|paper)\b"
)


def structural_disclosure(text: str, path: Path) -> str | None:
    sentences = list(policy_windows(text, path, adjacent=False))
    for window in sentences:
        if (
            DISCLOSURE_FORM_A.search(window)
            or DISCLOSURE_FORM_B.search(window)
            or DISCLOSURE_FORM_C.search(window)
            or (
                DISCLOSURE_AGENT_SIGNAL.search(window)
                or DISCLOSURE_QUALIFIED_AGENT_SIGNAL.search(window)
                or DISCLOSURE_TECHNOLOGY_SIGNAL.search(window)
                or DISCLOSURE_VENDOR_SIGNAL.search(window)
            )
            and DISCLOSURE_ACTION_SIGNAL.search(window)
            and DISCLOSURE_CONTENT_SIGNAL.search(window)
        ):
            return window
    for first, second in zip(sentences, sentences[1:]):
        agent = (
            DISCLOSURE_AGENT_SIGNAL.search(first)
            or DISCLOSURE_QUALIFIED_AGENT_SIGNAL.search(first)
            or DISCLOSURE_TECHNOLOGY_SIGNAL.search(first)
            or DISCLOSURE_VENDOR_SIGNAL.search(first)
        )
        if (
            agent
            and re.search(r"\b(?:was|were|is|are)\s+(?:used|employed)\b", first)
            and re.match(r"(?:it|this\s+(?:tool|system|program|application|model))\b", second)
            and DISCLOSURE_ACTION_SIGNAL.search(second)
            and DISCLOSURE_CONTENT_SIGNAL.search(second)
        ):
            return first + " " + second
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
    r"\\+(?:colon|mathcolon|ratio|textcolon|vcentcolon)\b", re.IGNORECASE
)
TEX_MATH_CLASS_COLON_RE = re.compile(
    r"\\+(?:mathord|mathop|mathbin|mathrel|mathopen|mathclose|mathpunct|"
    r"mathinner)\s*\{\s*(?:\\+(?:colon|mathcolon|ratio|textcolon|vcentcolon)\b|:)\s*\}",
    re.IGNORECASE,
)
TEX_WRAPPED_COLON_RE = re.compile(
    r"\\+[A-Za-z]+\*?\s*\{\s*"
    r"(?:\\+(?:colon|mathcolon|ratio|textcolon|vcentcolon)\b|:)\s*\}",
    re.IGNORECASE,
)
TEX_BRACED_COLON_RE = re.compile(r"\{\s*:\s*\}")
RAW_BAR_COMMAND_RE = re.compile(r"\\+(?:vert|mid|textbar)\b|\\+\|")
ALL_BAR_COMMAND_RE = re.compile(r"\\+(?:lvert|rvert|vert|mid|textbar)\b|\\+\|")
ENCODED_SQUARE_DELIMITERS = (
    (re.compile(r"\\+(?:lbrack|lBrack|Lbrack|llbracket|textlbrack)\b"), "["),
    (re.compile(r"\\+(?:rbrack|rBrack|Rbrack|rrbracket|textrbrack)\b"), "]"),
)
ENCODED_CSNAME_TOKENS = (
    (re.compile(r"\\+csname\s*(?:lbrack|lBrack|Lbrack|llbracket|textlbrack)\s*"
                r"\\+endcsname", re.IGNORECASE), "["),
    (re.compile(r"\\+csname\s*(?:rbrack|rBrack|Rbrack|rrbracket|textrbrack)\s*"
                r"\\+endcsname", re.IGNORECASE), "]"),
    (re.compile(r"\\+csname\s*(?:colon|mathcolon|ratio|textcolon|vcentcolon)\s*"
                r"\\+endcsname", re.IGNORECASE), ":"),
)
ENCODED_CHAR_TOKENS = (
    (re.compile(r"\\+char\s*(?:58(?![0-9])|[\"']3[aA](?![0-9A-Fa-f])|[']72(?![0-7]))"), ":"),
    (re.compile(r"\\+char\s*(?:91(?![0-9])|[\"']5[bB](?![0-9A-Fa-f])|[']133(?![0-7]))"), "["),
    (re.compile(r"\\+char\s*(?:93(?![0-9])|[\"']5[dD](?![0-9A-Fa-f])|[']135(?![0-7]))"), "]"),
)
ENCODED_MATHCHAR_TOKENS = (
    (re.compile(r"\\+mathchar\s*[\"']?[0-9A-Fa-f]*3[aA](?![0-9A-Fa-f])"), ":"),
    (re.compile(r"\\+mathchar\s*[\"']?[0-9A-Fa-f]*5[bB](?![0-9A-Fa-f])"), "["),
    (re.compile(r"\\+mathchar\s*[\"']?[0-9A-Fa-f]*5[dD](?![0-9A-Fa-f])"), "]"),
)
TEX_NEWCOMMAND_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand)\*?"
)
TEX_DEF_RE = re.compile(r"\\(?:def|gdef|edef|xdef)\s*\\([A-Za-z@]+)")
TEX_LET_RE = re.compile(
    r"\\let\s*\\([A-Za-z@]+)\s*=?\s*(\\[A-Za-z@]+|.)", re.DOTALL
)


def _escaped(text: str, offset: int) -> bool:
    backslashes = 0
    offset -= 1
    while offset >= 0 and text[offset] == "\\":
        backslashes += 1
        offset -= 1
    return backslashes % 2 == 1


def _skip_space(text: str, offset: int) -> int:
    while offset < len(text) and text[offset].isspace():
        offset += 1
    return offset


def _braced_argument(text: str, offset: int) -> tuple[str, int] | None:
    """Parse one balanced TeX braced argument, returning content and end."""

    offset = _skip_space(text, offset)
    if offset >= len(text) or text[offset] != "{":
        return None
    depth = 0
    start = offset + 1
    for cursor in range(offset, len(text)):
        if _escaped(text, cursor):
            continue
        if text[cursor] == "{":
            depth += 1
        elif text[cursor] == "}":
            depth -= 1
            if depth == 0:
                return text[start:cursor], cursor + 1
    return None


def _square_argument(text: str, offset: int) -> tuple[str, int] | None:
    offset = _skip_space(text, offset)
    if offset >= len(text) or text[offset] != "[":
        return None
    depth = 0
    start = offset + 1
    for cursor in range(offset, len(text)):
        if _escaped(text, cursor):
            continue
        if text[cursor] == "[":
            depth += 1
        elif text[cursor] == "]":
            depth -= 1
            if depth == 0:
                return text[start:cursor], cursor + 1
    return None


def _simple_tex_macros(
    text: str,
) -> tuple[dict[str, tuple[int, str, str | None]], list[tuple[int, int]]]:
    """Collect ordinary zero-to-nine-argument TeX macro definitions.

    This deliberately small parser covers the standard definition forms used
    by the manuscript and prevents a delimiter or disclosure token from being
    hidden behind simple source macros.  TeX remains the rendering authority;
    the rendered manuscript is checked separately below.
    """

    macros: dict[str, tuple[int, str, str | None]] = {}
    ranges: list[tuple[int, int]] = []
    for match in TEX_NEWCOMMAND_RE.finditer(text):
        cursor = _skip_space(text, match.end())
        name = ""
        if cursor < len(text) and text[cursor] == "{":
            parsed_name = _braced_argument(text, cursor)
            if parsed_name is None:
                continue
            raw_name, cursor = parsed_name
            name_match = re.fullmatch(r"\\([A-Za-z@]+)", raw_name.strip())
            if name_match is None:
                continue
            name = name_match.group(1)
        else:
            name_match = re.match(r"\\([A-Za-z@]+)", text[cursor:])
            if name_match is None:
                continue
            name = name_match.group(1)
            cursor += name_match.end()
        cursor = _skip_space(text, cursor)
        arguments = 0
        optional_default: str | None = None
        if cursor < len(text) and text[cursor] == "[":
            close = text.find("]", cursor + 1)
            if close == -1 or not text[cursor + 1:close].strip().isdigit():
                continue
            arguments = int(text[cursor + 1:close].strip())
            if not 0 <= arguments <= 9:
                continue
            cursor = _skip_space(text, close + 1)
            if cursor < len(text) and text[cursor] == "[":
                parsed_default = _square_argument(text, cursor)
                if parsed_default is None:
                    continue
                optional_default, cursor = parsed_default
                cursor = _skip_space(text, cursor)
        parsed_body = _braced_argument(text, cursor)
        if parsed_body is None:
            continue
        body, end = parsed_body
        macros[name] = (arguments, body, optional_default)
        ranges.append((match.start(), end))

    for match in TEX_DEF_RE.finditer(text):
        name = match.group(1)
        cursor = match.end()
        body_start = text.find("{", cursor)
        if body_start == -1:
            continue
        parameter_text = text[cursor:body_start]
        if not re.fullmatch(r"(?:\s*#[1-9])*\s*", parameter_text):
            continue
        numbers = [int(item) for item in re.findall(r"#([1-9])", parameter_text)]
        arguments = max(numbers, default=0)
        if numbers and numbers != list(range(1, arguments + 1)):
            continue
        parsed_body = _braced_argument(text, body_start)
        if parsed_body is None:
            continue
        body, end = parsed_body
        macros[name] = (arguments, body, None)
        ranges.append((match.start(), end))
    for match in TEX_LET_RE.finditer(text):
        macros[match.group(1)] = (0, match.group(2), None)
        ranges.append((match.start(), match.end()))
    return macros, ranges


def expand_simple_tex_macros(text: str) -> str:
    """Expand standard source macros sufficiently for policy and notation scans."""

    macros, ranges = _simple_tex_macros(text)
    if not macros:
        return text
    masked = list(text)
    for start, end in ranges:
        masked[start:end] = " " * (end - start)
    expanded = "".join(masked)

    names = "|".join(re.escape(name) for name in sorted(macros, key=len, reverse=True))
    invocation = re.compile(r"\\(" + names + r")(?![A-Za-z@])")
    for _round in range(20):
        changed = False
        pieces: list[str] = []
        cursor = 0
        for match in invocation.finditer(expanded):
            if match.start() < cursor:
                continue
            name = match.group(1)
            arguments, body, optional_default = macros[name]
            end = match.end()
            values: list[str] = []
            valid = True
            required = arguments
            used_optional = False
            if optional_default is not None:
                parsed_optional = _square_argument(expanded, end)
                if parsed_optional is None:
                    values.append(optional_default)
                else:
                    value, end = parsed_optional
                    values.append(value)
                    used_optional = True
                required -= 1
            for _index in range(required):
                parsed = _braced_argument(expanded, end)
                if parsed is None:
                    if used_optional:
                        values.extend("G" for _missing in range(required - _index))
                    else:
                        valid = False
                    break
                value, end = parsed
                values.append(value)
            if not valid:
                continue
            replacement = body
            for number, value in enumerate(values, 1):
                replacement = replacement.replace(f"#{number}", value)
            pieces.append(expanded[cursor:match.start()])
            pieces.append(replacement)
            cursor = end
            changed = True
        if changed:
            pieces.append(expanded[cursor:])
            expanded = "".join(pieces)
            require(len(expanded) <= 8 * 1024 * 1024,
                    "expanded TeX policy text is unexpectedly large")
        if not changed:
            break
    return expanded


def _square_spans(text: str) -> Iterator[tuple[int, int]]:
    stack: list[int] = []
    for offset, character in enumerate(text):
        if character == "[" and not _escaped(text, offset):
            stack.append(offset)
        elif character == "]" and not _escaped(text, offset) and stack:
            yield stack.pop(), offset + 1


def _standalone_square_spans(text: str) -> Iterator[tuple[int, int]]:
    """Yield mathematical-looking brackets, not programming subscripts."""

    for start, end in _square_spans(text):
        previous = text[start - 1] if start else ""
        if previous and (previous.isalnum() or previous in "_)]}"):
            continue
        yield start, end


def _bar_spans(text: str) -> Iterator[tuple[int, int]]:
    start: int | None = None
    for offset, character in enumerate(text):
        if character != "|" or _escaped(text, offset):
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
    normalized = normalized.translate(str.maketrans({
        "∶": ":",
        "꞉": ":",
        "︰": ":",
        "﹕": ":",
        "∣": "|",
        "❘": "|",
        "⏐": "|",
        "｜": "|",
        "⟦": "[",
        "⟧": "]",
        "〚": "[",
        "〛": "]",
    }))
    normalized = TEX_SIZE_COMMAND_RE.sub("", normalized)
    for pattern, replacement in ENCODED_SQUARE_DELIMITERS:
        normalized = pattern.sub(replacement, normalized)
    for pattern, replacement in ENCODED_CSNAME_TOKENS:
        normalized = pattern.sub(replacement, normalized)
    for pattern, replacement in ENCODED_CHAR_TOKENS:
        normalized = pattern.sub(replacement, normalized)
    for pattern, replacement in ENCODED_MATHCHAR_TOKENS:
        normalized = pattern.sub(replacement, normalized)
    while True:
        replaced = TEX_MATH_CLASS_COLON_RE.sub(":", normalized)
        replaced = TEX_WRAPPED_COLON_RE.sub(":", replaced)
        replaced = TEX_COLON_COMMAND_RE.sub(":", replaced)
        replaced = TEX_BRACED_COLON_RE.sub(":", replaced)
        if replaced == normalized:
            break
        normalized = replaced
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
    return _delimited_indices(normalized, _standalone_square_spans(normalized))


def find_raw_bar_indices(text: str, *, include_lr: bool = False) -> list[tuple[int, str]]:
    normalized = _decode_index_tokens(text)
    pattern = ALL_BAR_COMMAND_RE if include_lr else RAW_BAR_COMMAND_RE
    normalized = pattern.sub("|", normalized)
    return _delimited_indices(normalized, _bar_spans(normalized))


MATH_CONTENT_PATTERNS = (
    re.compile(r"(?<!\\)\$(?!\$)(.*?)(?<!\\)\$", re.DOTALL),
    re.compile(r"\\\((.*?)\\\)", re.DOTALL),
    re.compile(r"\\\[(.*?)\\\]", re.DOTALL),
)


def find_unbarred_math_indices(text: str) -> list[str]:
    normalized = _decode_index_tokens(text)
    findings: list[str] = []
    for pattern in MATH_CONTENT_PATTERNS:
        for match in pattern.finditer(normalized):
            content = match.group(1)
            if any(token in content for token in (
                r"\exists", r"\forall", r"\text", r"\{", "=", ">", "<", ",", ";"
            )):
                continue
            colons = _top_level_colons(content)
            if len(colons) != 1:
                continue
            for colon in colons:
                left = content[:colon]
                right = content[colon + 1:]
                enclosed = (
                    (re.search(r"\\lvert\b", left) and re.search(r"\\rvert\b", right))
                    or ("|" in left and "|" in right)
                )
                if (
                    not enclosed
                    and _group_expression(left)
                    and _group_expression(right, allow_identity=True)
                ):
                    findings.append(match.group(0))
                    break
    return findings


def markdown_raw_bar_segments(line: str) -> list[str]:
    """Return text regions whose bars are mathematical, not table columns."""

    unescaped_bars = [
        offset for offset, character in enumerate(line)
        if character == "|" and not _escaped(line, offset)
    ]
    if not (line.lstrip().startswith("|") and len(unescaped_bars) >= 3):
        return [line]
    return [
        line[start + 1:end]
        for start, end in zip(unescaped_bars, unescaped_bars[1:])
    ]


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

    notation_text = (
        expand_simple_tex_macros(text)
        if path.suffix.lower() in {".tex", ".md"}
        else text
    )
    require(not find_square_delimited_indices(notation_text),
            f"square-delimited subgroup index in {path}")
    require(not find_textual_indices(notation_text),
            f"unbarred textual subgroup index in {path}")
    require(not find_sized_indices(notation_text),
            f"manually sized subgroup index delimiters in {path}")
    if path.suffix.lower() in {".tex", ".md"}:
        require(not find_unbarred_math_indices(notation_text),
                f"unbarred subgroup index in mathematical text: {path}")

    if path.suffix.lower() == ".tex":
        require(not find_raw_bar_indices(notation_text),
                f"raw-bar subgroup index in LaTeX text: {path}")
    elif path.suffix.lower() == ".md":
        for line in notation_text.splitlines():
            for segment in markdown_raw_bar_segments(line):
                require(not find_raw_bar_indices(segment),
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
    outside = expand_simple_tex_macros(principal[:start] + principal[end:])
    for pattern in disclosure_patterns():
        require(pattern.search(outside) is None,
                "additional disclosure terminology in principal manuscript")
    require(structural_disclosure(outside, PRINCIPAL) is None,
            "additional disclosure terminology in principal manuscript")


def check_rendered_disclosure(rendered: str) -> None:
    """Enforce the same exact-one boundary on text extracted from the PDF."""

    normalized = unicodedata.normalize("NFKC", rendered)
    normalized = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "", normalized)
    normalized = " ".join(normalized.replace("’", "'").split())
    heading = "Gen" + "erative-" + "A" + "I disclosure"
    expected = (
        "Gen" + "erative-" + "A" + "I tools were used for literature search, proof exploration, "
        "code generation, drafting, and critical checking; the author checked and "
        "takes responsibility for the manuscript's arguments, citations, and computations."
    )
    require(normalized.count(heading) == 1,
            "rendered disclosure heading count is not one")
    start = normalized.index(heading)
    body_start = start + len(heading)
    end = normalized.find(" References ", body_start)
    require(end != -1, "rendered disclosure bibliography boundary")
    body = normalized[body_start:end].strip()
    require(body == expected, "rendered disclosure must be the one canonical sentence")
    outside = normalized[:start] + normalized[end:]
    rendered_path = Path("rendered-manuscript.txt")
    for pattern in disclosure_patterns():
        require(pattern.search(outside) is None,
                "additional disclosure terminology in rendered manuscript")
    require(structural_disclosure(outside, rendered_path) is None,
            "additional disclosure terminology in rendered manuscript")


def scan_tree(root: Path, paths: Sequence[Path], label: str) -> None:
    require(len(paths) == len(set(paths)), f"duplicate paths in {label}")
    check_path_policy(paths)
    principal = ""
    rendered = ""
    scanned = 0
    for path in paths:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            text = extract_pdf(root, path)
            check_text(path, text, rendered_manuscript=(path == RENDERED))
            if path == RENDERED:
                rendered = text
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
    if RENDERED in paths:
        require(rendered != "", f"rendered manuscript missing from {label}")
        check_rendered_disclosure(rendered)
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
