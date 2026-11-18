# 3. Data layer: filtering, cleaning, formatting

*Status: done on 2026-11-18 (Stage 2B). Written one dataset / one step at a time. Scripts are in
`Phase 4 - Entity Definition/src/`, outputs in `Phase 4 - Entity Definition/data/processed/`.
The raw files are never modified.*

## 3.1 Gene symbols: HGNC resolution

**Script:** `hgnc_resolution.py` (tests: `tests/test_hgnc_resolution.py`, 13 tests, all pass).
**Input:** `h.all.v2026.2.Hs.symbols.gmt`, `human_cell_marker.txt`, `hgnc_complete_set.txt`.
**Output:** `gene_symbol_resolution.csv`, one row per distinct symbol per source (62,147 rows),
with the original symbol, the normalized symbol, status, resolution method, HGNC ID, approved
symbol and name, candidates, warnings, and the CellMarker `gene_id`.

**Rules.**
- One normalization for every source: trim, then uppercase. It is only a matching key; the
  original spelling is kept.
- For CellMarker, the gene is taken from `symbol` when it is filled, otherwise from `marker`
  (Phase 1).
- A symbol is `resolved` when exactly one Approved HGNC entry has it as approved symbol;
  `non_approved_match` when it is only a previous or alias symbol; `ambiguous` with more than
  one approved candidate; `not_found`; `invalid` when blank or not a single word.
- All 45,326 HGNC records have status `Approved`; all HGNC IDs have the format `HGNC:n`.

**Results.**

| | MSigDB Hallmark | CellMarker 3.0 |
|---|---|---|
| Distinct symbols | 4,384 | 57,763 |
| Occurrences (gene–set pairs / records) | 7,322 | 1,779,944 |
| Resolved on the approved symbol | 4,383 | 30,615 |
| Resolved on a previous/alias symbol (D20) | 0 | 881 (11,557 records) |
| Non-approved match with more than one candidate | 0 | 20 (67 records) |
| Not found | 1 (`TARP`) | 25,952 (147,210 records) |
| Invalid | 0 | 295 (456 records) |
| Ambiguous | 0 | 0 |
| **Kept in the KG (D21)** | **4,383 symbols, 7,321 occurrences** | **31,496 symbols, 1,632,211 records (91.7%)** |

- The CellMarker symbols that are not found come almost all from the `marker` column (when
  `symbol` is empty): clone and locus names such as `AC092580.4` or `RP11-1143G9.4`, and
  protein markers such as `HLA-DR` or `CD45RA`. The invalid ones are free-text descriptions
  (e.g. `Acetylated tubulin`).
- 211 MSigDB and 731 CellMarker resolved symbols are also a previous or alias symbol of another
  HGNC entry: the approved-symbol resolution is kept and the case is flagged in the table.

**Mouse-style symbols (D19).** Checking the CellMarker `gene_id` against the HGNC `entrez_id`,
3,774 resolved symbols (11,371 records) have a `gene_id` that is not the human Entrez ID of the
gene. Almost all are written with mouse capitalization (e.g. `A2m`, CellMarker `gene_id`
232345, while human A2M is Entrez 2), although the file labels every record as Human.

### Decisions

| ID | Question | Decision |
|---|---|---|
| D19 | (2026-11-18) What about resolved symbols whose CellMarker `gene_id` is not the human Entrez ID (mostly mouse-style symbols)? | **Kept**, resolved on the human gene: the record is labelled Human and the symbol matches. Each case is flagged `gene_id_conflict` in the audit table and counted separately, so they can be excluded later. |
| D20 | Do we resolve previous/alias symbols? | **Only when there is exactly one candidate** (881 CellMarker symbols, 11,557 records), with `resolution_method = prev_or_alias` so they stay distinguishable. The 20 symbols with more than one candidate are not resolved. |
| D21 | What happens to genes that cannot be resolved (not found, multi-candidate aliases, invalid)? | **They are excluded from the KG**: only genes with an HGNC ID become `tpkg:Gene`. They stay in the audit table (`in_kg = no`). This removes `TARP` from `HALLMARK_ANDROGEN_RESPONSE` and 147,733 CellMarker records (8.3%). |

