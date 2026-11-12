# 2. Personas and Scenarios

*Phase 1 (Purpose Definition), Stage 1A: purpose formalization.*
*Status: draft for review.*

> **Note.** These personas and scenarios are made up, following the persona technique of the
> iTelos course. Each persona stands for a group of users. They are not real people, and the
> scenarios are not real studies or real results. The gene, pathway, and tissue names are just
> plausible examples (we checked that they exist in our data, see Stage 1B).

## 2.1 Personas

We imagined four people who could use our KG:

| ID | Name | Role | Age | Main need | Related scenarios |
|---|---|---|---|---|---|
| P1 | Dr. Laura Ferri | Spatial transcriptomics bioinformatician | 34 | Turn pathway scores at a tissue frontier into a biological reading | S1, S4 |
| P2 | Dr. Marco Ferretti | Tumour immunologist (wet lab) | 41 | Check which cell types could explain a pathway signal near a tumour border | S3 |
| P3 | Giulia Neri | MSc student in bioinformatics | 24 | Learn what the Hallmark pathways contain and look up single genes | S2, S5 |
| P4 | Dr. Chiara Bassi | Molecular pathologist | 47 | Verify that a gene seen in an image-based panel is a known marker, and find its pathways | S6 |

### P1 — Dr. Laura Ferri, spatial transcriptomics bioinformatician

- **Who she is:** she runs the computational analysis of spatial transcriptomics experiments
  in a core facility. Her pipeline splits the tissue into clusters, finds the frontiers between
  them, and scores the 50 Hallmark pathways in each region. The output is a list of
  *activated* and *suppressed* pathways, but nothing tells her what they mean biologically.
- **Tools:** workstation, Python/R, access to a SPARQL endpoint.
- **Needs:** competence, autonomy (she does not want to search the literature by hand for every
  pathway).
- **What she wants from the KG:** for a frontier, see the genes behind each pathway and find the
  genes shared by the activated and suppressed groups. A shared gene is worth a closer look,
  because it contributes to signals going in opposite directions.

### P2 — Dr. Marco Ferretti, tumour immunologist

- **Who he is:** he works at the bench on the tumour microenvironment. He gets results from a
  bioinformatician (like P1) and has to decide which cell types to stain for in the next
  experiments.
- **Tools:** laptop, web query interface; he does not write code.
- **Needs:** bridging (going from pathway names to cell types he can actually test), and
  trusting the sources.
- **What he wants from the KG:** given a pathway that changes across a tumour border, find the
  cell types whose marker genes overlap with it. This helps him pick candidates, keeping in mind
  that an overlap is a hint and not evidence of activity.

### P3 — Giulia Neri, MSc student in bioinformatics

- **Who she is:** she is new to gene-set analysis. She is writing her thesis on a public spatial
  dataset and keeps running into Hallmark names without knowing what is inside them.
- **Tools:** laptop, Python, SPARQL (still learning).
- **Needs:** curiosity, competence.
- **What she wants from the KG:** browse what each Hallmark pathway contains and, starting from
  a gene that came up in her analysis, find all the Hallmark pathways that include it.

### P4 — Dr. Chiara Bassi, molecular pathologist

- **Who she is:** she reviews targeted, image-based spatial panels on tissue sections. These
  panels measure only a few hundred genes, so she reasons one gene at a time.
- **Tools:** hospital PC, web query interface.
- **Needs:** security (reliable, traceable identifiers), competence.
- **What she wants from the KG:** for a gene that stands out in a tissue region, confirm its
  official HGNC identity, see which cell types it marks in that tissue, and see which pathways
  it belongs to.

## 2.2 Scenarios

Each scenario is told by the persona, in their own words.

### S1 — Reading a tissue frontier (P1)

"My pipeline flagged the frontier between a tumour cluster and the surrounding stroma. On the
tumour side, *Epithelial–mesenchymal transition* and *Hypoxia* score high. Before I write
anything about it, I want to see which genes make up these two pathways, so I can check which
of them are actually in my panel."

### S2 — Learning the Hallmark collection (P3)

"My supervisor keeps saying *'look at the Hallmarks'*. I want the full list of the 50 pathways
and, for each one, its genes and their official names, so I understand what a pathway score
is actually measuring."

### S3 — From a pathway to candidate cell types (P2)

"The bioinformatician tells me *Interferon gamma response* goes up along the invasive border.
I need to know which cell types have markers among the genes of this pathway, ideally only
markers reported in the right tissue. Then I can choose which cell populations to stain for. I
know an overlap does not mean those cells are the source of the signal."

### S4 — Activated versus suppressed pathways (P1)

"Across the frontier I have three activated pathways and two suppressed ones. I want the genes
that appear in at least one pathway of each group. Those genes contribute to signals moving in
opposite directions, so they are the first ones I check in the raw expression data."

### S5 — A single gene, many pathways (P3)

"*MYC* came up in my differential expression results. Which Hallmark pathways contain it? I
want to see whether its effect could be read through more than one pathway."

### S6 — Checking a panel gene (P4)

"In the image-based panel, the gene labelled *CD74* lights up in one region. I want to confirm
its approved HGNC symbol and ID, see which cell types it is a marker for in the tissue I am
looking at, and see the pathways it belongs to."

## 2.3 Which scenario needs which CQ

This table links each scenario to the competency questions it needs (the CQs are in
`03_competency_questions.md`):

| Scenario | Persona | Competency questions |
|---|---|---|
| S1 | P1 | CQ1 |
| S2 | P3 | CQ1, CQ1.2 |
| S3 | P2 | CQ3, CQ3.1, CQ3.3 |
| S4 | P1 | CQ4, CQ4.1, CQ4.2 |
| S5 | P3 | CQ2, CQ2.1 |
| S6 | P4 | CQ2, CQ2.2 |
