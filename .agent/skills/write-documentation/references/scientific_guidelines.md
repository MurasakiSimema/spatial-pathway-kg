# Scientific Guidelines, Scope Boundaries & Phrasing Rules

When authoring the project documentation report, the agent must strictly enforce the scientific boundaries, negative constraints, and precise biological terminology established in [AGENT.md](../../../../AGENT.md).

---

## 1. Strict Scope Boundaries

### 1.1 Principal Entity Types
The Knowledge Graph models **exactly four** principal entity classes (Disease was added with the scope change of 2026-11-13):
1. `Gene`: Human genetic entities normalized through HGNC.
2. `Pathway`: Biological pathways represented by the 50 gene sets in the MSigDB Hallmark collection.
3. `CellType`: Human cell types characterized by marker genes in CellMarker 3.0.
4. `Disease`: Diseases in which CellMarker reports a cell type, grounded in MONDO when an exact match exists.

*Negative Rule*: Do **not** introduce additional entity classes such as `CellState`, `Tissue`, `Protein`, or `SpatialSpot`. Tissue context from CellMarker is retained as literal properties or context qualifiers of `CellType`, never as separate entity nodes. CellMarker `disease` values that are not diseases (e.g. `Undefined`, vaccines, viruses) are not `Disease` instances.

### 1.2 Main Biological Object Properties
The Knowledge Graph asserts **only three** main biological relationships:
1. `participates_in` — Domain: `Gene`, Range: `Pathway`.
2. `is_marker_for` — Domain: `Gene`, Range: `CellType`.
3. `observed_in` — Domain: `CellType`, Range: `Disease`.

*Phrasing rule for `observed_in`*: it means that CellMarker has at least one record of the cell type in that disease. It is attached to the CellType, not to single markers: never write that the overlapping marker genes were observed in the disease, and never present it as a disease mechanism or a disease–gene association.

*Negative Rule*: Do **not** declare causal or regulatory relations such as `promotes`, `suppresses`, `activates`, `inhibits`, or `regulates`.

### 1.3 Role of HGNC
- HGNC (`hgnc_complete_set.txt`) is exclusively an **authority reference for identifier resolution and symbol normalization**.
- It is **not** a content dataset.
- Never import genes from HGNC into the KG unless they already occur in MSigDB Hallmark or CellMarker.
- Never model HGNC records as a separate entity class.
- In the same way, MONDO is a reference for disease identity: import only the MONDO terms matched by CellMarker diseases, and never model MONDO records as a separate class.

### 1.4 Spatial Transcriptomics Boundary
- The KG provides **biological contextualization** to assist researchers interpreting spatial transcriptomics data.
- The KG does **not**:
  - Store or analyze physical 2D or 3D spatial coordinates ($x, y, z$).
  - Store histology or microscopy images.
  - Process raw spatial spot expression matrices or count matrices.
  - Determine spatial spot boundaries or tissue frontiers.

---

## 2. Scientific Phrasing Rules & Negative Constraints

The table below contrasts acceptable phrasing with forbidden over-claims:

| Context | DO USE (Acceptable Phrasing) | DO NOT USE (Forbidden Phrasing) |
|:---|:---|:---|
| **Pathway–Cell Type Overlap** | *"shares marker genes with"*, *"shows gene overlap with"*, *"has overlapping marker genes"* | *"the pathway is active in this cell type"*, *"proves pathway activation"*, *"demonstrates cell identity"* |
| **Biological Interpretation** | *"provides biological context for further interpretation"*, *"descriptive overlap"* | *"proves cell presence in the tissue frontier"*, *"demonstrates causality"*, *"explains tissue architecture"* |
| **Gene-Pathway Link** | *"participates in the pathway gene set"*, *"is a member of the gene set"* | *"is upregulated by the pathway"*, *"causes the pathway to fire"* |
| **Statistical Association** | *"descriptive marker gene overlap"* | *"statistically significant pathway enrichment"*, *"GSEA enrichment demonstrated"* |
| **Pathway States (CQ4)** | *"genes shared between externally supplied activated and suppressed pathway lists"* | *"the KG determines which pathways are activated or suppressed"* |
| **Gene Identification** | *"gene identifier normalized via HGNC approved symbol match"* | *"HGNC proved functional expression in the tissue"* |
| **External Links** | *"conservatively linked via `rdfs:seeAlso`"* | *"asserted identical via `owl:sameAs`"* |

---

## 3. Data Integrity & Resolution Rules

### 3.1 HGNC Resolution Categories
Every source gene symbol must be classified into exactly one of five explicit categories:
1. `resolved`: Matches a unique approved HGNC symbol. The stable identifier is the HGNC ID (`HGNC:\d+`).
2. `not_found`: No match in the HGNC dataset.
3. `non_approved_match`: Matches only previous symbols, aliases, or withdrawn entries. *Must not be resolved automatically.*
4. `ambiguous`: Matches multiple HGNC entries.
5. `invalid`: Blank or malformed symbol string.

*Policy for Unresolved Genes*: Unresolved genes must **not** be silently dropped. They are instantiated as `Gene` resources under a separate local URI namespace (e.g. `.../gene/local/<symbol>`), retaining their literal resolution status for transparent filtering.

### 3.2 CellMarker Context Handling
- CellMarker may contain context columns (for example tissue, cancer/disease status, cell name). Use the column names actually found in the supplied file, as recorded in the input inspection.
- If identical cell-type names have distinct marker profiles in different tissue contexts, do not pool them into a single context-free entity without documenting the policy.
- Retain tissue context as literal datatype properties on the `CellType` entity.
- If a valid Cell Ontology CURIE is present (`CL:\d{7}`), link to OBO PURL `http://purl.obolibrary.org/obo/CL_\d{7}` using `rdfs:seeAlso`; describe it as a reference to the canonical concept, not as identity with a context-qualified CellType.

---

## 4. Query Semantics & Evaluation Rules

### Query 1: Genes in a Pathway
- **Input**: Hallmark pathway identifier or URI.
- **Output**: Genes linked via `participates_in`, approved HGNC symbols, HGNC IDs, and resolution status for unresolved genes.

### Query 2: Pathways for a Gene
- **Input**: Gene symbol, HGNC ID, or URI.
- **Output**: Hallmark pathways linked via `participates_in`.
- **Constraint**: Symbol lookup must use exact normalized matching; if ambiguous, report all candidate matches.

### Query 3: Pathway–Cell Type Overlap
- **Input**: One or more Hallmark pathway identifiers.
- **Output**: Pathway, CellType, distinct shared genes, and count of shared genes.
- **Grouping Rule**: Results must be grouped by **both** Pathway and CellType. Do not aggregate multiple selected pathways into a single union count without user request.
- **Interpretation Rule**: The count represents *descriptive shared marker genes*, not biological enrichment.

### Query 4: Shared Genes between Activated and Suppressed Pathway Groups
- **Input**: Two externally supplied lists: activated pathways and suppressed pathways.
- **Output**: Genes participating in at least one pathway from each group.
- **Boundary Rule**: The KG does not infer activation/suppression. If either list is empty, the query wrapper must return an empty result safely without executing an invalid query.

---

## 5. Metadata Rules

- Use Dublin Core Terms (`dcterms`) and VoID only with their standard semantics.
- Do not invent author, license, or creation dates:
  - If a creator is listed, model as an Agent resource or document in the handover.
  - If a license is unknown, report it as unstated; do not invent CC-BY or MIT.
- For VoID statistics, clearly specify whether ontology schema terms and metadata nodes are included in `void:triples` or `void:entities`.
