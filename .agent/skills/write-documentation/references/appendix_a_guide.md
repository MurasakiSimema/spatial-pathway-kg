# Appendix A: LLM Usage Questionnaire Guide

`secA-Appendix.tex` contains the standardized **LLM Usage Questionnaire** defined by the KnowDive / DataScientia group to evaluate the degree, nature, and reliability of Large Language Model assistance throughout each phase of the iTelos engineering lifecycle.

This guide explains the Common Frequency Scale (CFS), lists the questions and subtasks per phase, and shows the LaTeX layout.

> **The ratings are the authors' answers about their own LLM use.** The agent must ask the user for each rating and comment and must not pick them. This guide deliberately gives no suggested ratings.

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
| **Q3** | Output Verification | How frequently the generated outputs were checked against ground-truth source files or unit tests. |
| **Q4** | Hallucinations / Errors Found | How frequently errors, invented identifiers, malformed URIs, or hallucinated biological links were identified. |
| **Q5** | Completion Assistance | How helpful LLM assistance was in successfully reaching the phase milestones. |

---

## 3. Phase-by-Phase Task Breakdown

### Phase 1: Purpose Definition
- **Q2 Part 1 (Purpose & Requirements)**:
  - `a. Clarifying the informal purpose`
  - `b. Defining the domain of interest, space, and time`
  - `c. Generating scenarios`
  - `d. Generating personas`
  - `e. Drafting competency questions`
  - `f. Identifying concepts, ETypes, attributes, and relationships`
  - `g. Drafting or refining the ER diagram`
  - `h. Qualitative evaluation and refinement of the purpose`
  - `i. Other`
- **Q2 Part 2 (Data Source Exploration)**:
  - `a. Identifying data sources`
  - `b. Writing Python scripts for extraction, merging, or cleaning`
  - `c. Handling missing fields and duplicate records`
  - `d. Cross-referencing identifiers`
  - `e. Producing cleaned datasets`
  - `f. Qualitative evaluation of data sources and preprocessing`
  - `g. Other`
- **Q2 Part 3 (Schema & Ontology Exploration)**:
  - `a. Searching schemas and ontologies to reuse`
  - `b. Aligning ETypes with external ontologies`
  - `c. Defining attributes and data types`
  - `d. Resolving schema conflicts or ambiguities`
  - `e. Deciding when to use original dataset schema instead of external ontology terms`
  - `f. Other`

### Phase 2: Language Definition
- **Q2 Task List**:
  - `a. Identifying concepts, relationships, and attributes`
  - `b. Searching the Universal Knowledge Core`
  - `c. Searching external ontologies for definitions and IDs`
  - `d. Writing glosses and definitions for the Language Resource Table`
  - `e. Creating custom identifiers per KnowDive Identifier format`
  - `f. Building the language teleontology in Protégé`
  - `g. Defining object and data property terms`
  - `h. Qualitative evaluation of the language definition`
  - `i. Other`

### Phase 3: Knowledge Definition
- **Q2 Task List**:
  - `a. Creating the seed set of ETypes`
  - `b. Formalising ETypes as subclasses`
  - `c. Setting IRIs and annotations`

### Phase 4: Entity Definition
- **Q2 Task List**:
  - `a. Entity matching across datasets`
  - `b. Entity identification and unique identifier selection`
  - `c. Mapping datasets to the teleontology in Karma`
  - `d. Generating RDF Turtle files and R2RML models`
  - `e. Importing data and mapping to form RDF`
  - `f. Knowledge Graph visualisation`
  - `g. Fixing mapping issues such as hasAnnotation or path prefix problems`
  - `h. Qualitative evaluation of entity definition`
  - `i. Other`

### Phase 5: Evaluation & Metadata
- **Q2 Part 1 (Evaluation & Queries)**:
  - `a. Writing SPARQL queries for the competency questions`
  - `b. Running SPARQL queries`
  - `c. Interpreting query results`
  - `d. Calculating CQs vs dataset coverage`
  - `e. Calculating dataset vs CQs coverage`
  - `f. Calculating language definition coverage`
  - `g. Calculating knowledge definition coverage`
  - `h. Calculating connectivity and sparsity`
  - `i. Writing the evaluation section`
  - `j. Other`
- **Q2 Part 2 (Metadata & Packaging)**:
  - `a. Creating project metadata`
  - `b. Creating language metadata`
  - `c. Creating knowledge metadata`
  - `d. Packaging metadata as Excel files`
  - `e. Ensuring compatibility with LiveKnowledge`
  - `f. Other`

### Phase 6: Open Problems & Conclusion
- **Q2 Task List**:
  - `a. Summarising the project`
  - `b. Identifying open problems`
  - `c. Discussing limitations`
  - `d. Proposing future work`
  - `e. Writing the conclusion`
  - `f. Other`

---

## 4. Required LaTeX Formatting in `secA-Appendix.tex`

To ensure clean formatting in LaTeX, format each phase with an enumerated list specifying both the letter and CFS label (every `<...>` is filled with the user's own answer):

```latex
\section*{Phase 1: Purpose Definition}
\begin{enumerate}
  \item[\textbf{Q1.}] \textbf{<rating given by the user>} -- <user's comment>
  \item[\textbf{Q2.}] \textbf{Phase-Specific Tasks}:
  \begin{enumerate}
    \item[\textbf{Part 1:}]
    \begin{itemize}
      \item[a.] \textbf{<rating given by the user>} -- <user's comment>
      \item[b.] \textbf{<rating given by the user>} -- <user's comment>
      \item[c.] \textbf{<rating given by the user>} -- <user's comment>
      \item[d.] \textbf{<rating given by the user>} -- <user's comment>
      \item[e.] \textbf{<rating given by the user>} -- <user's comment>
      \item[f.] \textbf{<rating given by the user>} -- <user's comment>
      \item[g.] \textbf{<rating given by the user>} -- <user's comment>
      \item[h.] \textbf{<rating given by the user>} -- <user's comment>
      \item[i.] \textbf{<rating given by the user>} -- <user's comment>
    \end{itemize}
    ...
  \end{enumerate}
  \item[\textbf{Q3.}] \textbf{<rating given by the user>} -- <user's comment>
  \item[\textbf{Q4.}] \textbf{<rating given by the user>} -- <user's comment>
  \item[\textbf{Q5.}] \textbf{<rating given by the user>} -- <user's comment>
\end{enumerate}
```
