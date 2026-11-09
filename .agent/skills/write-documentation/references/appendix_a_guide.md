# Appendix A: LLM Usage Questionnaire Guide

`secA-Appendix.tex` contains the standardized **LLM Usage Questionnaire** defined by the KnowDive / DataScientia group to evaluate the degree, nature, and reliability of Large Language Model assistance throughout each phase of the iTelos engineering lifecycle.

This guide provides the scoring rubric, interpretation of the Common Frequency Scale (CFS), and guidelines for completing every question across all 6 phases.

---

## 1. The Common Frequency Scale (CFS)

All questions (Q1, Q2 subtasks, Q3, Q4, Q5) must be rated using one of the five standard CFS levels:

- **A. Never (0%)**: The LLM was not used or the phenomenon was never observed.
- **B. Rarely (1%–20%)**: LLM assistance was sought or observed on rare, isolated occasions.
- **C. Sometimes (21%–50%)**: LLM assistance was used intermittently for specific sub-problems.
- **D. Often (51%–80%)**: LLM assistance was the primary driver for executing the task, subject to human/agent review.
- **E. Always (81%–100%)**: The task was systematically conducted with continuous LLM generation or verification.

---

## 2. Standard Frequency Questions

For each phase, the following 5 standard questions must be addressed:

| Question | Focus | Evaluation Guideline |
|:---|:---|:---|
| **Q1** | Overall Usage Frequency | Overall proportion of phase effort that involved LLM prompting or generation. |
| **Q2** | Task-Specific Frequency | Detailed rating (A–E) for each subtask in the phase list. |
| **Q3** | Output Verification | How frequently the generated outputs were checked against ground-truth source files or unit tests. In rigorous agentic pipelines, this should be **E. Always**. |
| **Q4** | Hallucinations / Errors Found | How frequently errors, invented identifiers, malformed URIs, or hallucinated biological links were identified. |
| **Q5** | Completion Assistance | How helpful LLM assistance was in successfully reaching the phase milestones. |

---

## 3. Phase-by-Phase Task Breakdown & Scoring Guidance

### Phase 1: Purpose Definition
- **Q2 Part 1 (Purpose & Requirements)**:
  - `a. Clarifying the informal purpose`: Rating D/E. LLM refines user prompts into structured objectives.
  - `b. Defining the domain of interest, space, and time`: Rating D. Formulates spatial/temporal bounds.
  - `c. Generating scenarios`: Rating D/E. Drafts realistic biological usage scenarios.
  - `d. Generating personas`: Rating D/E. Constructs profiles of computational biologists and bioinformaticians.
  - `e. Drafting competency questions`: Rating D/E. Formulates CQ1–CQ4 in precise terms.
  - `f. Identifying concepts, ETypes, attributes, and relationships`: Rating D. Extracts Gene, Pathway, CellType.
  - `g. Drafting or refining the ER diagram`: Rating C/D. Specifies entity cardinalities and attributes.
  - `h. Qualitative evaluation and refinement of the purpose`: Rating C/D. Tabulates initial vs final counts.
  - `i. Other`: N/A or Rating A.
- **Q2 Part 2 (Data Source Exploration)**:
  - `a. Identifying data sources`: Rating C. Locating MSigDB, CellMarker, and HGNC.
  - `b. Writing Python scripts for extraction, merging, or cleaning`: Rating D/E. Writing parsers.
  - `c. Handling missing fields and duplicate records`: Rating D. Parsing audits and summary logic.
  - `d. Cross-referencing identifiers`: Rating D. Designing HGNC resolution logic.
  - `e. Producing cleaned datasets`: Rating D.
  - `f. Qualitative evaluation of data sources and preprocessing`: Rating C/D.
  - `g. Other`: Rating A.
- **Q2 Part 3 (Schema & Ontology Exploration)**:
  - `a. Searching schemas and ontologies to reuse`: Rating C/D. Identifying OBO Cell Ontology, Dublin Core, VoID.
  - `b. Aligning ETypes with external ontologies`: Rating C/D.
  - `c. Defining attributes and data types`: Rating D.
  - `d. Resolving schema conflicts or ambiguities`: Rating C/D.
  - `e. Deciding when to use original dataset schema instead of external ontology terms`: Rating D.
  - `f. Other`: Rating A.

### Phase 2: Language Definition
- **Q2 Task List**:
  - `a. Identifying concepts, relationships, and attributes`: Rating D.
  - `b. Searching the Universal Knowledge Core`: Rating C.
  - `c. Searching external ontologies for definitions and IDs`: Rating C/D.
  - `d. Writing glosses and definitions for the Language Resource Table`: Rating D/E. Writing unambiguous biological definitions.
  - `e. Creating custom identifiers per KnowDive Identifier format`: Rating C.
  - `f. Building the language teleontology in Protégé`: Rating B/C.
  - `g. Defining object and data property terms`: Rating D.
  - `h. Qualitative evaluation of the language definition`: Rating C/D.
  - `i. Other`: Rating A.

