"""Match the CellMarker disease strings to MONDO (Phase 2, Stage 2B; Phase 1 decisions D9, D13-D15).

Rules
  - Only strings with disease_category != Normal, of CellTypes in the KG (D22).
  - Values in NON_DISEASE are not diseases: status non_disease, no Disease, no link (D14, D26).
  - MONDO terms under "non-human animal disease" (MONDO:0005583) are not used (D24).
  - Strings in REJECTED_MERGES are not resolved even if they match (D25).
  - Normalization (same for both sides): lower case, "tumour" -> "tumor", possessive "'s"
    removed, "- _ , /" -> space, repeated spaces collapsed.
  - Names used for matching: rdfs:label and oboInOwl:hasExactSynonym of non-obsolete MONDO
    classes, EXCEPT exact synonyms typed ABBREVIATION, AMBIGUOUS, DUBIOUS, DEPRECATED or
    NON_HUMAN (an abbreviation alone is never used, D9).
  - resolved: exactly one MONDO term on the full string, else on the string without its final
    parenthesised part. ambiguous: more than one term. related_only: only a RELATED / NARROW /
    BROAD synonym matches (candidate written, not resolved). no_match otherwise.
  - Only resolved strings give a Disease and observedIn links (D15). Metastases are not merged
    into the primary disease (D13); they are flagged in the audit table.
Outputs (data/processed/)
  disease_mondo_matching.csv  one row per disease string (audit)
  diseases.csv                mondoId, label, sourceDiseaseName ("|"), cellTypes
  cell_type_disease.csv       cellName, tissueClass, diseaseCategory, mondoId (observedIn)
  mondo_merges.csv            MONDO terms reached by more than one string (to review)

Run:  python "Phase 4 - Entity Definition/src/mondo_matching.py"
"""
import csv
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

from common import MONDO_FILE, PROCESSED

# D14: values that are not diseases (5 from Phase 1, completed with the user on 2026-11-18, D26)
NON_DISEASE = {
    "Undefined", "Pan-cancer", "SARS-CoV-2 vaccine", "Mild fibrosis", "Hepatitis C virus",
    # ageing
    "Aging", "Healthy brain aging", "Skin aging", "Skeletal muscle aging", "Vascular ageing",
    # exposures
    "Arsenic exposure", "Human papillomavirus exposure",
    # viruses as organisms
    "Ebola virus", "Human immunodeficiency virus", "Human immunodeficiency virus-1",
    "Human papillomaviruses (HPV)", "Herpes simplex virus type 2", "Herpes simplex virus type 3",
    "Herpes simplex virus type 4", "SARS-CoV-2", "Respiratory viruses",
    # procedures
    "Heart transplantation", "Kidney transplantation", "Liver transplantation", "Lung transplantation",
    "Liver xenotransplantation", "Pig-to-human kidney xenotransplantation",
    # studies and states
    "Ebola vaccine study", "Spontaneous HIV-1 controller", "Viral infection susceptibility",
}

# D25: merges rejected after review (the string is broader than the MONDO term it reaches)
REJECTED_MERGES = {"Primary antibody deficiency", "Lewy body disease", "Intervertebral disc disease"}

# D24: MONDO terms of non-human animals are not used (CellMarker is human only)
NON_HUMAN_ROOT = "MONDO:0005583"

NS = dict(rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#", rdfs="http://www.w3.org/2000/01/rdf-schema#",
          owl="http://www.w3.org/2002/07/owl#", oio="http://www.geneontology.org/formats/oboInOwl#")
RDF_ABOUT = f"{{{NS['rdf']}}}about"
RDF_RES = f"{{{NS['rdf']}}}resource"
MONDO_PREFIX = "http://purl.obolibrary.org/obo/MONDO_"
EXCLUDED_TYPES = {"ABBREVIATION", "AMBIGUOUS", "DUBIOUS", "DEPRECATED", "NON_HUMAN"}


