# 4. Input Inspection (Information Gathering)

*Phase 1 (Purpose Definition), Stage 1B: information gathering.*
*Status: draft for review. We only read the raw files; none of them was modified.*

All our input files are in `Phase 4 - Entity Definition/data/raw/`. Where they come from, their
licences, and how to cite them is written in `SOURCES.md` and `cites.bib` in the same folder.
All the numbers below were computed from the files themselves on 2026-11-12, using `awk`,
`iconv`, and `file`. When we count records we do not count the header line.

## 4.1 Summary

| Source | File | Size | Format | Records | Encoding | Line endings |
|---|---|---|---|---|---|---|
| MSigDB Hallmark | `h.all.v2026.2.Hs.symbols.gmt` | 48,694 B | GMT (tab-separated, no header) | 50 gene sets | ASCII | LF |
| HGNC | `hgnc_complete_set.txt` | 16,994,064 B | TSV with header, 53 columns | 45,326 genes | UTF-8 (112 lines with non-ASCII characters) | LF |
| CellMarker 3.0 | `human_cell_marker.txt` | 577,624,367 B | TSV with header, 23 columns | 1,779,944 marker records | UTF-8 (we validated the whole file) | LF |

Every line has the same number of fields (53 for HGNC, 23 for CellMarker), so both files can be
read as plain TSV.

## 4.2 MSigDB Hallmark (`h.all.v2026.2.Hs.symbols.gmt`)

### Fields and missing values

A GMT file has no header: each line is one gene set, and the number of tab-separated fields
changes from line to line. By "missing" we mean an empty field.

| Field | Missing | Notes |
|---|---|---|
| 1 — gene-set name | 0 | 50 distinct values, all starting with `HALLMARK_` (e.g. `HALLMARK_HYPOXIA`); 16–42 characters |
| 2 — description | 0 | always a URL, `https://www.gsea-msigdb.org/gsea/msigdb/human/geneset/<NAME>`; there is no text description |
| 3+ — gene symbols | 0 | 32–200 genes per set; 7,322 gene–pathway memberships; 4,384 distinct symbols |

### Species

Human: the file name contains `Hs`, and all 50 URLs point to the `/human/` collection.

### Version

The file name says v2026.2. There is no version field inside the file, so we could not confirm
the version from the content.

### Gene symbols

**Quick check against HGNC:** 4,383 of the 4,384 distinct symbols are current HGNC approved
symbols. **Only one symbol, `TARP`, does not match any approved, previous, or alias symbol.**

### Duplicates

No gene appears twice in the same set, and no set name is repeated.

## 4.3 HGNC (`hgnc_complete_set.txt`)

### Columns and missing values

The file has 53 columns. In the table we list the ones we need to resolve genes (AGENT.md
§4.3) and the descriptive columns we looked at. By "missing" we mean an empty field.

| Column | Missing | Notes |
|---|---|---|
| `hgnc_id` | 0 | 45,326 distinct values (unique), e.g. `HGNC:5` |
| `symbol` | 0 | 45,326 distinct values (unique), e.g. `A1BG` |
| `name` | 0 | approved name, e.g. `alpha-1-B glycoprotein` |
| `locus_group` | 0 | `protein-coding gene` 19,299; `pseudogene` 14,671; `non-coding RNA` 10,352; `other` 1,004 |
| `locus_type` | 0 | 23 distinct values |
| `status` | 0 | always `Approved`; see below |
| `alias_symbol` | 22,653 (50.0%) | can contain more than one value; see below |
| `prev_symbol` | 32,609 (71.9%) | can contain more than one value; see below |
| `date_modified` | 96 (0.2%) | latest value `2026-11-05` |
| the other 44 columns (gene groups, dates, Entrez, Ensembl, UniProt, …) | — | out of scope (AGENT.md §3.3), we do not import them |

### Status

All 45,326 records have `status = Approved`. Since the file has no withdrawn entries, we cannot
use it to trace withdrawn symbols.

### Release

The file has no version field. The paper describing this release was published in October
2026.

### Multi-valued fields