## 3.2 MSigDB Hallmark

**Script:** `prepare_msigdb.py`. **Input:** `h.all.v2026.2.Hs.symbols.gmt`, `gene_symbol_resolution.csv`.
**Output:** `pathways.csv` (`hallmarkId`, `label`, `sourceUrl`, `genesInSource`, `genesInKg`) and
`pathway_gene.csv` (`hallmarkId`, `hgncId`, `sourceSymbol`: the `participatesIn` links).

- **Filtering:** every field of the GMT file is used (identifier, URL, genes); only the genes
  without an HGNC ID are dropped (D21).
- **Formatting:** the 50 identifiers match `HALLMARK_[A-Z0-9_]+` and the 50 URLs start with
  `https://`; no format problem. The label is built by rule D23.
- **Results:** 50 pathways, **7,321 `participatesIn` links**, 4,383 distinct genes; no pathway–gene
  pair is duplicated after resolution. Pathway sizes stay 32–200 genes; only
  `HALLMARK_ANDROGEN_RESPONSE` goes from 101 to 100 genes (`TARP`).

## 3.3 CellMarker 3.0

**Script:** `prepare_cellmarker.py`. **Input:** `human_cell_marker.txt`, `gene_symbol_resolution.csv`.
**Output:** `cell_types.csv`, `cell_type_gene.csv` (the `isMarkerFor` links with their kind),
`cell_type_disease_source.csv` (input of the MONDO matching), `cellmarker_excluded_cl_ids.csv`.

- **Filtering:** all 1,779,944 records have `species = Human` (checked, none excluded). Of the 23
  columns, we keep `cell_name`, `tissue_class`, `disease_category`, `tissue_type`,
  `cell_name_class`, `cellontology_id`, `disease`, `symbol`/`marker` and `marker_source`
  (only to choose reported/predicted). The other columns (`pmid`, `year`, `method_details`,
  `title`, `journal`, `series_id`, `uberon_id`, `gene_id`, …) are not carried into the processed
  files (Phase 1, D16; `gene_id` is only used for the check of D19).
- **Duplicates (D3):** 88,979 rows are exact copies of another row (5.0%); they are collapsed,
  leaving **1,690,965 distinct records**.
- **Renamed columns:** `cell_name` → `cellName`, `tissue_class` → `tissueClass`,
  `disease_category` → `diseaseCategory`, `tissue_type` → `tissueType`, `cell_name_class` →
  `cellNameClass`, `cellontology_id` → `cellOntologyId`, `disease` → `sourceDiseaseName`.
- **Value formats:** 2,111 raw records write the CL ID as `CL:nnnnnnn` and are changed to
  `CL_nnnnnnn`. 14 distinct values (1,608 distinct records) are not valid CL IDs (UBERON IDs or
  CL IDs with the wrong number of digits) and are treated as missing; they are listed in
  `cellmarker_excluded_cl_ids.csv`. Empty CL IDs stay missing.
- **Consistency checks:** every `cell_name` has exactly one `cell_name_class`.
- **Results:**
  - 1,552,657 distinct records have a gene in the KG; 138,308 do not (D21).
  - **12,632 CellTypes**, of which **12,460 enter the KG** (D22).
  - **873,776 `isMarkerFor` links**: **101,897 reported** and **771,879 predicted** (D17); they
    involve 26,886 genes.
  - 14,812 (CellType, disease string) pairs with category other than Normal and 1,065 distinct
    disease strings; 14,730 pairs and 1,064 strings belong to a CellType of the KG.

*Recount of Phase 1 figures.* Phase 1 (D17) counted 977,460 links, 108,040 reported and 869,420
predicted, on the raw symbols and before HGNC resolution. After resolution and D21 the links
are 873,776 (101,897 reported, 771,879 predicted).

## 3.4 Genes

