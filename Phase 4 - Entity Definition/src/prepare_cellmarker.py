"""Filter, clean and format CellMarker 3.0 (Phase 2, Stage 2B).

Needs data/processed/gene_symbol_resolution.csv (run hgnc_resolution.py first).
Rules:
  - human records only (the file labels every record Human; checked, not assumed);
  - exact duplicate rows are collapsed and counted (decision D3);
  - gene = `symbol` when filled, else `marker`; only genes with an HGNC ID enter (D21);
  - CellType key = (cellName, tissueClass, diseaseCategory) (Phase 1, D5);
  - cellOntologyId: `CL:nnnnnnn` -> `CL_nnnnnnn`; other values are treated as missing and logged;
  - a gene-cell type link is "reported" if at least one of its records has
    marker_source != Method, otherwise "predicted" (D17);
  - a CellType enters the KG only if it has at least one marker link with a KG gene (D22):
    inKg = yes/no in cell_types.csv and cell_type_disease_source.csv.
Outputs (column names = language terms of the LRT; multi-valued fields joined with "|"):
  cell_types.csv              cellName, tissueClass, diseaseCategory, tissueType, cellNameClass,
                              cellOntologyId, records, markerLinks, inKg
  cell_type_gene.csv          hgncId, cellName, tissueClass, diseaseCategory, markerKind, records
  cell_type_disease_source.csv  cellName, tissueClass, diseaseCategory, sourceDiseaseName, records, inKg
  cellmarker_excluded_cl_ids.csv  the cellontology_id values treated as missing

Run:  python "Phase 4 - Entity Definition/src/prepare_cellmarker.py"
"""
import csv
import hashlib
import re
from collections import Counter, defaultdict

from common import CELLMARKER_FILE, PROCESSED

csv.field_size_limit(2**31 - 1)


def clean_cl_id(v):
    """Return (clean id or '', problem or '')."""
    v = (v or "").strip()
    if not v:
        return "", ""
    if re.fullmatch(r"CL_\d{7}", v):
        return v, ""
    if re.fullmatch(r"CL:\d{7}", v):
        return v.replace(":", "_"), ""
    return "", v


def load_resolution():
    res = {}
    with open(PROCESSED / "gene_symbol_resolution.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["source"] == "CellMarker 3.0":
                res[(r["source_column"], r["original_symbol"])] = r
    return res


def main():
    res = load_resolution()
    seen = set()
    c = Counter()
    ct = {}                                   # key -> dict of sets/counters
    links = defaultdict(lambda: [0, False])   # (hgnc, key) -> [records, reported]
    dis = Counter()                           # (key, disease) -> records
    bad_cl = Counter()
    with open(CELLMARKER_FILE, encoding="utf-8", newline="") as f:
        rd = csv.reader(f, delimiter="\t")
        h = next(rd)
        ix = {name: i for i, name in enumerate(h)}
        for row in rd:
            c["raw records"] += 1
            digest = hashlib.md5("\t".join(row).encode("utf-8")).digest()
            if digest in seen:
                c["exact duplicate rows collapsed (D3)"] += 1
                continue
            seen.add(digest)
            g = lambda col: row[ix[col]].strip()  # noqa: E731
            if g("species") != "Human":
                c["non-human records excluded"] += 1
                continue
            c["distinct records"] += 1
            key = (g("cell_name"), g("tissue_class"), g("disease_category"))
            d = ct.get(key)
            if d is None:
                d = ct[key] = dict(tissueType=set(), cellNameClass=set(), cellOntologyId=set(), records=0)
            d["records"] += 1
            if g("tissue_type"):
                d["tissueType"].add(g("tissue_type"))
            if g("cell_name_class"):
                d["cellNameClass"].add(g("cell_name_class"))
            cl, problem = clean_cl_id(row[ix["cellontology_id"]])
            if cl:
                d["cellOntologyId"].add(cl)
            if problem:
                bad_cl[problem] += 1
            if key[2] != "Normal" and g("disease"):
                dis[(key, g("disease"))] += 1
            col, sym = ("symbol", row[ix["symbol"]]) if g("symbol") else ("marker", row[ix["marker"]])
            r = res[(col, sym)]
            if r["in_kg"] != "yes":
                c["distinct records whose gene is not in the KG (D21)"] += 1
                continue
            c["distinct records with a KG gene"] += 1
            link = links[(r["hgnc_id"], key)]
            link[0] += 1
            if g("marker_source") != "Method":
                link[1] = True

    PROCESSED.mkdir(parents=True, exist_ok=True)
    nlinks = Counter(k for (_, k) in links)

    def write(name, cols, rows):
        with open(PROCESSED / name, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)

    write("cell_types.csv", ["cellName", "tissueClass", "diseaseCategory", "tissueType", "cellNameClass",
                             "cellOntologyId", "records", "markerLinks", "inKg"],
          [[*k, "|".join(sorted(d["tissueType"])), "|".join(sorted(d["cellNameClass"])),
            "|".join(sorted(d["cellOntologyId"])), d["records"], nlinks.get(k, 0),
            "yes" if nlinks.get(k, 0) else "no"]
           for k, d in sorted(ct.items())])
    write("cell_type_gene.csv", ["hgncId", "cellName", "tissueClass", "diseaseCategory", "markerKind", "records"],
          [[hg, *k, "reported" if rep else "predicted", n] for (hg, k), (n, rep) in sorted(links.items())])
    write("cell_type_disease_source.csv", ["cellName", "tissueClass", "diseaseCategory", "sourceDiseaseName", "records", "inKg"],
          [[*k, dname, n, "yes" if nlinks.get(k, 0) else "no"] for (k, dname), n in sorted(dis.items())])
    write("cellmarker_excluded_cl_ids.csv", ["cellontology_id", "records"], sorted(bad_cl.items()))

    for k, v in c.items():
        print(f"{k}: {v}")
    print("CellTypes:", len(ct), "| without any marker link in the KG:", sum(1 for k in ct if nlinks.get(k, 0) == 0))
    print("CellTypes with >1 cellNameClass:", sum(1 for d in ct.values() if len(d["cellNameClass"]) > 1))
    kinds = Counter("reported" if rep else "predicted" for (n, rep) in links.values())
    print("isMarkerFor links:", len(links), dict(kinds))
    print("genes with at least one marker link:", len({hg for (hg, _) in links}))
    print("cellontology_id values treated as missing:", sum(bad_cl.values()), "records,", len(bad_cl), "distinct")
    print("(CellType, disease string) pairs, non-Normal:", len(dis),
          "| distinct disease strings:", len({dn for (_, dn) in dis}))
    kept = [(k, dn) for (k, dn) in dis if nlinks.get(k, 0)]
    print("  of which with a KG CellType (D22):", len(kept), "pairs,", len({dn for (_, dn) in kept}), "strings")


if __name__ == "__main__":
    main()
