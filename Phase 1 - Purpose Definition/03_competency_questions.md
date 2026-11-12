# 3. Competency Questions

*Phase 1 (Purpose Definition), Stage 1A: purpose formalization.*
*Status: approved by the domain expert. We discarded two of the proposed sub-CQs, CQ1.1 (gene
count per pathway) and CQ3.2 (count of shared genes per cell type), but we kept the other IDs
unchanged so that references stay valid.*

The four main competency questions (CQ1–CQ4) come from our project proposal
(`docs/0_project_summary.pdf`). The guide asks for a varied list of CQs, so we also wrote some
sub-questions that refine the main ones. All of them only use our three entity types (Gene,
Pathway, CellType) and our two relations (*participates in*, *is marker for*).

## 3.1 Main competency questions

| ID | Competency question |
|---|---|
| CQ1 | Which human genes are associated with each of the 50 MSigDB Hallmark pathways? |
| CQ2 | Which biological pathways contain a given human gene? |
| CQ3 | Which cell types have marker genes in common with the genes of a selected biological pathway? |
| CQ4 | Which genes are shared between pathways identified as *activated* and pathways identified as *suppressed* in an upstream spatial transcriptomics analysis? |

Two things to keep in mind:
- the answer to **CQ3** is a gene overlap, not evidence of pathway activity in the cell type;
- in **CQ4** the lists of activated and suppressed pathways are **inputs** given by the user. A
  gene is an answer to CQ4 if it belongs to at least one activated pathway *and* at least one
  suppressed pathway.

## 3.2 Sub-competency questions

| ID | Refines | Sub-competency question | Status |
|---|---|---|---|
| CQ1.2 | CQ1 | What are the HGNC ID and the approved name of each gene in a given pathway? | approved |
| CQ2.1 | CQ2 | Which genes belong to more than one Hallmark pathway, and to how many? | approved |
| CQ2.2 | CQ2 | For which cell types is a given gene reported as a marker, optionally within a given tissue class? | approved |
| CQ3.1 | CQ3 | Which cell types share marker genes with a selected pathway, considering only markers reported in a given tissue class (e.g. *Lung*)? | approved |
| CQ3.3 | CQ3 | Which specific genes make up the overlap between a given pathway and a given cell type? | approved |
| CQ4.1 | CQ4 | For each gene shared by the two groups, which activated and which suppressed pathways contain it? | approved |
| CQ4.2 | CQ4 | Which of the genes shared by the two groups are also markers of at least one cell type, and of which ones? | approved |

For the tissue filter (CQ2.2 and CQ3.1) we use the CellMarker `tissue_class` value **exactly as
it is written in the source**. This way we do not need any mapping to an external tissue
ontology: `tissue_class` has 138 distinct values and is never empty. We decided not to use the
UBERON IDs, because they are missing in 101,872 records and do not match tissue types
one-to-one.

## 3.3 CQs and entities by Focus

The guide asks to classify the entities with the Focus parameter (Common / Core / Contextual).
We proposed this classification and the domain expert accepted it:

- **Core:** Pathway and CellType, because the whole purpose is about linking these two.
- **Common:** Gene. It is a general entity, already modelled in reference resources like HGNC,
  and it is the bridge between pathways and cell types.
- **Contextual:** the tissue and disease context from CellMarker. It is not an entity type: it
  is kept as attributes of CellType (see decision D5 in `05_concept_identification.md`).

| Scenario | Persona | CQ | Common entities | Core entities | Contextual |
|---|---|---|---|---|---|
| S1, S2 | P1, P3 | CQ1 | Gene | Pathway | |
| S2 | P3 | CQ1.2 | Gene | Pathway | |
| S5, S6 | P3, P4 | CQ2 | Gene | Pathway | |
| S5 | P3 | CQ2.1 | Gene | Pathway | |
| S6 | P4 | CQ2.2 | Gene | CellType | tissue class |
| S3 | P2 | CQ3 | Gene | Pathway, CellType | |
| S3 | P2 | CQ3.1 | Gene | Pathway, CellType | tissue class |
| S3 | P2 | CQ3.3 | Gene | Pathway, CellType | |
| S4 | P1 | CQ4 | Gene | Pathway | |
| S4 | P1 | CQ4.1 | Gene | Pathway | |
| S4 | P1 | CQ4.2 | Gene | Pathway, CellType | |
