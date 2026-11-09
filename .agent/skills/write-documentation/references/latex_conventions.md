# LaTeX Conventions, Styling & Compilation Guide

This guide details the technical requirements, styling rules, typography, and compilation workflow for the KnowDive / DataScientia LaTeX report template.

---

## 1. Document Architecture & File Layout

The LaTeX documentation is located in `Documentation/`:

```text
Documentation/
├── Template_KG2026_report-pdf.pdf   # Reference PDF specification
├── knowdive-files/                  # Preamble, class, bib, and images
│   ├── knowdive.cls                 # Custom LaTeX class file
│   ├── knowdive.bst                 # BibTeX bibliography style
│   ├── KnowDivePubs.bib             # Bibliography database
│   ├── main.tex                     # Master LaTeX file
│   ├── DS-logo-new.png              # Header logo
│   ├── DataScientia_DataStrip-01.png# Footer banner
│   ├── DataScientia_DataStrip-02.png# Alternate banner
│   ├── DS_color_bar.png             # Decorative bar
│   ├── knowDiveUNITN.png            # Unitn logo
│   └── Knowdive_color_bar.png       # Alternate bar
└── section/                         # Modular section files included by main.tex
    ├── S1.tex                       # Section 1: Introduction
    ├── S2.tex                       # Section 2: Project Design
    ├── S3.tex                       # Section 3: Purpose Definition
    ├── S4.tex                       # Section 4: Language Definition
    ├── S5.tex                       # Section 5: Knowledge Definition
    ├── S6.tex                       # Section 6: Entity Definition
    ├── S7.tex                       # Section 7: Evaluation
    ├── S8.tex                       # Section 8: Metadata
    ├── S9.tex                       # Section 9: Open Issues
    ├── secA-Appendix.tex            # Appendix A: LLM Usage Questionnaire
    └── secB-Appendix.tex            # Appendix B: Technical Appendices
```

---

## 2. Preamble & Document Class (`knowdive.cls`)

### 2.1 Engine & Typography
- The document class `knowdive.cls` uses `\usepackage{fontspec}` and sets:
  ```latex
  \setsansfont{Arial}
  \setmainfont{Arial}
  ```
- **Required TeX Engine**: **XeLaTeX** (or **LuaLaTeX**). Traditional `pdflatex` will fail on `fontspec`.
- Margins: 2 cm on left, top, and right (`geometry` package).
- Line spacing: $1.5$ line spacing (`\onehalfspacing` via `setspace`).

### 2.2 Preamble Macros in `main.tex`
- **Title**:
  ```latex
  \title{Spatial Transcriptomics Knowledge Graph: \\ iTelos Purpose-Driven Knowledge Graph Report}
  ```
- **Author**:
  ```latex
  \author{First Author \and Second Author}
  ```
- **Revision History**:
  ```latex
  \revisionhistory{
      \revision{0.1}{20.04.2020}{Fausto Giunchiglia}{Document created}
      \revision{0.2}{12.01.2022}{Fausto Giunchiglia}{Document template simplified}
      \revision{0.3}{30.10.2026}{Mayukh Bagchi}{KG - 2026 - Project Report Template}
      \revision{1.0}{09.11.2026}{Implementation Team}{Final project report}
  }
  ```
- **Title Page Generation**:
  `\maketitle` automatically generates:
  - DataScientia logo (`DS-logo-new.png`)
  - Title and authors
  - Copyright and confidentiality notice
  - Table of Contents (`\tableofcontents`)
  - Revision history table
  - Sets the page counter to 0

---

## 3. Formatting Guidelines

### 3.1 Tables
Use `tabularx` with `X` columns for wrapped text:
```latex
\begin{table}[htbp]
\centering
\begin{tabularx}{\linewidth}{|l|X|r|}
\hline
\textbf{Metric} & \textbf{Operational Definition} & \textbf{Value} \\ \hline
Total Triples & Total distinct RDF triples in production graph & 48,291 \\ \hline
Gene Entities & Distinct human genes normalized via HGNC & 4,120 \\ \hline
Resolution Rate & Resolved symbols / valid distinct source symbols & 96.4\% \\ \hline
\end{tabularx}
\caption{Knowledge Graph Final Information Statistics}
\label{tab:kg-stats}
\end{table}
```

### 3.2 Code Listings (SPARQL & Turtle)
Use the `listings` package:
```latex
\begin{lstlisting}[language=SPARQL, caption={Query 1: Retrieving genes in a Hallmark pathway}, label={lst:q1}]
PREFIX : <https://w3id.org/spatial-kg/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?gene ?hgncId ?symbol ?name WHERE {
  ?gene a :Gene ;
        :participates_in ?pathway .
  ?pathway :hasHallmarkId "HALLMARK_HYPOXIA" .
  OPTIONAL { ?gene :hgncId ?hgncId . }
  OPTIONAL { ?gene :approvedSymbol ?symbol . }
  OPTIONAL { ?gene :approvedName ?name . }
}
\end{lstlisting}
```

### 3.3 Mathematical Formulas
Always use standard math environments (`equation`, `align*`, or `\[ ... \]`):
```latex
\[
\text{Entity Connectivity (\%)} = \frac{|\mathcal{E}_{\text{connected}}|}{|\mathcal{E}_{\text{total}}|} \times 100\%
\]
```

### 3.4 Citations & Bibliography
- Bibliography file: `Documentation/knowdive-files/KnowDivePubs.bib`
- Style file: `Documentation/knowdive-files/knowdive.bst`
- Citations:
  - `\cite{p1}`: Stratified data integration (Giunchiglia et al. 2021)
  - `\cite{p2}`: Popularity driven data integration (Giunchiglia et al. 2022)
  - `\cite{p3}`: iTelos--Purpose Driven Knowledge Graph Generation (Giunchiglia et al. 2021)
  - `\cite{p4}`: Language and knowledge representation (Bagchi 2025)
  - `\cite{p5}`: About me and you--iTelos (Bocca 2025)
  - `\cite{p6}`: Representation heterogeneity (Giunchiglia & Bagchi 2022)

---

## 4. Compilation Workflow

Because `main.tex` is located in `Documentation/knowdive-files/` while section files are located in `Documentation/section/`:

### Recommended Compilation from Project Root:
```powershell
cd Documentation
# Ensure XeLaTeX has access to both knowdive-files and section:
xelatex -output-directory=knowdive-files knowdive-files/main.tex
bibtex knowdive-files/main
xelatex -output-directory=knowdive-files knowdive-files/main.tex
xelatex -output-directory=knowdive-files knowdive-files/main.tex
```

Alternatively, use the helper script:
```powershell
python .agents/skills/write-documentation/scripts/check_compilation.py
```
This script audits LaTeX syntax, validates environments, verifies BibTeX keys, and runs the compiler if available.
