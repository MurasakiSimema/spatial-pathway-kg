# Report Structure Specification

This guide specifies the exact structure, mandatory subsections, LaTeX table structures, and required content for each section of the DataScientia KG Report, based on `Documentation/Template_KG2026_report-pdf.pdf` and `AGENT.md`.

> **All concrete values below (scenario texts, persona profiles, versions, URIs, counts, dates, pass rates) are format examples.** Replace them with what the phase deliverables and evaluation outputs actually contain; if something is not available, write a TODO marker (SKILL.md, Ground Rule 2).
>
> For structure and level of detail, compare with the previous-year report `docs/5_example.pdf` (see SKILL.md, "Example report"); its content and metrics are not to be reused.

---

## 1. Document Preamble & Frontmatter (`main.tex`)

- **Class**: `\documentclass{knowdive}`
- **Title**: Must be descriptive and specific to the project:
  ```latex
  \title{Spatial Transcriptomics Knowledge Graph: \\ iTelos Purpose-Driven Knowledge Graph Report}
  ```
- **Author**: Replace `Author1, ..., AuthorN` with the project author(s).
- **Revision History**:
  ```latex
  \revisionhistory{
      \revision{0.1}{20.04.2020}{Fausto Giunchiglia}{Document created}
      \revision{0.2}{12.01.2022}{Fausto Giunchiglia}{Document template simplified a lot with less and simpler guidelines}
      \revision{0.3}{30.10.2026}{Mayukh Bagchi}{KG - 2026 - Project Report Template}
      \revision{<version>}{<DD.MM.YYYY>}{<author(s) given by the user>}{<what changed>}
  }
  ```
  Add one row per completed phase (e.g. "Phase 1 Completed"), as in the example report.
- **Abstract** (`\section*{Abstract}`):
  - 200–250 words summarizing:
    1. Purpose: providing biological context for spatial transcriptomics interpretation by linking human genes to MSigDB Hallmark pathways and CellMarker cell-type markers.
    2. Methodology: iTelos purpose-driven, stratified engineering (language, knowledge, data layers).
    3. Technical architecture: RDF/OWL, RDFLib ingestion, SPARQL 1.1 query interface.
    4. Key results: HGNC gene normalization, query test success rate, graph connectivity and completeness, using the values in `Evaluation/`.

---

## 2. Section 1: Introduction (`S1.tex`)

### Purpose
Introduce the project within the theoretical framework of heterogeneity-aware Knowledge Graph engineering.

### Mandatory Content
1. **Reusability in Heterogeneity-Aware KGs**: Explain why reusability is paramount when integrating heterogeneous biological sources (GMT files, marker tables, nomenclature registries).
2. **The iTelos Methodology**: Present the stratified approach separating the Language Layer, Knowledge Layer, and Data Layer.
3. **Literature Citations**: Cite foundational iTelos and stratified integration works using the bibliography keys in `KnowDivePubs.bib`:
   - `\cite{p3}`: iTelos Purpose-Driven Knowledge Graph Generation.
   - `\cite{p1}`: Stratified Data Integration.
   - `\cite{p2}`: Popularity-Driven Data Integration.
   - `\cite{p4}`: Language and Knowledge Representation: A Stratified Approach (Bagchi 2025).
   - `\cite{p5}`: About Me and You - iTelos: A Cooperative Methodology (Bocca 2025).
   - `\cite{p6}`: Representation Heterogeneity.
4. **Report Roadmap**: Brief paragraph introducing Sections 2 through 9 and Appendices A and B.

---

## 3. Section 2: Project Design (`S2.tex`)

### Purpose
Define the high-level boundaries of the Knowledge Graph project before formalizing requirements.

### Mandatory Content
1. **Domain of Interest (DoI) Boundaries**:
   - **Space Boundaries**: Human molecular and cellular biology (*Homo sapiens*), transcriptomics, and spatial transcriptomics contextualization.
     > **Critical Scope Restriction**: The KG does *not* directly process or store 2D/3D physical spatial coordinates, tissue image pixel matrices, slide geometries, or spot expression grids. It provides the structured biological context needed by downstream spatial transcriptomics tools.
   - **Time Boundaries**: Contemporary post-genomic molecular biology, bounded by the specific snapshot releases actually used: HGNC Complete Set, MSigDB Hallmark collection, and CellMarker (versions/dates as recorded in the Phase 1 input inspection).
