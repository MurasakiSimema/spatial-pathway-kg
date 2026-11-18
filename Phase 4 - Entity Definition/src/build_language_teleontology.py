"""Build the Phase 2 language teleontology (Turtle) from the Language Resource Table.

Run from anywhere:  python "Phase 4 - Entity Definition/src/build_language_teleontology.py"
"""
import csv
import pathlib

D = pathlib.Path(__file__).resolve().parents[2] / "Phase 2 - Language Definition"
rows = [r for r in csv.DictReader(open(D / "language_resource_table.csv", encoding="utf-8"))
        if r["finally_considered"] == "yes" and r["final_term"].startswith("tpkg:")]


def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"@en'


def short_id(cid):
    """Short form of a concept ID for the comment, e.g. RO:0002607, EDAM:data_2298."""
    for pre, rep in (("http://purl.obolibrary.org/obo/", ""), ("http://edamontology.org/", "EDAM:"),
                     ("http://www.ebi.ac.uk/efo/", "")):
        if cid.startswith(pre):
            x = cid[len(pre):]
            if pre.endswith("obo/") or pre.endswith("efo/"):
                x = x.replace("_", ":", 1)
            return rep + x
    return cid


out = ["""@prefix tpkg: <http://knowdive.disi.unitn.it/etype#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

# Language teleontology of the Transcriptomics Pathways KG (Phase 2, Language Definition).
# Generated from language_resource_table.csv. It contains only the language terms:
# no instances and no knowledge modelling (Phase 3).
# rdfs:label is reused as it is (W3C RDF Schema) for Pathway and Disease labels.

<http://knowdive.disi.unitn.it/etype> a owl:Ontology ;
    rdfs:label "Transcriptomics Pathways KG - language teleontology"@en ;
    dcterms:created "2026-11-18"^^xsd:date .
"""]

kinds = {"EType": "owl:Class", "object property": "owl:ObjectProperty", "data property": "owl:DatatypeProperty"}
titles = {"EType": "Entity types", "object property": "Object properties", "data property": "Data properties"}
for kind in ("EType", "object property", "data property"):
    out.append(f"\n#################### {titles[kind]}\n")
    for r in rows:
        if r["kind"] != kind:
            continue
        t = [f"{r['final_term']} a {kinds[kind]}",
             f"    rdfs:label {lit(r['word_en'])}",
             f"    rdfs:comment {lit(r['gloss_en'] + ' (' + short_id(r['concept_id']) + ')')}"]
        if r["concept_id"].startswith("http"):
            t.append(f"    rdfs:seeAlso <{r['concept_id']}>")
        if r["domain"]:
            t.append(f"    rdfs:domain {r['domain']}")
        if r["range"]:
            t.append(f"    rdfs:range {r['range']}")
        if "subPropertyOf tpkg:isMarkerFor" in r["notes"]:
            t.append("    rdfs:subPropertyOf tpkg:isMarkerFor")
        out.append(" ;\n".join(t) + " .\n")

(D / "tpkg_language_teleontology.ttl").write_text("\n".join(out), encoding="utf-8", newline="\n")
print(len(rows), "terms written to", D / "tpkg_language_teleontology.ttl")
