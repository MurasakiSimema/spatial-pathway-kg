# 5. Concept Identification

*Phase 1 (Purpose Definition), Stage 1A: concept identification.*
*Status: draft for review.*

Following the middle-out approach of the guide, we looked for concepts in two directions:
- the **identifying attributes** come from the datasets (`04_input_inspection.md`);
- the **descriptive attributes** come from the competency questions   (`03_competency_questions.md`).

The same information, in a form that can be read by a program, is in the Purpose Formalization
sheet [`pf_sheet.csv`](pf_sheet.csv).

## 5.1 Entity types

| EType | Focus | What it represents in the KG | Source | Instances (preview) |
|---|---|---|---|---|
| Gene | Common | A human gene, identified through HGNC. It connects pathways and cell types. We only include genes that appear in MSigDB Hallmark or CellMarker. | HGNC (identity), MSigDB, CellMarker (where it appears) | ≤ 4,384 from Hallmark + those from CellMarker (exact count after Phase 2) |
| Pathway | Core | One of the 50 MSigDB Hallmark gene sets, i.e. a coherent biological state or process. | MSigDB Hallmark | 50 |
| CellType | Core | A human cell type **in a tissue class and disease category**, as reported by CellMarker (e.g. *Macrophage — Lung — Cancer*). | CellMarker 3.0 | 12,632 |
| Disease | Common | A MONDO disease in which CellMarker reports a cell type (e.g. *hepatocellular carcinoma*, `MONDO:0007256`). Only the CellMarker diseases with a reliable MONDO match become Diseases (D15). | CellMarker 3.0 (instances), MONDO (identity, labels) | ≈ 521 (prototype; exact count in Phase 2) |

### Why CellType includes the context (decisions D2 and D5)

- **D2:** we name a cell type with the CellMarker `cell_name` and not with its Cell Ontology ID.
  Names and CL IDs do not match one-to-one (`Macrophage` appears with 24 CL IDs), and the name
  is what users actually search for.
- **D5:** the same cell type is reported in many contexts (e.g. `Macrophage` appears in 98
  tissue classes), so the identity key of a CellType is **(`cell_name`, `tissue_class`,
  `disease_category`)**. In this way the tissue filter of CQ2.2 and CQ3.1 works on simple
  attributes. The three parts of the key are also kept as separate literals, so it is still
  possible to search by the base name (e.g. all the *Macrophage* CellTypes).
- The specific `disease` is **not** part of the key. It is free text with 1,067 values, and
  putting it in the key would mean normalizing it first. At first we kept it as a descriptive
  attribute with more than one value (2,126 of the 12,632 CellTypes have more than one disease
  value, at most 93). With the scope change of 2026-11-13 it became the **Disease** entity
  type, linked through *observed in* (decisions D6–D15, `04_input_inspection.md`).

## 5.2 Identifying attributes (from the datasets)

| EType | Primary | Secondary |
|---|---|---|
| Gene | HGNC ID (`hgnc_id`, e.g. `HGNC:1697`) | approved HGNC symbol (e.g. `CD74`); for genes we cannot resolve to HGNC, the normalized source symbol (the rule will be set in Phase 2) |
| Pathway | Hallmark gene-set identifier (e.g. `HALLMARK_HYPOXIA`) | MSigDB gene-set URL |
| CellType | (`cell_name`, `tissue_class`, `disease_category`) | Cell Ontology ID(s), when present and valid |
| Disease | MONDO ID (e.g. `MONDO:0007256`), from a reliable match (D8, D9, D15) | MONDO label |

## 5.3 Descriptive attributes (from the CQs)

| EType | Attribute | Type | Values | Focus | Needed by |
|---|---|---|---|---|---|
| Gene | approved symbol | string | single | Common | CQ1, CQ2, all CQ answers |
| Gene | approved name | string | single | Common | CQ1.2 |
| Gene | HGNC ID | string | single | Common | CQ1.2 |
| Gene | source symbol(s) | string | multi | Contextual | checking the HGNC resolution |
| Gene | resolution status | string | single | Contextual | checking the HGNC resolution |
| Pathway | Hallmark identifier | string | single | Core | CQ1–CQ4 (query input and output) |
| Pathway | label | string | single | Core | readability (e.g. *Hypoxia*) |
| Pathway | source URL | string (URI) | single | Common | provenance |
| CellType | cell name | string | single | Core | CQ2.2, CQ3, CQ3.1, CQ3.3, CQ4.2 |
| CellType | tissue class | string | single | Core | CQ2.2, CQ3.1 (tissue filter) |
| CellType | disease category | string (`Normal` / `Cancer` / `Disease`) | single | Core | context of the CQ3 answers |
| CellType | tissue type | string | multi | Contextual | descriptive context (more detailed than tissue class) |
| CellType | cell name class | string | single | Contextual | browsing (248 broader classes) |
| CellType | Cell Ontology ID | string | multi | Common | link to the Cell Ontology (LOD) |
| Disease | MONDO ID | string | single | Common | CQ3.4 (subclasses), link to MONDO (LOD) |
| Disease | label | string | single | Common | CQ3.4, readability |
| Disease | source strings | string | multi | Contextual | the CellMarker `disease` values, verbatim (D11) |