2. **General Purpose (Informal Definition)**:
   - Provide a natural language description as expressed by domain researchers.
   - State the core objective: integrate human genes (identified via HGNC) with 50 MSigDB Hallmark pathways and curated human cell-type markers from CellMarker to enable query-driven biological interpretation of spatial spot clusters, cell-type pathway overlaps, and functional pathway state contrasts.

---

## 4. Section 3: Purpose Definition (`S3.tex`)

### Purpose
Formalize user needs through scenarios, personas, competency questions, and the initial Purpose ER model, followed by information gathering.

### Mandatory Content

#### 3.1 Purpose Formalization
- **Scenarios**:
  - *Scenario 1 (Pathway Annotation of Spatial Spot Clusters)*: A bioinformatician analyzes spatial transcriptomics data from a human tissue sample. After clustering spots with similar expression profiles, they need to identify which functional Hallmark pathways are represented by the marker genes characterizing each spot cluster.
  - *Scenario 2 (Cell-Type Marker & Pathway Overlap)*: A researcher exploring tissue frontiers wants to know which cell types share marker genes with specific pathways (e.g., Epithelial-Mesenchymal Transition, Hypoxia) to propose candidate cell identities without claiming causality or in situ activation.
  - *Scenario 3 (Dual-State Pathway Analysis)*: A scientist analyzing perturbed spatial tissue sections identifies externally defined activated and suppressed pathway lists and requires all human genes bridging both functional states.
- **Personas** (take them from `Phase 1 - Purpose Definition/`; state that they are illustrative profiles). Example shape:
  - *Persona 1*: a computational biologist working on cancer spatial transcriptomics. Goal: functional annotation of spot-derived gene lists.
  - *Persona 2*: a spatial bioinformatics pipeline developer. Goal: automated querying of gene-pathway-cell-marker relationships via SPARQL.
- **Competency Questions (CQs)**:
  - Copy CQ1–CQ4 and the approved sub-CQs verbatim from `Phase 1 - Purpose Definition/03_competency_questions.md`.
  - Use a table with one row per CQ and columns for the persona(s) and scenario(s) it serves (the example report has a "Person" column; the template asks for CQs "created considering the personas in the scenarios").
- **Informal Labels & Popularity Categories**:
  - Take the labels and their Core / Common / Contextual classification from `pf_sheet.csv` and `05_concept_identification.md`; do not reclassify them in the report.
  - Report, per eType, the identifying attributes (from the datasets) and the descriptive attributes (from the CQs), and, per relation, domain, range, cardinality and any relation attributes.
  - State the main design choices with their strong and weak points (template requirement).
- **Purpose ER Model**:
  - Formal entity-relationship diagram and narrative specifying cardinalities:
    - `Gene` (1..*) `participates_in` (1..*) `Pathway`
    - `Gene` (1..*) `is_marker_for` (1..*) `CellType`
  - Cardinality notes, primary keys, and attributes.

#### 3.2 Information Gathering
The 2026 template requires this two-level structure (one subsubsection per source group, a paragraph or table per layer):
- **KG / KnowDive Data Sources** (already available, quality resources from KG/KnowDive):
  - Knowledge layer: sources description, collection, Common / Core / Contextual classification.
  - Data layer: sources description, collection, Common / Core / Contextual classification.
  - If no KnowDive resource was collected in Phase 1, say so explicitly for both layers.
- **External Data Sources** (informal, heterogeneous resources):
  - Knowledge layer: external ontologies and vocabularies considered (e.g. Cell Ontology from the OBO Foundry), which were adopted and why; classification.
  - Data layer: detail the 3 input resources:
    1. *MSigDB Hallmark Gene Sets* (GMT format, 50 gene sets, human gene symbols).
    2. *CellMarker 3.0* (Tabular TSV, human cell markers, Cell Ontology IDs, tissue context).
    3. *HGNC Complete Set* (`hgnc_complete_set.txt`, authoritative reference resource for gene symbols, approved names, and HGNC IDs; strictly not a content dataset).
  - For each data source, list the key columns actually used, with type and meaning, as the example report does ("Key attributes in the dataset are: ...").
  - Classification of data sources into Common, Core, and Contextual layers.