def normalize(s):
    s = (s or "").lower().replace("tumour", "tumor")
    s = re.sub(r"'s\b", "", s)
    s = re.sub(r"[-_,/]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def strip_final_parentheses(s):
    return re.sub(r"\s*\([^()]*\)\s*$", "", s).strip()


def is_metastasis(s):
    return "metasta" in s.lower()


def load_mondo(path=MONDO_FILE):
    """Return (terms, excluded_synonyms): terms[mondo_id] = dict(label, exact, other, deprecated)."""
    terms = {}
    syn_type = defaultdict(set)   # (mondo_id, synonym text) -> types, from owl:Axiom
    for _, el in ET.iterparse(path, events=("end",)):
        tag = el.tag
        if tag == f"{{{NS['owl']}}}Class":
            about = el.get(RDF_ABOUT, "")
            if about.startswith(MONDO_PREFIX):
                mid = "MONDO:" + about[len(MONDO_PREFIX):]
                t = terms.setdefault(mid, dict(label="", exact=set(), other=set(), deprecated=False, parents=set()))
                for ch in el:
                    if ch.tag == f"{{{NS['rdfs']}}}label" and ch.text:
                        t["label"] = ch.text
                    elif ch.tag == f"{{{NS['oio']}}}hasExactSynonym" and ch.text:
                        t["exact"].add(ch.text)
                    elif ch.tag in (f"{{{NS['oio']}}}hasRelatedSynonym", f"{{{NS['oio']}}}hasNarrowSynonym",
                                    f"{{{NS['oio']}}}hasBroadSynonym") and ch.text:
                        t["other"].add(ch.text)
                    elif ch.tag == f"{{{NS['owl']}}}deprecated" and (ch.text or "").strip() == "true":
                        t["deprecated"] = True
                    elif ch.tag == f"{{{NS['rdfs']}}}subClassOf" and ch.get(RDF_RES, "").startswith(MONDO_PREFIX):
                        t["parents"].add("MONDO:" + ch.get(RDF_RES)[len(MONDO_PREFIX):])
            el.clear()
        elif tag == f"{{{NS['owl']}}}Axiom":
            src = el.find("owl:annotatedSource", NS)
            prop = el.find("owl:annotatedProperty", NS)
            tgt = el.find("owl:annotatedTarget", NS)
            if src is not None and prop is not None and tgt is not None and tgt.text \
                    and prop.get(RDF_RES, "").endswith("#hasExactSynonym") \
                    and src.get(RDF_RES, "").startswith(MONDO_PREFIX):
                mid = "MONDO:" + src.get(RDF_RES)[len(MONDO_PREFIX):]
                for st in el.findall("oio:hasSynonymType", NS):
                    syn_type[(mid, tgt.text)].add(st.get(RDF_RES, "").rsplit("#", 1)[-1])
            el.clear()
    excluded = 0
    for (mid, text), types in syn_type.items():
        if types & EXCLUDED_TYPES and mid in terms and text in terms[mid]["exact"]:
            terms[mid]["exact"].discard(text)
            excluded += 1
    return terms, excluded


def descendants(terms, root):
    children = defaultdict(set)
    for mid, t in terms.items():
        for p in t.get("parents", ()):
            children[p].add(mid)
    out, todo = {root}, [root]
    while todo:
        for c in children[todo.pop()]:
            if c not in out:
                out.add(c)
                todo.append(c)
    return out


class MondoIndex:
    def __init__(self, terms, skip=frozenset()):
        self.terms = terms
        self.names = defaultdict(set)    # normalized label / exact synonym -> {mondo_id}
        self.other = defaultdict(set)    # normalized related/narrow/broad synonym -> {mondo_id}
        for mid, t in terms.items():
            if t["deprecated"] or mid in skip:
                continue
            for n in {t["label"], *t["exact"]}:
                if n:
                    self.names[normalize(n)].add(mid)
            for n in t["other"]:
                self.other[normalize(n)].add(mid)

    def match(self, s):
        """Return dict(status, mondoId, matchedOn, candidates)."""
        full = normalize(s)
        tries = [("full string", full)]
        stripped = normalize(strip_final_parentheses(s))
        if stripped and stripped != full:
            tries.append(("without final parentheses", stripped))
        for how, key in tries:
            hits = self.names.get(key, set())
            if len(hits) == 1:
                return dict(status="resolved", mondoId=next(iter(hits)), matchedOn=how, candidates="")
            if len(hits) > 1:
                return dict(status="ambiguous", mondoId="", matchedOn=how, candidates="|".join(sorted(hits)))
        for how, key in tries:
            hits = self.other.get(key, set())
            if hits:
                return dict(status="related_only", mondoId="", matchedOn=how, candidates="|".join(sorted(hits)))
        return dict(status="no_match", mondoId="", matchedOn="", candidates="")


def main():
    terms, excluded = load_mondo()
    active = sum(1 for t in terms.values() if not t["deprecated"])
    print(f"MONDO classes: {len(terms)} ({active} not obsolete); exact synonyms excluded by type: {excluded}")
    non_human = descendants(terms, NON_HUMAN_ROOT)
    print("non-human animal disease terms excluded (D24):", len(non_human))
    idx = MondoIndex(terms, skip=non_human)

    pairs = []
    with open(PROCESSED / "cell_type_disease_source.csv", encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r["inKg"] == "yes":
                pairs.append(r)
    records, ctypes = Counter(), defaultdict(set)
    for r in pairs:
        records[r["sourceDiseaseName"]] += int(r["records"])
        ctypes[r["sourceDiseaseName"]].add((r["cellName"], r["tissueClass"], r["diseaseCategory"]))

    audit = {}
    for s in sorted(records):
        if s in NON_DISEASE:
            m = dict(status="non_disease", mondoId="", matchedOn="", candidates="")
        else:
            m = idx.match(s)
            if s in REJECTED_MERGES and m["status"] == "resolved":
                m = dict(status="rejected_merge", mondoId="", matchedOn=m["matchedOn"], candidates=m["mondoId"])
        label = terms[m["mondoId"]]["label"] if m["mondoId"] else ""
        audit[s] = dict(sourceDiseaseName=s, normalized=normalize(s), **m, mondoLabel=label,
                        metastasis="yes" if is_metastasis(s) else "no", records=records[s],
                        cellTypes=len(ctypes[s]))

    PROCESSED.mkdir(parents=True, exist_ok=True)

    def write(name, rows):
        with open(PROCESSED / name, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write("disease_mondo_matching.csv", list(audit.values()))
    by_id = defaultdict(list)
    for a in audit.values():
        if a["status"] == "resolved":
            by_id[a["mondoId"]].append(a["sourceDiseaseName"])
    links = sorted({(r["cellName"], r["tissueClass"], r["diseaseCategory"], audit[r["sourceDiseaseName"]]["mondoId"])
                    for r in pairs if audit[r["sourceDiseaseName"]]["status"] == "resolved"})
    ct_per_dis = Counter(l[3] for l in links)
    write("diseases.csv", [dict(mondoId=mid, label=terms[mid]["label"], sourceDiseaseName="|".join(sorted(ss)),
                                cellTypes=ct_per_dis[mid]) for mid, ss in sorted(by_id.items())])
    write("cell_type_disease.csv", [dict(cellName=a, tissueClass=b, diseaseCategory=c, mondoId=d) for a, b, c, d in links])
    write("mondo_merges.csv", [dict(mondoId=mid, label=terms[mid]["label"], strings=len(ss),
                                    sourceDiseaseName="|".join(sorted(ss)))
                               for mid, ss in sorted(by_id.items()) if len(ss) > 1] or
          [dict(mondoId="", label="", strings=0, sourceDiseaseName="")])

    st, rec = Counter(), Counter()
    for a in audit.values():
        st[a["status"]] += 1
        rec[a["status"]] += a["records"]
    tot = sum(rec.values())
    print(f"disease strings: {len(audit)}, records: {tot}")
    missing = (NON_DISEASE | REJECTED_MERGES) - set(audit)
    if missing:
        print("WARNING: listed strings not found in the data:", sorted(missing))
    for k in ("resolved", "related_only", "ambiguous", "no_match", "non_disease", "rejected_merge"):
        print(f"  {k:13s} strings {st[k]:5d}   records {rec[k]:8d} ({100 * rec[k] / tot:.1f}%)")
    print("  resolved on: ", dict(Counter(a["matchedOn"] for a in audit.values() if a["status"] == "resolved")))
    print("  metastasis strings:", dict(Counter(a["status"] for a in audit.values() if a["metastasis"] == "yes")))
    print("Diseases (MONDO terms):", len(by_id), "| terms reached by >1 string:", sum(len(v) > 1 for v in by_id.values()))
    print("observedIn links:", len(links), "| CellTypes with at least one link:", len({l[:3] for l in links}))
    non_normal = {(r["cellName"], r["tissueClass"], r["diseaseCategory"]) for r in pairs}
    print("non-Normal CellTypes in the KG without any observedIn link:", len(non_normal - {l[:3] for l in links}),
          "of", len(non_normal))


if __name__ == "__main__":
    main()
