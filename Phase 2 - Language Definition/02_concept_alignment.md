# 2. Concept alignment

*Status: done on 2026-11-18. Full details (glosses, parent
concepts, sources, notes) are in [`language_resource_table.csv`](language_resource_table.csv).*

Each term of `01_language_terms.md` was aligned following decision L1 of `00_decisions.md`:
first the UKC, then the biomedical ontologies (read through EBI OLS), and a new concept with a
`TPKG26-nn` ID only when nothing fitted. Ontology versions used: NCIt 26.02d (2026-03-19),
EFO v3.96.0, Relation Ontology 2026-09-04, EDAM 1.25 (2026-06-26).

## 2.1 Entity types

| Term | Concept | Resource | Parent |
|---|---|---|---|
| `tpkg:Gene` | UKC-29340 *gene* | UKC | UKC-44849 *sequence* |
| `tpkg:Pathway` | NCIT:C54214 *Pathway* | NCIt | NCIT:C19896 |
| `tpkg:CellType` | EFO:0000324 *cell type* | EFO | BFO:0000040 *material entity* |
| `tpkg:Disease` | UKC-67092 *disease* | UKC | UKC-67044 *illness* |

## 2.2 Object properties

| Term | Concept | Resource | Parent |
|---|---|---|---|
| `tpkg:participatesIn` | RO:0000056 *participates in* | RO | — |
| `tpkg:isMarkerFor` | RO:0002607 *is marker for* | RO | RO:0002610 *correlated with* |
| `tpkg:isReportedMarkerFor` | **TPKG26-01** (new) | project | `tpkg:isMarkerFor` |
| `tpkg:isPredictedMarkerFor` | **TPKG26-02** (new) | project | `tpkg:isMarkerFor` |
| `tpkg:observedIn` | **TPKG26-03** (new) | project | UKC-105475 *occur* |

## 2.3 Data properties

| EType | Term | Concept | Resource |
|---|---|---|---|
| Gene | `tpkg:hgncId` | EDAM:data_2298 *Gene ID (HGNC)* | EDAM |
| Gene | `tpkg:approvedSymbol` | NCIT:C43568 *Gene Symbol* | NCIt |
| Gene | `tpkg:approvedName` | EDAM:data_2299 *Gene name* | EDAM |
| Gene | `tpkg:sourceSymbol` | EDAM:data_1026 *Gene symbol* | EDAM |
| Gene | `tpkg:hgncResolutionMethod` | **TPKG26-04** (new), parent UKC-38540 *result* | project |
| Pathway, Disease | `rdfs:label` | `rdfs:label` | W3C RDF Schema |
| Pathway | `tpkg:hallmarkId` | EDAM:data_1082 *Pathway or network identifier* | EDAM |
| Pathway | `tpkg:sourceUrl` | EDAM:data_1052 *URL* | EDAM |
| CellType | `tpkg:cellName` | EDAM:data_2892 *Cell type name* | EDAM |
| CellType | `tpkg:tissueClass` | **TPKG26-05** (new), parent UKC-28479 *tissue* | project |
| CellType | `tpkg:diseaseCategory` | **TPKG26-06** (new), parent UKC-31356 *category* | project |
| CellType | `tpkg:tissueType` | UKC-28479 *tissue* | UKC |
| CellType | `tpkg:cellNameClass` | **TPKG26-07** (new), parent UKC-42808 *class* | project |
| CellType | `tpkg:cellOntologyId` | EDAM:data_3238 *Cell type ontology ID* | EDAM |
| Disease | `tpkg:mondoId` | EDAM:data_3667 *Disease identifier* | EDAM |
| Disease | `tpkg:sourceDiseaseName` | EDAM:data_3668 *Disease name* | EDAM |

## 2.4 New concepts added to the language teleontology

| ID | Term | Gloss (written by the project) | Parent |
|---|---|---|---|
| TPKG26-01 | is reported marker for | A gene is a reported marker for a cell type when CellMarker has at least one record of it collected from a study, a review, or a company, rather than predicted by a computational tool. | `tpkg:isMarkerFor` |
| TPKG26-02 | is predicted marker for | A gene is a predicted marker for a cell type when all the CellMarker records of it come from computational marker-detection tools. | `tpkg:isMarkerFor` |
| TPKG26-03 | observed in | A cell type is observed in a disease when CellMarker has at least one record of the cell type in that disease; it does not say which of its markers were found there. | UKC-105475 *occur* |
| TPKG26-04 | HGNC resolution method | The way a gene symbol of a source dataset was matched to its HGNC entry: on the approved symbol, or on a unique previous or alias symbol. | UKC-38540 *result* |
| TPKG26-05 | tissue class | The broad tissue or organ category under which CellMarker groups a record (138 values, e.g. Lung, Bone); a tissue class contains one or more tissue types. | UKC-28479 *tissue* |
| TPKG26-06 | disease category | The broad health context in which CellMarker reports a cell type: Normal, Cancer, or Disease (other diseases). | UKC-31356 *category* |
| TPKG26-07 | cell name class | The broader cell class under which CellMarker groups a cell name (248 values, e.g. Progenitor cell). | UKC-42808 *class* |

## 2.5 Notes on the choices

- **The UKC first, when its sense fits.** Gene, Disease and tissue type are aligned to the UKC.
  For `participatesIn` the UKC has the verb *participate* (UKC-104720, "share in something"),
  but its sense is too generic for a gene–process relation, so RO:0000056 was preferred.
- **Biological terms missing from the UKC.** The UKC has *pathway* only as a trodden path or a
  nerve pathway, *cell* but not *cell type*, and only generic *identifier*, *symbol* and
  *name*. These terms were aligned to NCIt, EFO, RO and EDAM.
- **Approved vs. source symbol.** `approvedSymbol` uses NCIt *Gene Symbol*, whose gloss says
  "approved by a nomenclature committee"; `sourceSymbol` uses the generic EDAM *Gene symbol*,
  because a source symbol can be a previous or alias symbol.
- **New concepts** cover what is specific to CellMarker or to our processing: the
  reported/predicted split (Phase 1, D17), *observed in* (D7), the HGNC resolution method, and
  CellMarker's own groupings (tissue class, disease category, cell name class).

## 2.6 Counts

| | Initially considered | Finally considered | Aligned to an existing concept | New concepts |
|---|---|---|---|---|
| Entity types | 4 | 4 | 4 | 0 |
| Object properties | 5 | 5 | 2 | 3 |
| Data properties | 21 | 16 | 12 | 4 |
