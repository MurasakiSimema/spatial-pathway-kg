# 5. Concept Identification

*Phase 1 (Purpose Definition), Stage 1A: concept identification.*
*Status: draft for review.*

Following the middle-out approach of the guide, we looked for concepts in two directions:
- the **identifying attributes** come from the datasets (`04_input_inspection.md`);
- the **descriptive attributes** come from the competency questions
  (`03_competency_questions.md`).

The same information, in a form that can be read by a program, is in the Purpose Formalization
sheet [`pf_sheet.csv`](pf_sheet.csv).

## 5.1 Entity types

| EType | Focus | What it represents in the KG | Source | Instances (preview) |
|---|---|---|---|---|
| Gene | Common | A human gene, identified through HGNC. It connects pathways and cell types. We only include genes that appear in MSigDB Hallmark or CellMarker. | HGNC (identity), MSigDB, CellMarker (where it appears) | ≤ 4,384 from Hallmark + those from CellMarker (exact count after Phase 2) |
| Pathway | Core | One of the 50 MSigDB Hallmark gene sets, i.e. a coherent biological state or process. | MSigDB Hallmark | 50 |
| CellType | Core | A human cell type **in a tissue class and disease category**, as reported by CellMarker (e.g. *Macrophage — Lung — Cancer*). | CellMarker 3.0 | 12,632 |

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
  putting it in the key would mean normalizing it first. We keep it as a descriptive attribute
  that can have more than one value: 2,126 of the 12,632 CellTypes have more than one disease
  value, at most 93.

## 5.2 Identifying attributes (from the datasets)

| EType | Primary | Secondary |
|---|---|---|
| Gene | HGNC ID (`hgnc_id`, e.g. `HGNC:1697`) | approved HGNC symbol (e.g. `CD74`); for genes we cannot resolve to HGNC, the normalized source symbol (the rule will be set in Phase 2) |
| Pathway | Hallmark gene-set identifier (e.g. `HALLMARK_HYPOXIA`) | MSigDB gene-set URL |
| CellType | (`cell_name`, `tissue_class`, `disease_category`) | Cell Ontology ID(s), when present and valid |

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
| CellType | disease | string | multi | Contextual | descriptive context |
| CellType | tissue type | string | multi | Contextual | descriptive context (more detailed than tissue class) |
| CellType | cell name class | string | single | Contextual | browsing (248 broader classes) |
| CellType | Cell Ontology ID | string | multi | Common | link to the Cell Ontology (LOD) |

## 5.4 Relationships

| Relation | Domain → Range | Cardinality | Focus | Source | Needed by |
|---|---|---|---|---|---|
| participates in | Gene → Pathway | N:M | Core | MSigDB Hallmark | CQ1, CQ1.2, CQ2, CQ2.1, CQ3, CQ3.1, CQ3.3, CQ4, CQ4.1, CQ4.2 |
| is marker for | Gene → CellType | N:M | Core | CellMarker 3.0 | CQ2.2, CQ3, CQ3.1, CQ3.3, CQ4.2 |

### Attributes of the *is marker for* relation (marker evidence)

With decision D1 we keep all the CellMarker records, both predicted and curated, and we keep
track of their source. This information is about one specific gene–cell-type link, not about
the gene or the cell type on its own:

| Attribute | Values | Focus |
|---|---|---|
| marker source | `Method`, `Single-cell sequencing`, `Experiment`, `Review`, `Company` | Contextual |
| method details | e.g. `COSG`, `CelliD`, `Cepo` | Contextual |
| PubMed ID | multi | Contextual |
| publication year | multi, 1978–2026 | Contextual |

In the ER model these are **attributes of the relationship**. How to write them in RDF without
adding a fourth entity type (for example with RDF-star annotations or with standard
reification) is something we will decide in Phase 3; see open item O1 in `06_er_model.md`.

## 5.5 Concepts we considered and left out

| Concept | Why we left it out |
|---|---|
| Tissue, Disease as entity types | out of scope (AGENT.md §3); kept as literals of CellType |
| UBERON tissue IDs | incomplete (5.7% missing) and not one-to-one; they would need a mapping |
| Activated / suppressed pathway group | it is a query input, not something stored in the KG |
| Gene count per pathway (CQ1.1) | the domain expert discarded this sub-CQ |
| HGNC locus group/type, Entrez, Ensembl, UniProt | out of scope (AGENT.md §3.3) |
| CellMarker `gene_id`, `uniprot_id`, `technology_seq`, `series_id`, `title`, `journal` | no CQ needs them; they stay in the Phase 2 audit table, not in the KG |