**Script:** `prepare_genes.py`. **Output:** `genes.csv` (`hgncId`, `approvedSymbol`, `approvedName`,
`sourceSymbol`, `hgncResolutionMethod`, `inMsigdb`, `inCellmarker`).

- **26,893 genes**: 4,376 in both sources (same HGNC ID), 7 only in MSigDB, 22,510 only in
  CellMarker.
- `hgncResolutionMethod`: 26,511 `approved_symbol`, 382 `prev_or_alias` (genes reached only
  through a unique previous/alias symbol, D20).
- 4,271 genes have more than one source spelling (e.g. upper case in MSigDB and mouse-style in
  CellMarker); all are kept in `sourceSymbol`.

## 3.5 Decisions of steps 3.2–3.4

| ID | Question | Decision |
|---|---|---|
| D3 | (open since Phase 1, closed 2026-11-18) Exact duplicate rows? | **Collapsed and counted:** after D16 the KG has no per-record data, so duplicates change no triple; 88,979 copies are reported. |
| D22 | CellTypes left without any marker gene after D21? | **Excluded:** a CellType enters the KG only if it has at least one `isMarkerFor` link (172 of 12,632 excluded; kept in `cell_types.csv` with `inKg = no`). |
| D23 | How is the Pathway label built? | The GMT file has no readable name, so: drop `HALLMARK_`, turn `_` into spaces, keep the source upper case (`HALLMARK_TNFA_SIGNALING_VIA_NFKB` → `TNFA SIGNALING VIA NFKB`). Acronyms stay correct. |

## 3.6 Diseases: matching to MONDO

**Script:** `mondo_matching.py` (tests: `tests/test_mondo_matching.py`, 12 tests, all pass).
**Input:** `cell_type_disease_source.csv` (only CellTypes of the KG, D22), `mondo.owl`
(release 2026-11-03). **Output:** `disease_mondo_matching.csv` (one row per disease string),
`diseases.csv`, `cell_type_disease.csv` (the `observedIn` links), `mondo_merges.csv`.

**Rules** (Phase 1, D9 and D13–D15, plus D24–D26 below).
- Normalization, the same on both sides: lower case, `tumour` → `tumor`, possessive `'s`
  removed, `- _ , /` → space, repeated spaces collapsed.
- Names used: `rdfs:label` and EXACT synonyms of non-obsolete MONDO classes. EXACT synonyms
  typed ABBREVIATION, AMBIGUOUS, DUBIOUS, DEPRECATED or NON_HUMAN are not used (6,571 synonyms),
  so an abbreviation alone never gives a match.
- A string is resolved when exactly one MONDO term has that name, on the full string or, if
  not, on the string without its final part in parentheses (`Lung adenocarcinoma (LUAD)` →
  `lung adenocarcinoma`). RELATED/NARROW/BROAD synonyms are recorded as candidates only.
- MONDO has 36,168 classes, 32,137 not obsolete; 8,319 non-human animal disease terms are not
  used (D24).

**Results** (1,064 disease strings of the KG CellTypes; records counted after D3).

| Status | Strings | Records |
|---|---|---|
| resolved | 562 | 554,287 (73.2%) |
| — on the full string | 536 | |
| — without the final parentheses | 26 | |
| related_only (RELATED/NARROW/BROAD synonym only) | 20 | 10,220 (1.3%) |
| ambiguous | 2 | 11 |
| no_match | 447 | 183,438 (24.2%) |
| non_disease (D14, D26) | 30 | 9,542 (1.3%) |
| rejected_merge (D25) | 3 | 69 |

- **517 Diseases** (distinct MONDO terms); 37 of them are reached by more than one string (all
  listed in `mondo_merges.csv`, e.g. `Gastric cancer`, `Stomach cancer`, `Gastric cancer
  (circulating)` → *gastric cancer*). The original strings are kept in `sourceDiseaseName`.
- **10,254 `observedIn` links**, involving 5,565 CellTypes. 1,429 of the 6,994 KG CellTypes with
  category Cancer or Disease have no `observedIn` link (all their disease strings are
  unresolved, D15).
