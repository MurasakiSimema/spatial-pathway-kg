#!/usr/bin/env python3
"""
extract_metrics_to_latex.py

Reads Knowledge Graph statistics and query test outcomes from
Evaluation/graph_statistics.json and formats them as LaTeX tables for
Section 7 (Evaluation).

No value is ever invented: every value missing from the JSON is emitted as a
visible \\textbf{TODO} marker and listed on stderr, and the script exits with
status 2 if any value was missing (status 1 if the JSON cannot be read).

Expected JSON keys (all optional; missing ones become TODO):
    total_triples, gene_instances, pathway_instances, cell_type_instances,
    participates_in_triples, is_marker_for_triples, shared_hgnc_genes,
    hgnc_resolution_rate_percent,
    resolution_breakdown: [{source, resolved, not_found, non_approved,
                            ambiguous, invalid, rate}],
    connectivity: {gene_total, gene_connected, gene_connectivity_percent,
                   pathway_total, pathway_connected, pathway_connectivity_percent,
                   cell_type_total, cell_type_connected,
                   cell_type_connectivity_percent,
                   overall_total, overall_connected, overall_connectivity_percent},
    query_tests: [{id, desc, pos, neg, rate}]

Usage:
    python extract_metrics_to_latex.py [--json-path PATH] [--output-file PATH]
"""

import argparse
import json
import os
import sys

TODO = r"\textbf{TODO}"
missing = []


def latex_escape(text):
    text = str(text)
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\^{}")):
        text = text.replace(a, b)
    return text


def fmt(container, key, where, percent=False):
    """Format container[key]; record and return TODO if it is absent."""
    if not isinstance(container, dict) or container.get(key) is None:
        missing.append(f"{where}.{key}" if where else key)
        return TODO
    val = container[key]
    if isinstance(val, bool):
        out = str(val)
    elif isinstance(val, int):
        out = f"{val:,}"
    elif isinstance(val, float):
        out = f"{val:.2f}"
    else:
        out = latex_escape(val)
    return out + (r"\%" if percent and out != TODO else "")


def stats_table(stats):
    rows = [
        ("Total Triples", "Count of unique RDF triples in serialized Turtle graph", "total_triples", False),
        ("Gene Entities", "Gene instances (HGNC-resolved + flagged local)", "gene_instances", False),
        ("Pathway Entities", "Hallmark pathways from the MSigDB collection", "pathway_instances", False),
        ("CellType Entities", "CellMarker human cell-type resources", "cell_type_instances", False),
        (r"participates\_in", r"Gene $\rightarrow$ Pathway assertions", "participates_in_triples", False),
        (r"is\_marker\_for", r"Gene $\rightarrow$ CellType assertions", "is_marker_for_triples", False),
        ("Shared Genes", "HGNC IDs present in both MSigDB and CellMarker", "shared_hgnc_genes", False),
        ("HGNC Resolution Rate", "Resolved distinct valid symbols / distinct valid symbols", "hgnc_resolution_rate_percent", True),
    ]
    body = "".join(f"{m} & {d} & {fmt(stats, k, '', p)} \\\\ \\hline\n" for m, d, k, p in rows)
    return ("\\begin{table}[htbp]\n\\centering\n\\begin{tabularx}{\\linewidth}{|l|X|r|}\n\\hline\n"
            "\\textbf{Metric} & \\textbf{Operational Definition / Scope} & \\textbf{Value} \\\\ \\hline\n"
            + body +
            "\\end{tabularx}\n\\caption{Final Knowledge Graph Information Statistics}\n"
            "\\label{tab:kg_statistics}\n\\end{table}")


