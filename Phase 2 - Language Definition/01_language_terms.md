# 1. Fixing the language terms

*Status: terms fixed on 2026-11-18. Concept alignment is in
`02_concept_alignment.md`. The machine-readable version is
[`language_resource_table.csv`](language_resource_table.csv).*

We started from every term of Phase 1 (`05_concept_identification.md`, `06_er_model.md`) and
gave each one its final English name, following decision L3 of `00_decisions.md`: classes in
UpperCamelCase, properties in lowerCamelCase, all in the `tpkg:` namespace.

## 1.1 Entity types

| Phase 1 term | Final term | Word (en) |
|---|---|---|
| Gene | `tpkg:Gene` | gene |
| Pathway | `tpkg:Pathway` | pathway |
| CellType | `tpkg:CellType` | cell type |
| Disease | `tpkg:Disease` | disease |

## 1.2 Object properties

| Phase 1 term | Final term | Domain → Range | Note |
|---|---|---|---|
| participates in | `tpkg:participatesIn` | Gene → Pathway | |
| is marker for | `tpkg:isMarkerFor` | Gene → CellType | |
| is reported marker for | `tpkg:isReportedMarkerFor` | Gene → CellType | sub-property of `isMarkerFor` (D17) |
| is predicted marker for | `tpkg:isPredictedMarkerFor` | Gene → CellType | sub-property of `isMarkerFor` (D17) |
| observed in | `tpkg:observedIn` | CellType → Disease | |

## 1.3 Data properties

| EType | Phase 1 term | Final term | Change |
|---|---|---|---|
| Gene | HGNC ID | `tpkg:hgncId` | |
| Gene | approved symbol | `tpkg:approvedSymbol` | |
| Gene | approved name | `tpkg:approvedName` | |
| Gene | source symbol(s) | `tpkg:sourceSymbol` | singular (see below) |
| Gene | resolution status | `tpkg:hgncResolutionMethod` | renamed (twice, see below) |
| Pathway | Hallmark identifier | `tpkg:hallmarkId` | |
| Pathway | label | `rdfs:label` | merged (see below) |
| Pathway | source URL | `tpkg:sourceUrl` | |
| CellType | cell name | `tpkg:cellName` | |
| CellType | tissue class | `tpkg:tissueClass` | |
| CellType | disease category | `tpkg:diseaseCategory` | |
| CellType | tissue type | `tpkg:tissueType` | |
| CellType | cell name class | `tpkg:cellNameClass` | |
| CellType | Cell Ontology ID | `tpkg:cellOntologyId` | |
| Disease | MONDO ID | `tpkg:mondoId` | |
| Disease | label | `rdfs:label` | merged (see below) |
| Disease | source strings | `tpkg:sourceDiseaseName` | renamed, singular |

The four evidence attributes of *is marker for* (marker source, method details, PubMed ID,
publication year) were already removed in Phase 1 (D16). They are kept in the table as
"not finally considered", so that the counts start from all the terms of Phase 1.

## 1.4 Changes and why

- **One label for all.** Pathway and Disease both had a "label". Instead of a new term we use
  the standard `rdfs:label`, which is already the usual way to give a resource a readable name.
- **Singular names for multi-valued properties** (`sourceSymbol`, `sourceDiseaseName`). In RDF
  every triple has one value, so a gene with three source symbols has three
  `tpkg:sourceSymbol` triples; each one reads "has source symbol X". This is the usual
  convention (e.g. `rdf:type`, `skos:altLabel`). Whether a property can have more than one
  value is not in its name: it is multi-valued unless it is declared functional.
- **`hgncResolutionMethod`** instead of "resolution status". It was first renamed
  `hgncResolutionStatus`; after decision D21 (only resolved genes enter the KG, `03_data_layer.md`)
  its only values are the method of resolution (approved symbol, or a unique previous/alias
  symbol), so it was renamed again and its gloss changed.
- **`sourceDiseaseName`** instead of "source strings": the values are the disease names as
  CellMarker writes them; "strings" only described the data type.

## 1.5 Counts so far

| | Initially considered | Finally considered |
|---|---|---|
| Entity types | 4 | 4 |
| Object properties | 5 | 5 |
| Data properties | 21 (17 + 4 removed in D16) | 16 (two labels merged into `rdfs:label`) |

The number of terms aligned to the Language Teleontology is in `02_concept_alignment.md`.