#### 3.3 Qualitative Evaluation
Must include the following LaTeX tables:
1. **Scenarios Table**: Initial vs Final Scenarios.
   ```latex
   \begin{table}[ht]
   \centering
   \begin{tabularx}{\linewidth}{|l|X|l|}
   \hline
   \textbf{Scenario ID} & \textbf{Description} & \textbf{Status} \\ \hline
   SC-01 & Pathway Annotation of Spot Clusters & Retained \\ \hline
   SC-02 & Cell-Type Marker \& Pathway Overlap & Retained \\ \hline
   SC-03 & Dual-State Pathway Intersection & Retained \\ \hline
   \end{tabularx}
   \caption{Purpose Definition: Scenarios Considered}
   \end{table}
   ```
2. **Personas Table**: Initial vs Final Personas.
3. **Competency Questions Table**: Initial vs Final CQs with mapping to Scenarios. For each CQ that was changed or discarded, give old wording, new wording (if any) and the reason, as the example report does ("Old / New / Change").
4. **Dataset-level Formatting & Transformations**: Summary of format inspection and pre-filtering (e.g. GMT parsing, human-only row filtering).
5. **Remarks on LLM Usage**: Summary of LLM support during Phase 1 (referencing Appendix A).

---

## 5. Section 4: Language Definition (`S4.tex`)

### Purpose
Establish lexical terms, words, and concepts for entity types, object properties, and data properties, and align them to the Language Teleontology.

### Mandatory Content
1. **Knowledge Layer**:
   - *Fixing Language Terms*: Finalize informal terms into controlled vocabulary terms.
   - *Language Teleontology Alignment*: Align terms to parent lexical concepts in the Universal Knowledge Core (UKC) or WordNet (e.g., aligning `Gene` to biological entity, `Pathway` to biological process / biochemical pathway, `CellType` to cell class).
   - Document any custom lexical terms enriched into the teleontology.
2. **Data Layer**:
   - Cleaning, filtering, and formatting operations applied to raw source text:
     - Whitespace trimming.
     - Uppercase normalization for gene symbols across all sources.
     - Validation of Cell Ontology CURIE formats (`CL:0000000`).
     - Validation of HGNC ID formatting (`HGNC:\d+`).
3. **Qualitative Evaluation**:
   - For eTypes, object properties and data properties: first the three counts (initially considered / finally considered / aligned), then the per-term table.
   - Table: eType terms considered vs finalized vs aligned.
   - Table: Object property terms considered vs finalized vs aligned.
   - Table: Data property terms considered vs finalized vs aligned.
   - Language teleontology enrichment table.
   - Statement on whether any backtracking to Phase 1 was required.
   - Remarks on LLM usage in Phase 2.

---

## 6. Section 5: Knowledge Definition (`S5.tex`)

### Purpose
Define the formal knowledge structure (teleology) by composing ontology atoms and aligning them with the foundational Knowledge Teleontology.

### Mandatory Content
1. **Knowledge Layer**:
   - *Teleology Definition*: Compose ontology fragments/atoms representing:
     - Class `Gene`
     - Class `Pathway`
     - Class `CellType`
     - Object property `participates_in` ($\text{domain} = \text{Gene}, \text{range} = \text{Pathway}$)
     - Object property `is_marker_for` ($\text{domain} = \text{Gene}, \text{range} = \text{CellType}$)
   - *Knowledge Teleontology Alignment*: Align composed classes and properties to parent ontological entities in foundational models (e.g. OWL/RDFS primitives, BFO/OBO upper ontologies).
2. **Data Layer**:
   - Transform and structure source data to conform to the knowledge shapes defined above.
   - Explain how column values map to datatype properties.
3. **Qualitative Evaluation**:
   - Table: eTypes in teleology, source atoms, alignment to Knowledge Teleontology.
   - Table: Object properties, domains, ranges, and upper ontology alignments.
   - Table: Data properties and datatypes (e.g., `xsd:string`, `xsd:date`).
   - Discussion of ontology enrichment and backtracking.
   - Remarks on LLM usage in Phase 3.

---

## 7. Section 6: Entity Definition (`S6.tex`)

