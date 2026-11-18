"""Build the Gene table from the resolved symbols of both sources (Phase 2, Stage 2B).

Needs gene_symbol_resolution.csv, pathway_gene.csv and cell_type_gene.csv.
Only genes used by at least one participatesIn or isMarkerFor link are written (D21: all of
them have an HGNC ID).
Output genes.csv: hgncId, approvedSymbol, approvedName, sourceSymbol (all original spellings
in MSigDB and CellMarker, "|"-joined), hgncResolutionMethod, inMsigdb, inCellmarker.
hgncResolutionMethod = approved_symbol if at least one source symbol matched the approved
symbol, otherwise prev_or_alias (D20).

Run:  python "Phase 4 - Entity Definition/src/prepare_genes.py"
"""
import csv
from collections import Counter, defaultdict

from common import PROCESSED


def read(name):
    with open(PROCESSED / name, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    used_ms = {r["hgncId"] for r in read("pathway_gene.csv")}
    used_cm = {r["hgncId"] for r in read("cell_type_gene.csv")}
    info, symbols, methods = {}, defaultdict(set), defaultdict(set)
    for r in read("gene_symbol_resolution.csv"):
        if r["in_kg"] != "yes":
            continue
        hg = r["hgnc_id"]
        if (r["source"] == "MSigDB Hallmark" and hg in used_ms) or (r["source"] == "CellMarker 3.0" and hg in used_cm):
            info[hg] = (r["approved_symbol"], r["approved_name"])
            symbols[hg].add(r["original_symbol"])
            methods[hg].add(r["resolution_method"])
    rows = []
    for hg in sorted(used_ms | used_cm, key=lambda x: int(x.split(":")[1])):
        m = "approved_symbol" if "approved_symbol" in methods[hg] else "prev_or_alias"
        rows.append(dict(hgncId=hg, approvedSymbol=info[hg][0], approvedName=info[hg][1],
                         sourceSymbol="|".join(sorted(symbols[hg])), hgncResolutionMethod=m,
                         inMsigdb="yes" if hg in used_ms else "no", inCellmarker="yes" if hg in used_cm else "no"))
    with open(PROCESSED / "genes.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("genes:", len(rows))
    print("in MSigDB only:", len(used_ms - used_cm), "| CellMarker only:", len(used_cm - used_ms),
          "| shared (same HGNC ID):", len(used_ms & used_cm))
    print("hgncResolutionMethod:", dict(Counter(r["hgncResolutionMethod"] for r in rows)))
    print("genes with more than one source spelling:", sum("|" in r["sourceSymbol"] for r in rows))


if __name__ == "__main__":
    main()
