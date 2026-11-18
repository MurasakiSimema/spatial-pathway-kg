# 0. Decisions taken before starting Phase 2

*Taken on 2026-11-18, before any Phase 2 work. They follow the guide
`docs/2_language_definition.pdf`.*

| # | Question | Decision |
|---|---|---|
| L1 | Which Language Teleontology (LTLO) do we align to? | **Three tiers, as in the Oncovirus KG example:** first the **UKC** (Universal Knowledge Core); if the concept is not there, the **biomedical ontologies** of the project proposal (Cell Ontology, MONDO, GO, NCIt, Pathway Ontology, through OBO Foundry / NCBO BioPortal); if it is not there either, a **new concept** with a custom ID. Every ID is recorded with the resource it comes from and the date it was checked; MONDO is used from the local `mondo.owl`. A UKC concept may be skipped when its sense is too generic for the biological relation; the reason is written in the Language Resource Table (so far: `participatesIn`). |
| L2 | Which namespace and custom IDs? | Namespace of the language terms: **`http://knowdive.disi.unitn.it/etype#`**, prefix **`tpkg:`** (Transcriptomics Pathways KG). Custom concept IDs: **`TPKG26-01`, `TPKG26-02`, …** |
| L3 | Which naming convention? | **camelCase style:** classes in UpperCamelCase (`tpkg:Gene`, `tpkg:CellType`), object and data properties in lowerCamelCase (`tpkg:participatesIn`, `tpkg:isMarkerFor`, `tpkg:observedIn`, `tpkg:approvedSymbol`, `tpkg:tissueClass`), no `has` prefix. |