### Purpose
Map data values to knowledge structures, mint deterministic entity URIs, resolve entities across datasets, and construct the RDF Knowledge Graph.

### Mandatory Content
1. **Sub-activities**:
   - *Single Dataset Ingestion & Entity Identification*:
     - MSigDB Hallmark: Create `Pathway` entities from gene-set identifiers.
     - CellMarker 3.0: Create `CellType` entities, preserving cell names and tissue context.
     - HGNC Complete Set: Reference resolution table for gene symbols.
   - *Multi-Dataset Composition & Entity Matching*:
     - Explain the strict HGNC resolution policy:
       - Match normalized symbol against HGNC approved symbols.
       - Unique match $\rightarrow$ resolved with HGNC ID.
       - Unresolved symbols categorized as `not_found`, `non_approved_match`, `ambiguous`, or `invalid`.
       - Non-resolved genes receive local deterministic URIs and literal resolution status (never dropped silently).
     - Merge `Gene` instances across MSigDB and CellMarker strictly through identical HGNC ID.
2. **URI Construction Policy**:
   - Base URI configuration.
   - URI templates:
     - Resolved Gene: `.../gene/HGNC_11998`
     - Unresolved Gene: `.../gene/local/TP53_VARIANT`
     - Pathway: `.../pathway/HALLMARK_HYPOXIA`
     - CellType: `.../celltype/CL_0000235` (or context-qualified deterministic local slug).
3. **Mapping Tools & Ingestion**:
   - Karma R2RML models or RDFLib ingestion pipeline.
   - Graph serialization in Turtle (`.ttl`).
4. **Qualitative Evaluation**:
   - Table: Initial vs final entities considered and modeled.
   - Karma mapping iterations / RDFLib pipeline iterations.
   - Difficulties encountered (e.g., handling obsolete aliases without automated guessing, preserving tissue context columns, preventing empty URIs).
   - Remarks on LLM usage in Phase 4.

---

## 8. Section 7: Evaluation (`S7.tex`)

### Purpose
Provide comprehensive quantitative, ontological, data-quality, and query-based evaluation of the resulting Knowledge Graph.

### Mandatory Content
1. **Final KG Information Statistics**:
   - Summary table generated from `Evaluation/graph_statistics.json`:
     - Total RDF Triples.
     - Distinct Subjects and Objects.
     - Entity instance counts: `Gene`, `Pathway`, `CellType`, `Disease`.
     - Object property assertions: `participates_in`, `is_marker_for`.
     - Total unique symbols in MSigDB vs CellMarker.
     - Shared genes across MSigDB and CellMarker (by HGNC ID).
     - HGNC Resolution Rate:
       $$\text{Resolution Rate} = \frac{\text{Distinct Valid Symbols Resolved to HGNC}}{\text{Total Distinct Valid Source Symbols}} \times 100\%$$
2. **Knowledge Layer Evaluation**:
   - Structural consistency: class hierarchy, domain/range adherence, absence of dangling references.
   - Competency Question coverage: which CQs are answerable by the implemented queries (as measured).
   - Coverage metrics listed in the Phase 5 questionnaire (CQs vs dataset, dataset vs CQs, language-definition and knowledge-definition coverage), only if computed in `Evaluation/`, each with its formula written out (the example report uses ratios such as $|E_{CQ} \cap E_{DS}| / |E_{CQ}|$).
3. **Data Layer Evaluation**:
   - **Source-data completeness / missing-value rates**:
     $$\text{Missing-value rate} = \frac{\text{Missing values in column}}{\text{Total records parsed}} \times 100\%$$
     $$\text{Field completeness} = 100\% - \text{Missing-value rate}$$
     Reported for required columns vs optional columns (e.g., Cell Ontology ID).
   - **Entity Connectivity**:
     $$\text{Entity Connectivity} = \frac{\text{Distinct Connected Entities (Gene, Pathway, CellType, Disease)}}{\text{Total Entities (Gene, Pathway, CellType, Disease)}} \times 100\%$$
     Reported overall and per entity type, with the number of isolated entities per type as measured.
