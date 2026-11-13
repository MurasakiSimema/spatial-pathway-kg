# iTelos Methodology Guide & Project Mapping

The **iTelos methodology** is a purpose-driven, diversity-aware, and stratified methodology for Knowledge Graph engineering developed by the KnowDive / DataScientia group at the University of Trento.

This reference provides the theoretical background, architectural layers, and direct mapping between the repository folders and the academic documentation sections.

---

## 1. Core Principles of iTelos

Traditional ontology and KG engineering often suffers from scope creep, semantic drift, and excessive complexity by attempting to model entire domains comprehensively. iTelos addresses this through three foundational principles:

1. **Purpose-Driven Engineering**:
   - The KG is engineered strictly to satisfy a predefined set of user requirements formalized as **Scenarios**, **Personas**, and **Competency Questions (CQs)**.
   - Any entity type, relation, or dataset field that does not serve the defined purpose is excluded.

2. **Stratified Architecture**:
   - Explicitly decouples three operational layers:
     - **Language Layer**: Controls vocabulary, natural language terms, synonyms, and multilingual lexical-semantic concepts (e.g., using WordNet or the Universal Knowledge Core).
     - **Knowledge Layer**: Models conceptual schemas, classes (eTypes), object properties, and axioms without data-level instances. Built by composing small, modular ontology fragments called **atoms**.
     - **Data Layer**: Handles physical datasets, tabular records, entity values, and data cleaning/formatting.

3. **Popularity-Driven Integration**:
   - Resources, terms, and schema elements are classified into three popularity categories based on frequency of occurrence and centrality to the purpose:
     - **Core**: Elements that are specific to the purpose and without which it cannot be satisfied.
     - **Common**: General elements, shared across sources and domains and already modelled by reference resources.
     - **Contextual**: Elements that provide specific context (e.g. experimental, anatomical or clinical details).
   - The classification of this project's elements is a Phase 1 decision: take it from `pf_sheet.csv` and `05_concept_identification.md`, never from this guide.

4. **Producer vs. Consumer Processes**:
   - *Producer Process*: Models and cleans each dataset individually against its own local schema.
   - *Consumer Process*: Composes and aligns multiple datasets against a unified target knowledge structure (the **Teleology**).

---

## 2. Theoretical Vocabulary

- **Teleology**: The purpose-specific knowledge structure designed to satisfy the project's CQs, constructed by composing ontology atoms.
- **Teleontology**: The overarching background or foundational ontology against which teleology elements are aligned and anchored.
- **eType (Entity Type)**: A formal class representing a category of entities (e.g., `Gene`, `Pathway`, `CellType`, `Disease`).
- **Atom**: A minimal, self-contained ontology fragment representing a single concept and its immediate attributes/relations.
- **Competency Question (CQ)**: A natural language question that the KG must be able to answer, later operationalized as a SPARQL query.
- **Common Frequency Scale (CFS)**: Standard 5-point scale (A: Never, B: Rarely, C: Sometimes, D: Often, E: Always) used to measure human/LLM activity.

---

## 3. Mapping: Repository Folders to Report Sections

| Repository Directory | iTelos Phase | Report Section | Key Deliverables & Evidence |
|:---|:---|:---|:---|
| Project Root (`AGENT.md`, `README.md`) | Inception / Design | Section 1 (Intro) & Section 2 (Project Design) | Scope boundaries, Domain of Interest, literature citations (`KnowDivePubs.bib`), informal purpose. |
| `Phase 1 - Purpose Definition/` | Phase 1: Purpose Definition | Section 3 (`S3.tex`) | Scenarios, personas, CQs, informal labels table, Purpose ER model, data sources inspection. |
| `Phase 2 - Language Definition/` | Phase 2: Language Definition | Section 4 (`S4.tex`) | Language terms, Language Resource Table (LRT), UKC alignment, symbol normalization scripts. |
| `Phase 3 - Knowledge Definition/` | Phase 3: Knowledge Definition | Section 5 (`S5.tex`) | Composed teleology ontology atoms, Knowledge Teleontology alignment, data shape constraints. |
| `Phase 4 - Entity Definition/` | Phase 4: Entity Definition | Section 6 (`S6.tex`) | Karma R2RML models, RDFLib ingestion scripts, HGNC resolution table, Turtle serialization (`.ttl`). |
| `Evaluation/` | Phase 5: Evaluation | Section 7 (`S7.tex`) | `graph_statistics.json`, `validation_summary.json`, entity connectivity, SPARQL query results (Q1–Q4). |
| `Metadata/` | Phase 5: Metadata | Section 8 (`S8.tex`) | DC Terms, VoID statistics, resource catalog metadata tables. |
| Post-Evaluation Analysis | Phase 6: Conclusion | Section 9 (`S9.tex`) | Schedule audit, purpose satisfaction analysis, open issues, future work. |
| All Phases | Transversal | Appendix A (`secA-Appendix.tex`) | LLM questionnaire answered across all 6 phases using the CFS scale. |
| Technical Handover | Transversal | Appendix B (`secB-Appendix.tex`) | SPARQL `.rq` files, schema listings, sample query tables. |