- **Metastases (D13):** 32 strings mention a metastasis; 30 have no match. The 2 resolved ones
  (`Metastatic melanoma`, `Metastatic prostate cancer`) match a MONDO term of their own, not
  the primary cancer.
- The 2 remaining ambiguous strings are `Embryonal tumor with multilayered rosettes` and
  `Long QT syndrome` (two human MONDO terms each).

*Recount of Phase 1 figures.* The prototype of Phase 1 found 569 matched strings and 521
Diseases on the raw file. The pipeline gives 562 strings and 517 Diseases, on the strings of
the KG CellTypes, with D24–D26.

### Decisions of this step

| ID | Question | Decision |
|---|---|---|
| D24 | (2026-11-18) Do we use MONDO terms of non-human animal diseases? | **No**: the 8,319 terms under MONDO:0005583 (*non-human animal disease*) are left out, because CellMarker is human only. Without this, `Multiple myeloma` and `Myeloma` were ambiguous with *plasma cell myeloma, non-human animal*. |
| D25 | Review of the merges (strings reaching the same MONDO term)? | **All accepted except three**, where the string is broader than the term: `Primary antibody deficiency` (→ *common variable immunodeficiency*), `Lewy body disease` (→ *Lewy body dementia*), `Intervertebral disc disease` (→ *intervertebral disk degenerative disorder*). They are not resolved (status `rejected_merge`). |
| D26 | Completing the non-disease list (D14)? | **30 values**: the 5 of Phase 1 plus ageing (`Aging`, `Healthy brain aging`, `Skin aging`, `Skeletal muscle aging`, `Vascular ageing`), exposures (`Arsenic exposure`, `Human papillomavirus exposure`), viruses as organisms (`Ebola virus`, `Human immunodeficiency virus`, `Human immunodeficiency virus-1`, `Human papillomaviruses (HPV)`, `Herpes simplex virus type 2/3/4`, `SARS-CoV-2`, `Respiratory viruses`), procedures (`Heart`/`Kidney`/`Liver`/`Lung transplantation`, `Liver xenotransplantation`, `Pig-to-human kidney xenotransplantation`) and studies or states (`Ebola vaccine study`, `Spontaneous HIV-1 controller`, `Viral infection susceptibility`). None of them had a MONDO match, so the KG does not change; the audit now separates "not a disease" from "not in MONDO". |

## 3.7 Summary of the processed data

| Element | Count | File |
|---|---|---|
| Gene | 26,893 | `genes.csv` |
| Pathway | 50 | `pathways.csv` |
| CellType | 12,460 | `cell_types.csv` (`inKg = yes`) |
| Disease | 517 | `diseases.csv` |
| `participatesIn` | 7,321 | `pathway_gene.csv` |
| `isMarkerFor` (= reported + predicted) | 873,776 | `cell_type_gene.csv` |
| — `isReportedMarkerFor` | 101,897 | |
| — `isPredictedMarkerFor` | 771,879 | |
| `observedIn` | 10,254 | `cell_type_disease.csv` |

**Missing values in the kept attributes.** No Gene lacks an approved name, no Disease lacks a
label, and every KG CellType has a tissue type and a cell name class. 164 KG CellTypes have no
valid Cell Ontology ID (the attribute is optional); 669 have more than one, and 2,008 have more
than one tissue type (multi-valued, as planned in Phase 1).

**How to rerun** (from the repository root, in the project environment):

```text
python "Phase 4 - Entity Definition/src/hgnc_resolution.py"
python "Phase 4 - Entity Definition/src/prepare_msigdb.py"
python "Phase 4 - Entity Definition/src/prepare_cellmarker.py"
python "Phase 4 - Entity Definition/src/prepare_genes.py"
python "Phase 4 - Entity Definition/src/mondo_matching.py"
python "Phase 4 - Entity Definition/src/tests/test_hgnc_resolution.py"
python "Phase 4 - Entity Definition/src/tests/test_mondo_matching.py"
```
