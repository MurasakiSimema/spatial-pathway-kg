"""Check the Phase 2 language teleontology: Turtle syntax (rdflib), label/comment/domain/range
of every term, the sub-properties of isMarkerFor, and agreement with the Language Resource Table.

Run from anywhere:  python "Phase 4 - Entity Definition/src/validate_language_teleontology.py"
Exit code 0 if no error is found.
"""
import csv
import pathlib
import sys

from rdflib import OWL, RDF, RDFS, Graph, Namespace

D = pathlib.Path(__file__).resolve().parents[2] / "Phase 2 - Language Definition"
T = Namespace("http://knowdive.disi.unitn.it/etype#")

g = Graph()
g.parse(D / "tpkg_language_teleontology.ttl", format="turtle")
print("triples:", len(g))

errors = []
kinds = {OWL.Class: "EType", OWL.ObjectProperty: "object property", OWL.DatatypeProperty: "data property"}
found = {}
for k, name in kinds.items():
    subs = sorted(str(s) for s in g.subjects(RDF.type, k))
    found[name] = subs
    print(name, len(subs))
    for s in g.subjects(RDF.type, k):
        labels = list(g.objects(s, RDFS.label))
        comments = list(g.objects(s, RDFS.comment))
        if len(labels) != 1 or labels[0].language != "en":
            errors.append(f"{s}: label")
        if len(comments) != 1 or not str(comments[0]).rstrip().endswith(")"):
            errors.append(f"{s}: comment without concept ID")
        if k != OWL.Class:
            if len(list(g.objects(s, RDFS.domain))) != 1:
                errors.append(f"{s}: domain")
            if len(list(g.objects(s, RDFS.range))) != 1:
                errors.append(f"{s}: range")
            for d in g.objects(s, RDFS.domain):
                if (d, RDF.type, OWL.Class) not in g:
                    errors.append(f"{s}: domain {d} is not a declared class")
            if k == OWL.ObjectProperty:
                for r in g.objects(s, RDFS.range):
                    if (r, RDF.type, OWL.Class) not in g:
                        errors.append(f"{s}: range {r} is not a declared class")

subs = set(g.subjects(RDFS.subPropertyOf, T.isMarkerFor))
if subs != {T.isReportedMarkerFor, T.isPredictedMarkerFor}:
    errors.append(f"sub-properties of isMarkerFor: {subs}")

rows = [r for r in csv.DictReader(open(D / "language_resource_table.csv", encoding="utf-8"))
        if r["finally_considered"] == "yes" and r["final_term"].startswith("tpkg:")]
for r in rows:
    iri = T[r["final_term"].split(":", 1)[1]]
    if str(iri) not in found[r["kind"]]:
        errors.append(f"missing in the Turtle file: {r['final_term']}")
    cid = r["concept_id"].split("/")[-1].replace("_", ":")
    if cid not in str(g.value(iri, RDFS.comment)).replace("_", ":"):
        errors.append(f"concept ID not in comment: {r['final_term']}")
print("LRT terms checked:", len(rows))
print("errors:", errors or "none")
sys.exit(1 if errors else 0)