def resolution_table(rows):
    if not isinstance(rows, list) or not rows:
        missing.append("resolution_breakdown")
        rows = [{}]
    body = ""
    for i, r in enumerate(rows):
        w = f"resolution_breakdown[{i}]"
        cells = [fmt(r, "source", w)] + [fmt(r, k, w) for k in
                 ("resolved", "not_found", "non_approved", "ambiguous", "invalid", "rate")]
        body += " & ".join(cells) + " \\\\ \\hline\n"
    return ("\\begin{table}[htbp]\n\\centering\n\\begin{tabularx}{\\linewidth}{|X|r|r|r|r|r|r|}\n\\hline\n"
            "\\textbf{Source} & \\textbf{Resolved} & \\textbf{Not Found} & \\textbf{Non-Appr.} & "
            "\\textbf{Ambig.} & \\textbf{Invalid} & \\textbf{Rate} \\\\ \\hline\n"
            + body +
            "\\end{tabularx}\n\\caption{HGNC Gene Symbol Resolution Audit Breakdown}\n"
            "\\label{tab:hgnc_resolution}\n\\end{table}")


def connectivity_table(conn):
    if not isinstance(conn, dict):
        conn = {}
    w = "connectivity"
    body = ""
    for label, p in (("Gene", "gene"), ("Pathway", "pathway"), ("CellType", "cell_type"),
                     ("Disease", "disease"), (r"\textbf{Overall}", "overall")):
        body += (f"{label} & {fmt(conn, p + '_total', w)} & {fmt(conn, p + '_connected', w)} & "
                 f"{fmt(conn, p + '_connectivity_percent', w, True)} \\\\ \\hline\n")
    return ("\\begin{table}[htbp]\n\\centering\n\\begin{tabularx}{\\linewidth}{|X|r|r|r|}\n\\hline\n"
            "\\textbf{Entity Type} & \\textbf{Total Instances} & \\textbf{Connected} & "
            "\\textbf{Connectivity} \\\\ \\hline\n"
            + body +
            "\\end{tabularx}\n\\caption{Entity Connectivity Across Biological Object Properties}\n"
            "\\label{tab:entity_connectivity}\n\\end{table}")


def query_table(cases):
    if not isinstance(cases, list) or not cases:
        missing.append("query_tests")
        cases = [{}]
    body = ""
    for i, c in enumerate(cases):
        w = f"query_tests[{i}]"
        body += " & ".join(fmt(c, k, w) for k in ("id", "desc", "pos", "neg", "rate")) + " \\\\ \\hline\n"
    return ("\\begin{table}[htbp]\n\\centering\n\\begin{tabularx}{\\linewidth}{|l|X|l|l|r|}\n\\hline\n"
            "\\textbf{Query} & \\textbf{Competency Question} & \\textbf{Positive Test} & "
            "\\textbf{No-Match / Edge Test} & \\textbf{Success} \\\\ \\hline\n"
            + body +
            "\\end{tabularx}\n\\caption{Competency Query Validation}\n"
            "\\label{tab:query_eval}\n\\end{table}")


def main():
    parser = argparse.ArgumentParser(description="Convert KG metrics JSON into LaTeX tables.")
    parser.add_argument("--json-path", default=os.path.join("Evaluation", "graph_statistics.json"),
                        help="Path to graph_statistics.json")
    parser.add_argument("--output-file", default=None, help="Write LaTeX here (stdout if omitted)")
    args = parser.parse_args()

    try:
        with open(args.json_path, "r", encoding="utf-8") as f:
            stats = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"[X] Cannot read {args.json_path}: {e}", file=sys.stderr)
        print("    Run Phase 5 (evaluation) first; no tables are generated without real data.", file=sys.stderr)
        sys.exit(1)

    parts = [
        "% Generated from " + args.json_path.replace("\\", "/") + " by extract_metrics_to_latex.py",
        stats_table(stats),
        resolution_table(stats.get("resolution_breakdown")),
        connectivity_table(stats.get("connectivity")),
        query_table(stats.get("query_tests")),
    ]
    text = "\n\n".join(parts) + "\n"

    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"LaTeX tables written to {args.output_file}", file=sys.stderr)
    else:
        print(text)

    if missing:
        print(f"[!] {len(missing)} value(s) missing from the JSON, emitted as TODO:", file=sys.stderr)
        for m in missing:
            print(f"    - {m}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
