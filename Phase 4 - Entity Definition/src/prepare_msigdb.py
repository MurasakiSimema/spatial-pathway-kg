"""Filter, clean and format MSigDB Hallmark (Phase 2, Stage 2B).

Needs data/processed/gene_symbol_resolution.csv (run hgnc_resolution.py first).
Outputs (column names = language terms of the LRT):
  pathways.csv      hallmarkId, label, sourceUrl, genesInSource, genesInKg
  pathway_gene.csv  hallmarkId, hgncId, sourceSymbol      (tpkg:participatesIn)
Label rule (decision of 2026-11-18): drop the "HALLMARK_" prefix and turn "_" into spaces,
keeping the source upper case (HALLMARK_TNFA_SIGNALING_VIA_NFKB -> "TNFA SIGNALING VIA NFKB").

Run:  python "Phase 4 - Entity Definition/src/prepare_msigdb.py"
"""
import csv
import re

from common import MSIGDB_FILE, PROCESSED


def pathway_label(hallmark_id):
    return hallmark_id[len("HALLMARK_"):].replace("_", " ") if hallmark_id.startswith("HALLMARK_") else hallmark_id


def load_resolution(source):
    res = {}
    with open(PROCESSED / "gene_symbol_resolution.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["source"] == source:
                res[(r["source_column"], r["original_symbol"])] = r
    return res


def main():
    res = load_resolution("MSigDB Hallmark")
    pathways, links, problems = [], [], []
    with open(MSIGDB_FILE, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                problems.append(f"line {i}: fewer than 3 fields")
                continue
            hid, url, genes = parts[0], parts[1], parts[2:]
            if not re.fullmatch(r"HALLMARK_[A-Z0-9_]+", hid):
                problems.append(f"line {i}: unexpected identifier {hid}")
            if not url.startswith("https://"):
                problems.append(f"line {i}: unexpected URL {url}")
            kept = set()
            for s in genes:
                r = res[("gene", s)]
                if r["in_kg"] == "yes":
                    links.append(dict(hallmarkId=hid, hgncId=r["hgnc_id"], sourceSymbol=s))
                    kept.add(r["hgnc_id"])
            pathways.append(dict(hallmarkId=hid, label=pathway_label(hid), sourceUrl=url,
                                 genesInSource=len(genes), genesInKg=len(kept)))
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for name, rows in (("pathways.csv", pathways), ("pathway_gene.csv", links)):
        with open(PROCESSED / name, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    dup_links = len(links) - len({(l["hallmarkId"], l["hgncId"]) for l in links})
    print(f"pathways: {len(pathways)} | participatesIn links: {len(links)} "
          f"(duplicate pathway-gene pairs after resolution: {dup_links})")
    print("distinct genes in KG:", len({l['hgncId'] for l in links}))
    print("pathway sizes in KG: min", min(p["genesInKg"] for p in pathways), "max", max(p["genesInKg"] for p in pathways))
    print("pathways that lost genes:", [(p["hallmarkId"], p["genesInSource"], p["genesInKg"])
                                        for p in pathways if p["genesInSource"] != p["genesInKg"]])
    print("format problems:", problems or "none")


if __name__ == "__main__":
    main()
