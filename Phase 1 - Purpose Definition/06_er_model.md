# 6. Purpose ER Model

*Phase 1 (Purpose Definition), Stage 1A: ER modelling.*
*Status: draft for review.*

The ER model is the first version of the knowledge layer of our KG, built around our purpose.
It only contains what we agreed on in the scope: three ETypes and two relations.

## 6.1 Diagram

```mermaid
erDiagram
    GENE }o--o{ PATHWAY : "participates in"
    GENE }o--o{ CELLTYPE : "is marker for"

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
        string disease "multi; free text, e.g. Lung adenocarcinoma (LUAD)"
        string tissue_type "multi"
        string cell_name_class "broader class"
        string cell_ontology_id "multi; e.g. CL_0000235"
    }
```

Mermaid cannot draw attributes on a relationship, so we list them here:

| Relationship | Attributes |
|---|---|
| GENE — *is marker for* → CELLTYPE | `marker_source`, `method_details`, `pmid` (multi), `year` (multi) |
| GENE — *participates in* → PATHWAY | none (the membership is just as MSigDB states it) |

## 6.2 Focus

| Element | Focus |
|---|---|
| Gene | Common |
| Pathway | Core |
| CellType | Core |
| participates in, is marker for | Core |
| marker evidence, `disease`, `tissue_type`, `cell_name_class` | Contextual |

## 6.3 How to read the model

- Both relations are many-to-many. A gene can belong to several pathways (e.g. `MYC` is in 10)
  and be a marker of several cell types. A pathway contains between 32 and 200 genes.
- Pathway and CellType are **never connected directly**. Their connection (CQ3) is always
  computed through the genes they share, so the KG never asserts pathway activity in a cell
  type.
- The groups of activated and suppressed pathways (CQ4) are not part of the model: they are
  given to the query.

## 6.4 What is left for the next phases

| ID | Item | Phase |
|---|---|---|
| O1 | How to write the *is marker for* evidence attributes in RDF without adding a fourth entity type (RDF-star annotation vs. reification vs. audit table only) | Phase 3 |
| O2 | How to build the URI key of a CellType from (`cell_name`, `tissue_class`, `disease_category`) in a deterministic way | Phase 3 |
| O3 | What to do with duplicate rows (D3), and the HGNC resolution rules for unresolved symbols and symbols that differ only in case | Phase 2 |