### Phase 3: Knowledge Definition
- **Q2 Task List**:
  - `a. Creating the seed set of ETypes`: Rating D. Formalizing Gene, Pathway, CellType.
  - `b. Formalising ETypes as subclasses`: Rating C/D. Structuring OWL classes and hierarchy.
  - `c. Setting IRIs and annotations`: Rating D. Assigning labels, comments, and domains/ranges.

### Phase 4: Entity Definition
- **Q2 Task List**:
  - `a. Entity matching across datasets`: Rating D/E. Matching gene symbols to HGNC approved symbols.
  - `b. Entity identification and unique identifier selection`: Rating D. Enforcing HGNC ID stability.
  - `c. Mapping datasets to the teleontology in Karma`: Rating C/D. Designing R2RML mappings.
  - `d. Generating RDF Turtle files and R2RML models`: Rating D/E. Writing RDFLib serialization code.
  - `e. Importing data and mapping to form RDF`: Rating D. Running batch graph population.
  - `f. Knowledge Graph visualisation`: Rating B/C.
  - `g. Fixing mapping issues such as hasAnnotation or path prefix problems`: Rating D. Resolving URI minting bugs.
  - `h. Qualitative evaluation of entity definition`: Rating C/D.
  - `i. Other`: Rating A.

### Phase 5: Evaluation & Metadata
- **Q2 Part 1 (Evaluation & Queries)**:
  - `a. Writing SPARQL queries for the competency questions`: Rating E. Drafting Q1–Q4 templates.
  - `b. Running SPARQL queries`: Rating D. Executing RDFLib queries.
  - `c. Interpreting query results`: Rating D. Analyzing pathway overlaps and shared genes.
  - `d. Calculating CQs vs dataset coverage`: Rating D.
  - `e. Calculating dataset vs CQs coverage`: Rating D.
  - `f. Calculating language definition coverage`: Rating C/D.
  - `g. Calculating knowledge definition coverage`: Rating C/D.
  - `h. Calculating connectivity and sparsity`: Rating D/E. Computing metric formulas.
  - `i. Writing the evaluation section`: Rating D/E. Synthesizing results in LaTeX.
  - `j. Other`: Rating A.
- **Q2 Part 2 (Metadata & Packaging)**:
  - `a. Creating project metadata`: Rating D. Formulating Dublin Core and VoID blocks.
  - `b. Creating language metadata`: Rating C/D.
  - `c. Creating knowledge metadata`: Rating C/D.
  - `d. Packaging metadata as Excel files`: Rating C.
  - `e. Ensuring compatibility with LiveKnowledge`: Rating C.
  - `f. Other`: Rating A.

### Phase 6: Open Problems & Conclusion
- **Q2 Task List**:
  - `a. Summarising the project`: Rating E. Synthesizing achievements against objectives.
  - `b. Identifying open problems`: Rating D. Articulating alias resolution and CL mapping limits.
  - `c. Discussing limitations`: Rating D. Explaining absence of raw spatial coordinates.
  - `d. Proposing future work`: Rating D. Recommending spatial neighborhood graph integrations.
  - `e. Writing the conclusion`: Rating E. Authoring final concluding narrative.
  - `f. Other`: Rating A.

---

## 4. Required LaTeX Formatting in `secA-Appendix.tex`

To ensure clean formatting in LaTeX, format each phase with an enumerated list specifying both the letter and CFS label:

```latex
\section*{Phase 1: Purpose Definition}
\begin{enumerate}
  \item[\textbf{Q1.}] \textbf{D. Often} -- The LLM was employed frequently to draft scenarios, personas, and formulate competency questions.
  \item[\textbf{Q2.}] \textbf{Phase-Specific Tasks}:
  \begin{enumerate}
    \item[\textbf{Part 1:}]
    \begin{itemize}
      \item[a.] \textbf{E. Always} -- Clarifying the informal purpose.
      \item[b.] \textbf{D. Often} -- Defining domain of interest in space and time.
      \item[c.] \textbf{E. Always} -- Generating realistic biological scenarios.
      \item[d.] \textbf{E. Always} -- Formulating detailed researcher personas.
      \item[e.] \textbf{E. Always} -- Drafting formal competency questions CQ1--CQ4.
      \item[f.] \textbf{D. Often} -- Identifying Core, Common, and Contextual eTypes.
      \item[g.] \textbf{D. Often} -- Specifying the Purpose ER model relationships.
      \item[h.] \textbf{C. Sometimes} -- Tabulating initial vs final purpose metrics.
      \item[i.] \textbf{A. Never} -- Other.
    \end{itemize}
    ...
  \end{enumerate}
  \item[\textbf{Q3.}] \textbf{E. Always} -- All LLM-generated definitions and questions were strictly audited against biological literature and AGENT.md.
  \item[\textbf{Q4.}] \textbf{C. Sometimes} -- Initial suggestions included non-human entities and unsupported causal relations, which were eliminated.
  \item[\textbf{Q5.}] \textbf{E. Always} -- Crucial for rapid requirement formalization and structural alignment.
\end{enumerate}
```
