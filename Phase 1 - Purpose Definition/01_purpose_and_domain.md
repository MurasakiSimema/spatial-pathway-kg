# 1. Purpose and Domain of Interest

*Phase 1 (Purpose Definition), Stage 1A: purpose formalization.*
*Status: draft for review.*

## 1.1 Informal purpose

We started from the purpose written in our project proposal (`docs/0_project_summary.pdf`).
In short, it says:

> Support the interpretation of spatial transcriptomics data by integrating information about
> human genes, biological pathways, and cell types into a unified, queryable Knowledge Graph.
> The KG connects the MSigDB Hallmark collection with human cell-type marker information from
> CellMarker, using HGNC as the source of gene identity. It exposes the overlap between
> pathway genes and cell-type marker genes as biological context for pathways observed in
> different tissue regions or at tissue frontiers, without assuming that a pathway is active in
> a cell type. It also supports comparing pathways identified as activated and as suppressed by
> an upstream spatial transcriptomics analysis, by finding the genes the two groups share.

## 1.2 Refined purpose

After discussing it, we rewrote the purpose in one statement that says more precisely what the
KG has to do:

> Build a reproducible Knowledge Graph that links **human genes** (identified through HGNC) to
> the **50 MSigDB Hallmark pathways** they belong to and to the **human cell types** for which
> CellMarker reports them as markers. A researcher who has already run a spatial
> transcriptomics analysis can use it to look up which genes make up a pathway, which pathways
> a gene belongs to, which cell types share marker genes with a pathway, and which genes are
> shared between a set of activated and a set of suppressed pathways.

One thing we want to be clear about from the start: our KG is **descriptive and exploratory**.
If a pathway and a cell type share some genes, this is only context that helps the
interpretation. It does not show that the pathway is active in that cell type, it does not
prove which cells are there, it is not a statistical enrichment result, and it does not say
anything about causality.

## 1.3 Domain of Interest

Our domain is molecular and cellular biology, but only two aspects of it: which human genes
belong to which gene sets (pathways), and which human genes are used as markers of which cell
types. We care about these because they are what people use to interpret spatial
transcriptomics results.

The KG comes *after* the spatial analysis and does not contain any spatial data. The questions
it answers, though, come from spatial work: for example, a pathway that scores high on one side
of a tissue frontier and low on the other.

## 1.4 Context

As the guide suggests, we describe the context along three dimensions: space, time, and domain.

### Space

- **Organism:** only *Homo sapiens*. We use the human Hallmark collection, HGNC (which only
  covers human genes), and the human marker file of CellMarker.
- **Biological space:** the tissues and cell types annotated in CellMarker. We keep tissue and
  disease information as attributes of the cell types (see decision D5 in
  `05_concept_identification.md`), not as separate entities.
- **What we do not cover:** spatial coordinates, tissue images, spots, regions, or expression
  matrices. The KG never sees raw spatial transcriptomics data.

### Time

**Our temporal scope is the knowledge published from 1978 to 2026, as it appears in the 2026
releases of the three sources, which we downloaded on 2026-11-05.**

| Source | Temporal reference | Where we got it from |
|---|---|---|
| MSigDB Hallmark | Collection defined in 2015 (Liberzon et al., *Cell Systems* 2015); file release v2026.2 | Citation `liberzon2015molecular`; the release comes from the file name and had to be confirmed in Stage 1B |
| HGNC | Gene nomenclature as of our download on 2026-11-05 (resource described in Seal et al., *NAR* 2026) | `SOURCES.md`; citation `seal2026genenames` |
| CellMarker 3.0 | Marker evidence from studies published **1978–2026**; resource released in 2026 (Hu et al., *NAR* 2026) | `year` column of `human_cell_marker.txt`; citation `hu2026cellmarker` |

To get the CellMarker range we looked at the `year` column (1,779,944 records):

- the oldest year is 1978 and the newest is 2026;
- about 99.7% of the records that have a year come from studies published in **2016–2026**;
  2020 alone has 646,189 records;
- **88,351 records (≈5.0%) have no year**. We keep them anyway, since a missing year is not a
  good reason to throw away a marker. How we handle them is described in Stage 1B.

What this means for our KG:
- the KG is a **snapshot** of what the three sources say in their 2026 releases. If someone
  wants it up to date, they have to rebuild it on newer releases;
- we do **not model time as an entity or a relation**: no biological states that change over
  time, no history of gene membership, no marker versions. The publication year of a
  CellMarker record is at most a descriptive attribute of the marker evidence (we decided this
  in concept identification).

### Domain boundaries

What is in scope:
- three entity types: **Gene**, **Pathway**, **CellType**;
- two biological relations: Gene **participates in** Pathway, and Gene **is marker for**
  CellType;
- HGNC information (HGNC ID, approved symbol, approved name) as attributes of Gene, only for
  genes that appear in MSigDB Hallmark or CellMarker.

What is out of scope:
- cell states, diseases as entities, and causal relations (promotes / suppresses);
- pathway or GO enrichment, statistical inference of pathway–cell-type associations,
  pathway–pathway crosstalk;
- machine-learning or predictive models;
- other pathway collections (KEGG, Reactome, other MSigDB collections) and other datasets
  (e.g. Open Targets);
- HGNC genes that do not appear in either source, and HGNC fields other than identity and
  name;
- deciding which pathways are activated or suppressed: the user gives us these lists as
  **inputs** when running a query.