## 5.4 Relationships

| Relation | Domain → Range | Focus | Source | Needed by |
|---|---|---|---|---|
| participates in | Gene → Pathway | Core | MSigDB Hallmark | CQ1, CQ1.2, CQ2, CQ2.1, CQ3, CQ3.1, CQ3.3, CQ4, CQ4.1, CQ4.2 |
| is marker for | Gene → CellType | Core | CellMarker 3.0 | CQ2.2, CQ3, CQ3.1, CQ3.3, CQ3.4, CQ4.2 |
| ↳ is reported marker for | Gene → CellType | Contextual | CellMarker 3.0 (at least one record with `marker_source` ≠ `Method`) | D1 filter on the CQs above |
| ↳ is predicted marker for | Gene → CellType | Contextual | CellMarker 3.0 (only `Method` records) | D1 filter on the CQs above |
| observed in | CellType → Disease | Common | CellMarker 3.0 (`disease` with `disease_category` ≠ `Normal`) | CQ3.4 |

*observed in* has no attributes. It says that CellMarker has at least one record of the cell
type in that disease; it does not say which markers were found there (D7).

### Sub-relations of *is marker for* (decisions D16–D18)

With decision D1 we keep all the CellMarker records, both predicted and reported. At first we
kept the evidence (`marker_source`, `method_details`, PubMed ID, year) as attributes of the
relation. On 2026-11-17 we removed them: no CQ needs them, they have many values on
the same link, and in RDF they would need reification.

What we keep is only whether a link is **reported** or **predicted**, and we write it in the
predicate itself. Each gene–cell-type link is written with **exactly one** of two sub-relations
of *is marker for*:

| Sub-relation | When | Links (before HGNC resolution) |
|---|---|---|
| *is reported marker for* | at least one record with `marker_source` = Single-cell sequencing, Experiment, Review, or Company | 108,040 |
| *is predicted marker for* | only `Method` records (computational tools such as COSG, CelliD) | 869,420 |

*Reported* means that CellMarker collected the marker from a study, a review, or a company, and
did not predict it with a tool. It does not mean that the marker was validated by hand. The
10,571 links that have both kinds of records count as reported.

*is marker for* stays as the parent relation (`rdfs:subPropertyOf`), and the CQs still use it.
Its triple is stored too, next to the sub-relation triple, so that the queries do not depend on
a reasoner (D18). The relations have no attributes any more, so open
item O1 is closed.

## 5.5 Concepts we considered and left out

| Concept | Why we left it out |
|---|---|
| Tissue as entity type | kept as literals of CellType (D5); no mapping to a tissue ontology |
| Disease values that are not diseases (`Undefined`, `Pan-cancer`, vaccines, viruses, …) | they would make false Disease instances; logged as `non_disease` in the audit table (D14) |
| Disease strings without a reliable MONDO match (metastases, qualified diseases, typos, …) | no reliable identity; no Disease and no link, logged as `unresolved` in the audit table (D15) |
| UBERON tissue IDs | incomplete (5.7% missing) and not one-to-one; they would need a mapping |
| Activated / suppressed pathway group | it is a query input, not something stored in the KG |
| Marker evidence: `pmid`, `year`, `method_details` | no CQ needs them; multi-valued on the aggregated link; audit table only (D16) |
| Gene count per pathway (CQ1.1) | the domain expert discarded this sub-CQ |
| HGNC locus group/type, Entrez, Ensembl, UniProt | out of scope |
| CellMarker `gene_id`, `uniprot_id`, `technology_seq`, `series_id`, `title`, `journal` | no CQ needs them; they stay in the Phase 2 audit table, not in the KG |