---

## 4. Phase-by-Phase Process Details for the Report

### Phase 1: Purpose Definition
- **Step 1.1**: Clarify the informal user need into a concise statement.
- **Step 1.2**: Define a set of usage scenarios covering the different aspects of the purpose (as many as needed; the number is a project decision).
- **Step 1.3**: Characterize the Personas acting within the scenarios.
- **Step 1.4**: Define the Competency Questions (CQ1 to CQ4 from the proposal, plus any approved sub-CQs).
- **Step 1.5**: Extract informal labels for entity types, object properties, and data properties; classify by popularity.
- **Step 1.6**: Construct the Purpose ER model (entities, relationships, attributes, cardinalities).
- **Step 1.7**: Conduct Information Gathering: identify formal KnowDive sources and external sources (MSigDB, CellMarker, HGNC).
- **Step 1.8**: Complete Phase 1 Qualitative Evaluation table and Appendix A (Part 1, 2, 3).

### Phase 2: Language Definition
- **Knowledge Layer**:
  - Finalize language terms for `Gene`, `Pathway`, `CellType`, `Disease`, `participates_in`, `is_marker_for`, `observed_in`, and data properties.
  - Align terms to lexical concepts in UKC / WordNet (identifying synsets, hypernyms, definitions).
- **Data Layer**:
  - Filter and clean raw input datasets: trim whitespace, uppercase gene symbols for comparison only (AGENT.md §5.1; the original strings are kept for audit), validate format of identifiers.
- **Evaluation**: Report initial vs final term counts and teleontology alignments.

### Phase 3: Knowledge Definition
- **Knowledge Layer**:
  - Construct the teleology by composing ontology atoms for Gene, Pathway, CellType, and Disease.
  - Define domains and ranges:
    - $\text{domain}(\text{participates\_in}) = \text{Gene}$, $\text{range}(\text{participates\_in}) = \text{Pathway}$
    - $\text{domain}(\text{is\_marker\_for}) = \text{Gene}$, $\text{range}(\text{is\_marker\_for}) = \text{CellType}$
  - Anchor the teleology into the Knowledge Teleontology.
- **Data Layer**:
  - Restructure datasets to match the schema shape.

### Phase 4: Entity Definition
- **Producer Process (Single Dataset)**:
  - Extract and identify entities in MSigDB Hallmark, CellMarker 3.0, and HGNC.
- **Consumer Process (Multi-Dataset Composition)**:
  - Align MSigDB and CellMarker entities using the HGNC resolution procedure:
    - Match normalized symbols against approved HGNC entries.
    - Resolve unique matches to stable HGNC IDs (`HGNC:\d+`).
    - Flag ambiguous, previous, alias, or withdrawn symbols.
    - Retain unresolved genes under deterministic local URIs with resolution status literal.
- **Mapping & Turtle Generation**:
  - Build RDF triples using RDFLib (or Karma R2RML).
  - Mint deterministic URIs.
  - Preserve source context (tissue, disease, sample context).

### Phase 5: Evaluation & Metadata
- **Quantitative Evaluation**:
  - Calculate basic statistics (triples, entities, relations, shared genes, resolution rate).
  - Calculate source completeness / missing-value rates per column.
  - Calculate entity connectivity (connected / total * 100%).
- **Competency Query Evaluation**:
  - Execute SPARQL templates for CQ1–CQ4 against synthetic test fixtures and production KG.
- **Metadata Generation**:
  - Compile Dublin Core Terms and VoID statistics.
  - Prepare metadata packages for catalog distribution.

### Phase 6: Conclusion & Open Problems
- Review project execution vs timeline.
- Verify purpose coverage and document any unfulfilled aspects.
- Formulate open research challenges and future extensions.