`prev_symbol` and `alias_symbol` are lists separated by `|` and wrapped in double quotes, e.g.
`"NCRNA00181|A1BGAS|A1BG-AS"`. 12,717 rows have at least one previous symbol and 22,673 have at
least one alias. We only use them for diagnostics when resolving genes (Phase 2).

### Duplicates

`hgnc_id` and `symbol` are both unique (0 duplicates).

## 4.4 CellMarker 3.0 (`human_cell_marker.txt`)

### Columns and missing values

By "missing" we mean an empty field. We did not find any `NA`/`nan` strings.

| Column | Missing | Notes |
|---|---|---|
| `species` | 0 | always `Human` |
| `tissue_class` | 0 | 138 distinct values |
| `tissue_type` | 0 | 482 distinct values |
| `uberon_id` | 101,872 (5.7%) | does not match `tissue_type` one-to-one (607 type/ID pairs) |
| `disease_category` | 0 | `Normal` 954,305; `Cancer` 492,514; `Disease` 333,125 |
| `disease` | 0 | |
| `cell_name_class` | 0 | 248 distinct values |
| `cell_name` | 0 | 3,190 distinct values |
| `cellontology_id` | 3,482 (0.2%) | 713 distinct values; see the problems below |
| `marker` | 0 | the marker as written in the original study |
| `symbol`, `gene_id`, `gene_type`, `gene_name` | 161,509 (9.1%) each | always missing together; `gene_id` is an Entrez ID saved as a float (e.g. `55120.0`) |
| `uniprot_id` | 286,093 (16.1%) | |
| `technology_seq` | 21,801 (1.2%) | |
| `marker_source` | 0 | see below |
| `pmid`, `title`, `journal`, `year` | 88,351 (5.0%) each | always missing together; years go from 1978 to 2026 |
| `series_id`, `method_details` | 141,967 (8.0%) each | |

### Species

All 1,779,944 records have `species = Human`. We downloaded the human file, so we do not need
to filter by species.

### Marker evidence (`marker_source`)

| `marker_source` | Records | Share |
|---|---|---|
| Method | 1,635,971 | 91.9% |
| Single-cell sequencing | 95,087 | 5.3% |
| Experiment | 40,360 | 2.3% |
| Review | 5,648 | 0.3% |
| Company | 2,878 | 0.2% |

For the `Method` records, `method_details` gives the name of a computational tool that detects
markers: COSG, CelliD, FindAllMarker, Cepo, SEMITONES, Spapros. These are the *computationally
predicted* markers mentioned in the title of the CellMarker 3.0 paper (`hu2026cellmarker`). The
other sources are the manually curated part. **Decision D1:** we keep all records and keep
track of their source.

### Gene symbols

- `gene_type`: most records are `protein_coding` (1,494,492). The rest are lncRNA (73,706),
  immunoglobulin/T-cell receptor segments, pseudogenes, and small RNAs.
- In 58,515 records where `symbol` is filled in, `marker` and `symbol` are different. This means
  CellMarker has already normalized part of the markers.
- **Quick check of the `symbol` column against HGNC:** there are 30,761 distinct symbols. 26,314
  are HGNC approved symbols, **4,447 are not**. Of these, 3,725 differ from an approved symbol
  only in upper/lower case (e.g. `Plp1`, written the mouse way). The other 722 will have to be
  resolved through previous symbols and aliases (Phase 2).
- **Records without `symbol`:** they contain 27,002 distinct `marker` values. 176 are approved
  HGNC symbols, 132 are previous symbols, and 513 are aliases. **26,181 do not match anything in
  HGNC.** Some examples: clone/contig names (`RP11-1143G9.4`, `AC092580.4`), names of complexes
  (`HLA-DR`), and old names (`C15orf48`).

### Cell types and Cell Ontology

- There are 3,190 distinct `cell_name` values, 713 distinct `cellontology_id` values, and 3,955
  distinct (name, ID) pairs. So **cell names and CL IDs do not match one-to-one**: for example
  `Macrophage` appears with 24 different CL IDs, and `Monocyte` with 9. We decided how to handle
  this in decision D2.
