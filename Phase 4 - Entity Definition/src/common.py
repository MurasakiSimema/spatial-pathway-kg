"""Shared paths and normalization rules for the data layer (Phase 2, Stage 2B)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "Phase 4 - Entity Definition" / "data" / "raw"
PROCESSED = ROOT / "Phase 4 - Entity Definition" / "data" / "processed"

MSIGDB_FILE = RAW / "h.all.v2026.2.Hs.symbols.gmt"
CELLMARKER_FILE = RAW / "human_cell_marker.txt"
HGNC_FILE = RAW / "hgnc_complete_set.txt"
MONDO_FILE = RAW / "mondo.owl"

HGNC_ID_RE = re.compile(r"^HGNC:\d+$")


def normalize_symbol(s):
    """The one matching key for gene symbols: trim, then uppercase.

    Used for MSigDB, CellMarker, HGNC symbols and query inputs alike. It is only a
    comparison key: the original spelling is always kept separately.
    """
    return (s or "").strip().upper()


def is_valid_symbol(s):
    """A symbol is malformed if it is blank or contains whitespace after trimming."""
    s = (s or "").strip()
    return bool(s) and not re.search(r"\s", s)


def is_valid_hgnc_id(s):
    return bool(HGNC_ID_RE.match(s or ""))


def split_pipe(s):
    """HGNC list fields: optional surrounding double quotes, values separated by '|'."""
    s = (s or "").strip().strip('"')
    return [x.strip() for x in s.split("|") if x.strip()] if s else []