4. **Query Execution & Competency Validation**:
   - Evaluation of CQ1, CQ2, CQ3, CQ4.
   - Execution over:
     - Synthetic test graph with known ground truth (positive, no-match, empty list tests).
     - Real-data smoke tests on the production KG.
   - Query test success rate:
     $$\text{Query Success Rate} = \frac{\text{Passed Test Cases}}{\text{Total Test Cases}} \times 100\%$$
5. **Qualitative Evaluation**:
   - Highlights, unexpected findings, and remarks on LLM usage in Phase 5.

---

## 9. Section 8: Metadata (`S8.tex`)

### Purpose
Describe metadata for all intermediate and final project assets, ensuring FAIR compliance and enabling catalog distribution.

### Mandatory Content
1. **Resource Metadata Specifications**:
   - *Language Resources Metadata*: Language terms, lexical definitions, UKC concepts.
   - *Knowledge Resources Metadata*: OWL ontology schema, atom definitions.
   - *Data Resources Metadata*: Raw source filenames, retrieval dates, source URLs, licensing constraints.
   - *KG Dataset Metadata*: Embedded Turtle dataset node using:
     - `dcterms:title`, `dcterms:description`, `dcterms:created`, `dcterms:source`.
     - `dcterms:creator` (Agent resource), `dcterms:license`.
     - `owl:versionInfo`.
     - VoID properties: `void:triples`, `void:entities`, `void:classes`, `void:properties`, `void:distinctSubjects`, `void:distinctObjects`.
   - Present each group as a Field / Value table (the example report has "Project Metadata", "Language Metadata", "Knowledge Metadata" tables). Leave out or mark TODO any field whose value is not in `Metadata/` or given by the user.
2. **Catalog Distribution Plan**:
   - Target repositories: DataScientia LiveKnowledge catalog, Zenodo, GitHub.
   - Packaging of metadata tables as Excel/CSV for LiveKnowledge compatibility.
3. **Qualitative Evaluation**:
   - Metadata validation results and remarks on LLM usage.

---

## 10. Section 9: Open Issues & Conclusion (`S9.tex`)

### Purpose
Synthesize project achievements, evaluate schedule and scope adherence, and document unresolved issues and future directions.

### Mandatory Content
1. **Schedule Adherence**:
   - Comparison of planned timeline vs actual completion of the phases (dates supplied by the user).
2. **Satisfaction of Initial Purpose**:
   - Detailed review showing how CQ1–CQ4 fulfill the domain researchers' requirements.
3. **Open Issues and Limitations** (from the handover's known limitations; examples):
   - Handling unapproved alias symbols without risking incorrect biological inferences.
   - CellMarker records lacking Cell Ontology (CL) mappings.
   - Boundary condition: The current KG provides biological context but does not embed 2D/3D spatial coordinate graphs or cell-cell neighborhood graphs.
4. **Future Extensions** (clearly labelled as outside the current scope; examples):
   - Incorporating ligand-receptor interactions.
   - Integration with spatial transcriptomics libraries (e.g. Squidpy, Seurat).
5. **Remarks on LLM Usage in Phase 6**.

---

## 11. Appendix A: LLM Usage Questionnaire (`secA-Appendix.tex`)

Must record the user's CFS ratings (A–E) and their explanations for each completed phase (never chosen by the agent):
- Phase 1: Purpose Definition (Q1, Q2 part 1 a–i, Q2 part 2 a–g, Q2 part 3 a–f, Q3, Q4, Q5).
- Phase 2: Language Definition (Q1, Q2 a–i, Q3, Q4, Q5).
- Phase 3: Knowledge Definition (Q1, Q2 a–c, Q3, Q4, Q5).
- Phase 4: Entity Definition (Q1, Q2 a–i, Q3, Q4, Q5).
- Phase 5: Evaluation & Metadata (Q1, Q2 part 1 a–j, Q2 part 2 a–f, Q3, Q4, Q5).
- Phase 6: Open Problems & Conclusion (Q1, Q2 a–f, Q3, Q4, Q5).

---

## 12. Appendix B: Technical Appendix (`secB-Appendix.tex`)

### Purpose
Provide reproducible technical artifacts and reference code.

### Mandatory Content
1. Complete SPARQL listings for Query 1, Query 2, Query 3, and Query 4 with input parameters and expected output columns.
2. RDF schema excerpt in Turtle.
3. Sample output tables from competency queries.
