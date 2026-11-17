# 6. Purpose ER Model

*Phase 1 (Purpose Definition), Stage 1A: ER modelling.*
*Status: draft for review.*

The ER model is the first version of the knowledge layer of our KG, built around our purpose.
It only contains what we agreed on in the scope: four ETypes and three relations (Disease and
*observed in* were added with the scope change of 2026-11-13, see `04_input_inspection.md`).

## 6.1 Diagram

```mermaid
erDiagram
    GENE }o--o{ PATHWAY : "participates in"
    GENE }o--o{ CELLTYPE : "is marker for"
    CELLTYPE }o--o{ DISEASE : "observed in"

    GENE {
        string hgnc_id PK "HGNC ID, e.g. HGNC:1697"
        string approved_symbol "e.g. CD74"
        string approved_name "e.g. CD74 molecule"
        string source_symbols "multi; as found in MSigDB / CellMarker"
        string resolution_status "HGNC resolution outcome"
    }
    PATHWAY {
        string hallmark_id PK "e.g. HALLMARK_HYPOXIA"
        string label "e.g. Hypoxia"
        string source_url "MSigDB gene-set page"
    }
    CELLTYPE {
        string cell_name PK "e.g. Macrophage"
        string tissue_class PK "e.g. Lung"
        string disease_category PK "Normal | Cancer | Disease"
        string tissue_type "multi"
        string cell_name_class "broader class"
        string cell_ontology_id "multi; e.g. CL_0000235"
    }
    DISEASE {
        string mondo_id PK "e.g. MONDO:0007256"
        string label "MONDO label"
        string source_strings "multi; verbatim CellMarker values"
    }
```

Mermaid cannot draw attributes on a relationship, so we list them here:

| Relationship | Attributes |
|---|---|
| GENE — *is marker for* → CELLTYPE | none; specialized into *is reported marker for* and *is predicted marker for* (D17) |
| GENE — *participates in* → PATHWAY | none (the membership is just as MSigDB states it) |
| CELLTYPE — *observed in* → DISEASE | none (CellMarker has at least one record of the cell type in the disease) |

Mermaid cannot draw sub-relations either. *is marker for* has two sub-relations, *is reported
marker for* and *is predicted marker for* (Gene → CellType); each gene–cell-type link is
stored with *is marker for* and with exactly one of them (D17, D18).

## 6.2 Focus

| Element | Focus |
|---|---|
| Gene | Common |
| Disease | Common |
| Pathway | Core |
| CellType | Core |
| participates in, is marker for | Core |
| observed in | Common |
| *is reported marker for*, *is predicted marker for*, `tissue_type`, `cell_name_class`, Disease `source_strings` | Contextual |

## 6.3 How to read the model

- A gene can belong to several pathways (e.g. `MYC` is in 10)
  and be a marker of several cell types. A pathway contains between 32 and 200 genes.
- Pathway and CellType are **never connected directly**. Their connection (CQ3) is always
  computed through the genes they share, so the KG never asserts pathway activity in a cell
  type.
- A marker link is either reported or predicted, never both (D17). Queries on any marker use
  *is marker for*, which covers both sub-relations.
- Disease is reached from a Pathway only through Gene → CellType → Disease. *observed in* is
  attached to the CellType, not to the single marker, so the KG does not say in which disease a
  marker was reported (D7, CQ3.4).
- CellTypes with `disease_category = Normal` have no *observed in* link, and neither do disease
  values without a reliable MONDO match (D15) or values that are not diseases (D14). A CellType
  can therefore have no *observed in* link even if its category is `Cancer` or `Disease`.
- The groups of activated and suppressed pathways (CQ4) are not part of the model: they are
  given to the query.

## 6.4 What is left for the next phases

| ID | Item | Phase |
|---|---|---|
| O1 | ~~How to write the *is marker for* evidence attributes in RDF without adding a fourth entity type~~ **Closed on 2026-11-17** by D16–D18: no relation attributes are left | — |
| O2 | How to build the URI key of a CellType from (`cell_name`, `tissue_class`, `disease_category`) in a deterministic way | Phase 3 |
| O3 | What to do with duplicate rows (D3), and the HGNC resolution rules for unresolved symbols and symbols that differ only in case | Phase 2 |
| O4 | The exact local URI rule for Disease, from the MONDO ID (together with O2) | Phase 3 |
| O5 | Aligning the Disease class to the MONDO root `MONDO:0000001` (*disease*), as CellType is aligned to CL | Phase 3 |
| O6 | The MONDO matching pipeline: D14 non-disease list, audit log of merges and of unresolved strings (including metastases, D13, D15), review of the merges | Phase 2 (rules) / Phase 4 (pipeline) |
| O7 | Pin the MONDO release used (`mondo.owl`, 2026-11-03) so that results can be reproduced | Phase 4 |
| O8 | Which predicate links a Disease to its MONDO IRI | Phase 3 |
| O9 | The exact names and URIs of the two sub-relations of *is marker for*, and whether to align them to an external vocabulary | Phase 3 |
