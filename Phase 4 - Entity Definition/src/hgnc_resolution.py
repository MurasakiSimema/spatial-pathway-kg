"""HGNC symbol resolution for the gene symbols of MSigDB Hallmark and CellMarker.

Statuses (one per distinct source symbol):
  resolved            exactly one Approved HGNC entry has this symbol (normalized)
  not_found           no HGNC entry has it as approved, previous or alias symbol
  non_approved_match  no approved-symbol match, but it is a previous/alias symbol of
                      one or more entries (candidates listed, NOT resolved)
  ambiguous           more than one Approved entry has this normalized symbol
  invalid             blank or malformed symbol

Project decisions applied on top of the statuses (Phase 2, 03_data_layer.md):
  D19  mouse-style symbols whose CellMarker gene_id is not the human Entrez ID stay resolved,
       flagged with gene_id_conflict in the audit table;
  D20  a non_approved_match with exactly one candidate is resolved to it, with
       resolution_method = prev_or_alias (otherwise approved_symbol);
  D21  only genes with an HGNC ID enter the KG (in_kg = yes); all others are audit-only.

Writes data/processed/gene_symbol_resolution.csv.
Run:  python "Phase 4 - Entity Definition/src/hgnc_resolution.py"
"""
import csv
import sys
from collections import Counter, defaultdict

from common import (CELLMARKER_FILE, HGNC_FILE, MSIGDB_FILE, PROCESSED, is_valid_hgnc_id,
                    is_valid_symbol, normalize_symbol, split_pipe)

csv.field_size_limit(sys.maxsize if sys.maxsize < 2**31 else 2**31 - 1)


class HGNCResolver:
    def __init__(self, rows):
        """rows: iterable of dicts with hgnc_id, symbol, name, status, prev_symbol, alias_symbol."""
        self.approved = defaultdict(list)   # normalized approved symbol -> [row]
        self.other = defaultdict(set)       # normalized prev/alias symbol -> {hgnc_id}
        self.entrez = {}                    # hgnc_id -> entrez_id
        self.by_id = {}                     # hgnc_id -> row
        self.bad_ids = []
        self.statuses = Counter()
        for r in rows:
            self.statuses[r["status"]] += 1
            if not is_valid_hgnc_id(r["hgnc_id"]):
                self.bad_ids.append(r["hgnc_id"])
                continue
            self.entrez[r["hgnc_id"]] = (r.get("entrez_id") or "").strip()
            self.by_id[r["hgnc_id"]] = r
            if r["status"] == "Approved":
                self.approved[normalize_symbol(r["symbol"])].append(r)
            else:  # e.g. withdrawn entries, if any: only as candidates
                self.other[normalize_symbol(r["symbol"])].add(r["hgnc_id"])
            for s in split_pipe(r.get("prev_symbol")) + split_pipe(r.get("alias_symbol")):
                self.other[normalize_symbol(s)].add(r["hgnc_id"])

    @classmethod
    def from_file(cls, path=HGNC_FILE):
        with open(path, encoding="utf-8", newline="") as f:
            return cls(csv.DictReader(f, delimiter="\t"))

    def resolve(self, symbol):
        """Return dict(status, hgnc_id, approved_symbol, approved_name, candidates, warning)."""
        out = dict(status="", hgnc_id="", approved_symbol="", approved_name="", candidates="", warning="")
        if not is_valid_symbol(symbol):
            out["status"] = "invalid"
            return out
        key = normalize_symbol(symbol)
        hits = self.approved.get(key, [])
        if len(hits) == 1:
            r = hits[0]
            out.update(status="resolved", hgnc_id=r["hgnc_id"], approved_symbol=r["symbol"],
                       approved_name=r["name"])
            others = self.other.get(key, set()) - {r["hgnc_id"]}
            if others:
                out["warning"] = "also_prev_or_alias_of:" + "|".join(sorted(others))
        elif len(hits) > 1:
            out.update(status="ambiguous", candidates="|".join(sorted(h["hgnc_id"] for h in hits)))
        elif key in self.other:
            out.update(status="non_approved_match", candidates="|".join(sorted(self.other[key])))
        else:
            out["status"] = "not_found"
        return out