- **Badly formatted `cellontology_id` values:**
  - 4 cell names use the colon form `CL:0000765` instead of `CL_0000765` (`Erythroblast`,
    `Neuroepithelial cell`, `Chromaffin cell`, `Interneuron`);
  - 12 (name, ID) pairs have a UBERON ID in the CL column, e.g. `Venous endothelial cell` →
    `UBERON_0001919`.

### Duplicates

70,731 distinct lines appear more than once in the file (identical in all 23 columns). We will
decide how to handle duplicates in Phase 2, and we will log the counts (AGENT.md §5.4).

## 4.5 Do the sources cover our CQs?

| CQ | What we need | Where we find it | Covered |
|---|---|---|---|
| CQ1, CQ1.2 | pathway → genes; HGNC ID and approved name | GMT; HGNC `hgnc_id`, `name` | yes |
| CQ2, CQ2.1 | gene → pathways | GMT | yes |
| CQ2.2, CQ3.1 | gene → cell types, tissue filter | CellMarker `symbol`/`marker`, `cell_name`, `tissue_class` | yes |
| CQ3, CQ3.3 | pathway genes ∩ cell-type marker genes | GMT + CellMarker, joined through HGNC | yes, once both sides are resolved to HGNC |
| CQ4, CQ4.1, CQ4.2 | pathway groups (query input) → shared genes (+ markers) | GMT (+ CellMarker) | yes |

The sources we collected cover all the approved CQs. As the guide says, this means we do not
need to go back and look for other sources.

### Checking the examples in the scenarios

- The pathways used in S1 and S3 exist: `HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION`,
  `HALLMARK_HYPOXIA`, `HALLMARK_INTERFERON_GAMMA_RESPONSE`.
- `MYC` (S5) is in 10 Hallmark pathways.
- `CD74` (S6) is an approved HGNC symbol (`HGNC:1697`, *CD74 molecule*), has 1,249 CellMarker
  records, and belongs to 3 Hallmark pathways (`ALLOGRAFT_REJECTION`,
  `INTERFERON_ALPHA_RESPONSE`, `INTERFERON_GAMMA_RESPONSE`). At first we had used `CD68`, but
  `CD68` is a marker that belongs to no Hallmark pathway, so we replaced it (decision D4).

## 4.6 How we plan to parse the files

1. Read the GMT file line by line, splitting on tabs: field 1 is the pathway identifier, field 2
   the source URL, fields 3+ the gene symbols.
2. Read HGNC and CellMarker as UTF-8 TSV with a header, and pick the columns by **name**, not by
   position. Remove the double quotes from `prev_symbol` / `alias_symbol` before splitting on
   `|`.
3. To resolve CellMarker genes against HGNC, use `symbol` when it is there and `marker`
   otherwise, and keep the original string for audit.
4. Keep tissue (`tissue_class`, `tissue_type`) and disease (`disease_category`, `disease`) as
   literals of CellType (`tissue_class` and `disease_category` are part of its identity key,
   decision D5). Do not map them to UBERON or to disease ontologies.
5. Change `CL:nnnnnnn` into `CL_nnnnnnn`; treat IDs in `cellontology_id` that are not CL IDs as
   missing, and log them.
6. Never drop records without saying so: every excluded or unresolved record is counted and
   logged.

## 4.7 Decisions

| ID | Question | What we decided |
|---|---|---|
| D1 | Do we include the computationally predicted markers (`marker_source = Method`, 91.9%)? | **Yes:** we include all records and keep `marker_source` (and `method_details`) as attributes of the marker evidence, so queries can be limited to curated markers. |
| D2 | What identifies a CellType: `cell_name`, `cellontology_id`, or the pair? | **`cell_name`**; the CL IDs become an attribute that can have more than one value. |
| D3 | What do we do with exact duplicate records (collapse them with a count, or keep them)? | Still open, to be decided in Phase 2. |
| D4 | Which example gene do we use in scenario S6? | **`CD74`** instead of `CD68`. |
| D5 | How do we bring the context into the model while keeping three ETypes and two relations? | CellType identity key = (`cell_name`, `tissue_class`, `disease_category`), which gives 12,632 CellTypes; `disease` and `tissue_type` are kept as literals that can have more than one value. See `05_concept_identification.md`. |
