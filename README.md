# Interpretation of Pathways from Spatial Transcriptomics

A purpose-driven Knowledge Graph (KG) designed to support the biological interpretation of spatial transcriptomics analyses by integrating human genes, biological pathways, human cell-type marker annotations, and the diseases in which those cell types are reported.

---

## 🎯 Purpose & Scope

Spatial transcriptomics enables the study of gene expression while preserving information about the spatial organization of tissues. Interpreting spatial patterns is particularly challenging at **tissue frontiers**—boundary zones where different cellular microenvironments meet and distinct cell populations or biological processes overlap.

This project builds an integrated, queryable Knowledge Graph to provide biological context for spatial transcriptomics results by connecting:
- **Human Genes**: Identified and normalized via the official HGNC standard.
- **Biological Pathways**: The 50 well-defined gene sets from the **MSigDB Hallmark** collection.
- **Cell Types**: Human cell-type marker profiles from **CellMarker 3.0**.
- **Diseases**: The diseases in which CellMarker reports each cell type, grounded in the **Mondo Disease Ontology (MONDO)** when an exact match exists.

> [!NOTE]
> The Knowledge Graph is descriptive and exploratory. It provides biological context and identifies gene overlaps; it does not directly process raw image/coordinate matrices, nor does it infer causal mechanisms or assume pathway activity.

---

## ❓ Competency Questions

The Knowledge Graph is engineered to answer four core competency questions:

1. **CQ1**: Which human genes are associated with each of the 50 MSigDB Hallmark biological pathways?
2. **CQ2**: Which biological pathways contain a given human gene?
3. **CQ3**: Which cell types have marker genes in common with the genes of a selected biological pathway?
4. **CQ4**: Which genes are shared between pathways identified as *activated* and pathways identified as *suppressed* from an upstream spatial transcriptomics analysis?

---

## 📚 Core Resources

- **MSigDB Hallmark Gene Sets**: 50 curated biological pathways representing specific, coherent biological states or processes ([MSigDB](https://www.gsea-msigdb.org/gsea/msigdb/)).
- **CellMarker 3.0**: Curated human cell-type markers across tissue and disease contexts ([CellMarker](http://bio-bigdata.hrbmu.edu.cn/CellMarker/)).
- **HGNC (HUGO Gene Nomenclature Committee)**: Authoritative resource for human gene symbols, identifiers, and normalization ([HGNC](https://www.genenames.org/)).
- **MONDO (Mondo Disease Ontology)**: Reference ontology used to identify the diseases reported by CellMarker ([MONDO](http://purl.obolibrary.org/obo/mondo.owl)).

Reference ontologies considered for conceptual grounding include the Gene Ontology (GO), Cell Ontology (CL), Pathway Ontology (PW), and OBO Foundry registries.

---

## 🏗️ Repository Layout (iTelos Methodology)

The project follows the **iTelos** Knowledge Graph engineering methodology developed by the KnowDive / DataScientia group (University of Trento):

```text
spatial-pathway-kg/
├── docs/                                # Step-by-step PDF methodological guides
├── Documentation/                       # Academic report (LaTeX) & KnowDive template
├── Phase 1 - Purpose Definition/        # Scenarios, personas, CQs, and informal ER models
├── Phase 2 - Language Definition/       # Language Resource Table (LRT) & lexical alignments
├── Phase 3 - Knowledge Definition/      # Teleology ontology atoms & schema alignments
├── Phase 4 - Entity Definition/         # Data ingestion, entity mapping, and RDF generation
├── Evaluation/                          # Quantitative graph metrics & SPARQL CQ validation
├── Metadata/                            # Resource catalog metadata (DC Terms, VoID)
├── .agent/                              # Automated agent skills & helper workflows
└── README.md                            # Project overview and reference guide
```

---

## 📈 Project Status

This project is currently in the definition and specification phase and is developed incrementally following the iTelos lifecycle. Pipeline scripts, RDF graphs, and validation metrics will be integrated into their respective phase directories as development advances.