def apply_policy(r, hgnc_rows):
    """Add resolution_method and in_kg to a resolve() result (decisions D20, D21)."""
    r = dict(r)
    r["resolution_method"] = ""
    if r["status"] == "resolved":
        r["resolution_method"] = "approved_symbol"
    elif r["status"] == "non_approved_match" and "|" not in r["candidates"]:
        h = hgnc_rows[r["candidates"]]
        r.update(status="resolved", hgnc_id=h["hgnc_id"], approved_symbol=h["symbol"],
                 approved_name=h["name"], resolution_method="prev_or_alias")
    r["in_kg"] = "yes" if r["status"] == "resolved" else "no"
    return r


def msigdb_symbols(path=MSIGDB_FILE):
    """Counter of original gene symbols (fields 3+ of every GMT line)."""
    c = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            for s in parts[2:]:
                c[s] += 1
    return c


def cellmarker_symbols(path=CELLMARKER_FILE):
    """Counter of (source column, original symbol): `symbol` when filled, else `marker`.

    Also collects the CellMarker gene_id per symbol, to check it against HGNC's entrez_id."""
    c = Counter()
    gene_ids = defaultdict(set)
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["symbol"].strip():
                key = ("symbol", r["symbol"])
            else:
                key = ("marker", r["marker"])
            c[key] += 1
            gid = (r.get("gene_id") or "").strip()
            if gid:
                gene_ids[key].add(gid)
    return c, gene_ids


def main():
    res = HGNCResolver.from_file()
    print("HGNC status values:", dict(res.statuses), "| malformed HGNC IDs:", len(res.bad_ids))
    PROCESSED.mkdir(parents=True, exist_ok=True)
    out_rows = []
    ms = msigdb_symbols()
    for s, n in sorted(ms.items()):
        out_rows.append(dict(source="MSigDB Hallmark", source_column="gene", original_symbol=s,
                             normalized_symbol=normalize_symbol(s), records=n, source_gene_id="",
                             **apply_policy(res.resolve(s), res.by_id)))
    cm, gids = cellmarker_symbols()
    for (col, s), n in sorted(cm.items()):
        r = apply_policy(res.resolve(s), res.by_id)
        gid = "|".join(sorted(gids.get((col, s), [])))
        if r["status"] == "resolved" and gid:
            hgnc_entrez = res.entrez.get(r["hgnc_id"], "")
            cm_ids = {g.split(".")[0] for g in gid.split("|")}
            if hgnc_entrez and hgnc_entrez not in cm_ids:
                r["warning"] = (r["warning"] + ";" if r["warning"] else "") + \
                    f"gene_id_conflict:cellmarker={gid}/hgnc_entrez={hgnc_entrez}"
        out_rows.append(dict(source="CellMarker 3.0", source_column=col, original_symbol=s,
                             normalized_symbol=normalize_symbol(s), records=n, source_gene_id=gid, **r))
    cols = ["source", "source_column", "original_symbol", "normalized_symbol", "records", "status",
            "resolution_method", "in_kg", "hgnc_id", "approved_symbol", "approved_name", "candidates",
            "warning", "source_gene_id"]
    path = PROCESSED / "gene_symbol_resolution.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)
    print("written:", path, len(out_rows), "rows")
    for src in ("MSigDB Hallmark", "CellMarker 3.0"):
        rows = [r for r in out_rows if r["source"] == src]
        sym = Counter(r["status"] for r in rows)
        rec = Counter()
        for r in rows:
            rec[r["status"]] += int(r["records"])
        print(f"\n{src}: {len(rows)} distinct symbols, {sum(rec.values())} occurrences")
        for st in ("resolved", "non_approved_match", "ambiguous", "not_found", "invalid"):
            print(f"  {st:20s} symbols {sym[st]:8d}   occurrences {rec[st]:9d}")
        print("  resolved via prev/alias (D20): symbols", sum(r["resolution_method"] == "prev_or_alias" for r in rows),
              "occurrences", sum(int(r["records"]) for r in rows if r["resolution_method"] == "prev_or_alias"))
        print("  in KG (D21): symbols", sum(r["in_kg"] == "yes" for r in rows),
              "occurrences", sum(int(r["records"]) for r in rows if r["in_kg"] == "yes"))
        print("  gene_id_conflict (D19): symbols", sum("gene_id_conflict" in r["warning"] for r in rows),
              "occurrences", sum(int(r["records"]) for r in rows if "gene_id_conflict" in r["warning"]))
        print("  also_prev_or_alias_of warning: symbols", sum("also_prev_or_alias_of" in r["warning"] for r in rows))


if __name__ == "__main__":
    main()
