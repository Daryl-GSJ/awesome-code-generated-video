#!/usr/bin/env python3
"""Generate README-ready charts and a statistical summary from repository JSON.

Usage:
    python scripts/generate_charts.py

All counts are computed from data/papers.json and data/resources.json. The script
intentionally contains presentation rules, but no hard-coded statistical values.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, PercentFormatter


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSET_DIR = ROOT / "assets"
ANALYSIS_PATH = ROOT / "analysis.md"
DPI = 200

# Colorblind-friendly blue/green system used consistently across all figures.
COLORS = {
    "navy": "#174A6E",
    "blue": "#2C7FB8",
    "sky": "#7FCDBB",
    "green": "#2CA25F",
    "mint": "#B8E3D5",
    "pale": "#E8F3F1",
    "gray": "#AAB7C4",
    "dark": "#253746",
    "grid": "#DCE5EA",
}
RELEVANCE_ORDER = ["core", "support", "adjacent"]
RELEVANCE_COLORS = {
    "core": COLORS["navy"],
    "support": COLORS["blue"],
    "adjacent": COLORS["sky"],
}
RESOURCE_COLORS = [
    COLORS["navy"], COLORS["blue"], COLORS["green"],
    COLORS["sky"], COLORS["mint"], COLORS["gray"],
]

# Verifier-like means feedback tied to executable, rendered, structural, symbolic,
# metric, rule, test, or state evidence rather than feedback in the broad sense.
VERIFIER_KEYWORDS = (
    "compil", "execution", "runtime", "render", "lint", "test", "schema",
    "validation", "verification", "verifier", "metric", "rule", "check",
    "geometry", "constraint", "predicate", "simulation", "state", "pixel",
    "equivalence", "parameter error", "objective", "qa checklist", "static",
    "play-test", "reward", "reversion", "integrity", "physics",
)


def load_records(path: Path, key: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load and minimally validate a repository JSON collection."""
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    records = payload.get(key)
    if not isinstance(records, list):
        raise ValueError(f"{path}: expected a list at key {key!r}")
    ids = [record.get("id") for record in records]
    if any(not item for item in ids):
        raise ValueError(f"{path}: every record must have a non-empty id")
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path}: duplicate ids detected")
    return records, payload


def set_style() -> None:
    """Apply a restrained, GitHub-friendly static chart style."""
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.family": "DejaVu Sans",
        "font.size": 9.5,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "axes.labelcolor": COLORS["dark"],
        "axes.edgecolor": COLORS["grid"],
        "xtick.color": COLORS["dark"],
        "ytick.color": COLORS["dark"],
        "text.color": COLORS["dark"],
        "legend.fontsize": 9,
    })


def clean_axes(ax: plt.Axes, grid_axis: str = "x") -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis=grid_axis, color=COLORS["grid"], linewidth=0.8, alpha=0.8)
    ax.set_axisbelow(True)


def add_bar_labels(ax: plt.Axes, bars: Iterable[Any], horizontal: bool = False) -> None:
    """Label bars with discrete counts using point offsets."""
    for bar in bars:
        if horizontal:
            value = int(round(bar.get_width()))
            ax.annotate(
                f"{value:,}",
                xy=(bar.get_x() + bar.get_width(), bar.get_y() + bar.get_height() / 2),
                xytext=(6, 0), textcoords="offset points", ha="left", va="center",
                fontsize=9, fontweight="bold", color=COLORS["dark"],
            )
        else:
            value = int(round(bar.get_height()))
            if value:
                ax.annotate(
                    f"{value:,}",
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height()),
                    xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                    fontsize=8.5, fontweight="bold", color=COLORS["dark"],
                )


def save(fig: plt.Figure, filename: str) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(ASSET_DIR / filename, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_papers_by_year(papers: list[dict[str, Any]]) -> None:
    years = sorted({int(paper["year"]) for paper in papers})
    counts = {rel: Counter() for rel in RELEVANCE_ORDER}
    for paper in papers:
        counts[paper["relevance"]][int(paper["year"])] += 1

    peak_year = max(years, key=lambda year: sum(counts[rel][year] for rel in RELEVANCE_ORDER))
    peak_count = sum(counts[rel][peak_year] for rel in RELEVANCE_ORDER)

    fig, ax = plt.subplots(figsize=(10.8, 6.2), dpi=DPI, constrained_layout=True)
    bottoms = [0] * len(years)
    for rel in RELEVANCE_ORDER:
        values = [counts[rel][year] for year in years]
        bars = ax.bar(
            [str(year) for year in years], values, bottom=bottoms,
            color=RELEVANCE_COLORS[rel], label=rel.title(), width=0.68,
        )
        for index, bar in enumerate(bars):
            if values[index] >= 3:
                ax.annotate(
                    str(values[index]),
                    xy=(bar.get_x() + bar.get_width() / 2, bottoms[index] + values[index] / 2),
                    ha="center", va="center", color="white", fontsize=8.5, fontweight="bold",
                )
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    for index, total in enumerate(bottoms):
        ax.annotate(
            f"{total}", xy=(index, total), xytext=(0, 7), textcoords="offset points",
            ha="center", va="bottom", fontsize=9, fontweight="bold",
        )
    ax.set_title(f"Publication coverage peaks in {peak_year} with {peak_count} cataloged papers", pad=14)
    ax.set_xlabel("Publication year", labelpad=10)
    ax.set_ylabel("Papers", labelpad=10)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, max(bottoms) * 1.17)
    clean_axes(ax, "y")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.24), ncol=3, frameon=False)
    save(fig, "papers_by_year.png")


def plot_representation_landscape(papers: list[dict[str, Any]]) -> Counter:
    representation_counts = Counter(
        representation
        for paper in papers
        for representation in paper.get("representation", [])
    )
    top = representation_counts.most_common(12)
    labels = [label for label, _ in reversed(top)]
    values = [value for _, value in reversed(top)]
    leader, leader_count = top[0]

    fig, ax = plt.subplots(figsize=(10.8, 7.2), dpi=DPI, constrained_layout=True)
    colors = [COLORS["green"] if label == leader else COLORS["blue"] for label in labels]
    bars = ax.barh(labels, values, color=colors, height=0.68)
    add_bar_labels(ax, bars, horizontal=True)
    ax.set_title(f"{leader} is the most frequent executable representation ({leader_count} papers)", pad=14)
    ax.set_xlabel("Paper–representation incidences (multi-label)", labelpad=10)
    ax.set_ylabel("")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlim(0, max(values) * 1.18)
    clean_axes(ax, "x")
    save(fig, "representation_landscape.png")
    return representation_counts


def is_verifier_like(feedback: list[str]) -> bool:
    text = " ".join(feedback).lower()
    return any(keyword in text for keyword in VERIFIER_KEYWORDS)


def feedback_stats(papers: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    groups: dict[str, list[dict[str, Any]]] = {"All papers": papers}
    groups.update({
        rel.title(): [paper for paper in papers if paper["relevance"] == rel]
        for rel in RELEVANCE_ORDER
    })
    result: dict[str, dict[str, int]] = {}
    for group, records in groups.items():
        verifier = sum(is_verifier_like(record.get("feedback", [])) for record in records)
        broad_only = sum(
            bool(record.get("feedback", [])) and not is_verifier_like(record.get("feedback", []))
            for record in records
        )
        none = len(records) - verifier - broad_only
        result[group] = {
            "total": len(records),
            "verifier": verifier,
            "broad_only": broad_only,
            "none": none,
        }
    return result


def plot_feedback_coverage(papers: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    stats = feedback_stats(papers)
    groups = list(stats)
    categories = [
        ("Verifier-like checks", "verifier", COLORS["navy"]),
        ("Other reported feedback", "broad_only", COLORS["sky"]),
        ("No feedback listed", "none", COLORS["pale"]),
    ]
    overall = stats["All papers"]
    any_feedback_pct = 100 * (overall["verifier"] + overall["broad_only"]) / overall["total"]
    verifier_pct = 100 * overall["verifier"] / overall["total"]

    fig, ax = plt.subplots(figsize=(10.8, 5.8), dpi=DPI, constrained_layout=True)
    left = [0.0] * len(groups)
    for label, key, color in categories:
        values = [100 * stats[group][key] / stats[group]["total"] for group in groups]
        bars = ax.barh(groups, values, left=left, color=color, label=label, height=0.62)
        for index, (bar, value) in enumerate(zip(bars, values)):
            if value >= 9:
                ax.annotate(
                    f"{value:.1f}%", xy=(left[index] + value / 2, bar.get_y() + bar.get_height() / 2),
                    ha="center", va="center", fontsize=8.5, fontweight="bold",
                    color="white" if key == "verifier" else COLORS["dark"],
                )
        left = [current + value for current, value in zip(left, values)]

    ax.invert_yaxis()
    ax.set_title(
        f"{any_feedback_pct:.0f}% report feedback; {verifier_pct:.0f}% include verifier-like checks",
        pad=14,
    )
    ax.set_xlabel("Share of papers", labelpad=10)
    ax.set_ylabel("")
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    clean_axes(ax, "x")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.31), ncol=3, frameon=False)
    save(fig, "feedback_coverage.png")
    return stats


def plot_research_resource_mix(
    papers: list[dict[str, Any]], resources: list[dict[str, Any]]
) -> tuple[Counter, Counter]:
    relevance_counts = Counter(paper["relevance"] for paper in papers)
    resource_counts = Counter(resource["type"] for resource in resources)
    rel_labels = [rel.title() for rel in RELEVANCE_ORDER]
    rel_values = [relevance_counts[rel] for rel in RELEVANCE_ORDER]
    resource_items = sorted(resource_counts.items(), key=lambda item: (-item[1], item[0]))
    resource_labels = [label.title() for label, _ in resource_items]
    resource_values = [value for _, value in resource_items]

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.4), dpi=DPI, constrained_layout=True)
    fig.suptitle(
        f"The catalog links {len(papers)} papers with {len(resources)} research resources",
        fontsize=15, fontweight="bold", y=1.02,
    )

    bars_left = axes[0].bar(
        rel_labels, rel_values,
        color=[RELEVANCE_COLORS[rel] for rel in RELEVANCE_ORDER], width=0.62,
    )
    add_bar_labels(axes[0], bars_left)
    axes[0].set_title("Paper relevance", fontsize=12, pad=12)
    axes[0].set_ylabel("Papers", labelpad=10)
    axes[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    axes[0].set_ylim(0, max(rel_values) * 1.18)
    clean_axes(axes[0], "y")

    bars_right = axes[1].barh(
        resource_labels[::-1], resource_values[::-1],
        color=RESOURCE_COLORS[:len(resource_labels)][::-1], height=0.64,
    )
    add_bar_labels(axes[1], bars_right, horizontal=True)
    axes[1].set_title("Resource types", fontsize=12, pad=12)
    axes[1].set_xlabel("Resources", labelpad=10)
    axes[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    axes[1].set_xlim(0, max(resource_values) * 1.20)
    clean_axes(axes[1], "x")

    save(fig, "research_resource_mix.png")
    return relevance_counts, resource_counts


def pct(numerator: int, denominator: int) -> str:
    return f"{100 * numerator / denominator:.1f}%"


def write_analysis(
    papers: list[dict[str, Any]],
    resources: list[dict[str, Any]],
    paper_payload: dict[str, Any],
    resource_payload: dict[str, Any],
    representation_counts: Counter,
    feedback: dict[str, dict[str, int]],
    relevance_counts: Counter,
    resource_counts: Counter,
) -> None:
    year_counts = Counter(int(paper["year"]) for paper in papers)
    year_range = (min(year_counts), max(year_counts))
    peak_year, peak_count = max(year_counts.items(), key=lambda item: (item[1], item[0]))
    overall = feedback["All papers"]
    any_feedback = overall["verifier"] + overall["broad_only"]
    representations_total = sum(representation_counts.values())
    top_representations = representation_counts.most_common(12)
    resource_order = sorted(resource_counts.items(), key=lambda item: (-item[1], item[0]))
    years_table = []
    for year in sorted(year_counts):
        by_rel = Counter(paper["relevance"] for paper in papers if int(paper["year"]) == year)
        years_table.append(
            f"| {year} | {year_counts[year]} | {by_rel['core']} | {by_rel['support']} | {by_rel['adjacent']} |"
        )

    text = f"""# Catalog analysis

This report is generated from [`data/papers.json`](data/papers.json) and [`data/resources.json`](data/resources.json) by [`scripts/generate_charts.py`](scripts/generate_charts.py). Counts describe catalog metadata, not the size or performance of the research field. Both inputs were last verified on **{paper_payload.get('last_verified')}**; resource metadata reports **{resource_payload.get('last_verified')}**.

## Headline statistics

- **{len(papers)} deduplicated papers/works** spanning **{year_range[0]}–{year_range[1]}**: {relevance_counts['core']} core, {relevance_counts['support']} support, and {relevance_counts['adjacent']} adjacent.
- **{peak_year} is the largest publication year** in the catalog, with {peak_count} papers ({pct(peak_count, len(papers))} of all records).
- **{len(resources)} resources** are indexed: {', '.join(f'{count} {kind}' for kind, count in resource_order)}.
- **{any_feedback}/{len(papers)} papers ({pct(any_feedback, len(papers))})** list at least one feedback mechanism; **{overall['verifier']}/{len(papers)} ({pct(overall['verifier'], len(papers))})** include verifier-like checks under the reproducible keyword rule below.
- The metadata contains **{len(representation_counts)} distinct representation labels** and **{representations_total} paper–representation incidences** because records may carry multiple labels. The most frequent label is **{top_representations[0][0]}** ({top_representations[0][1]} papers).

## Papers by year and relevance

| Year | All | Core | Support | Adjacent |
|---:|---:|---:|---:|---:|
{chr(10).join(years_table)}

![Papers by year and relevance](assets/papers_by_year.png)

## Representation landscape

The chart reports the 12 most frequent **exact strings** in each paper's `representation` array. Counts are multi-label incidences and should not be summed as unique papers.

| Representation | Papers |
|---|---:|
{chr(10).join(f'| {label} | {count} |' for label, count in top_representations)}

![Representation landscape](assets/representation_landscape.png)

## Feedback and verifier coverage

“Any feedback” means a non-empty `feedback` array. “Verifier-like checks” are detected case-insensitively from feedback strings using terms for compilation/execution/runtime, rendering, tests/schema/validation, symbolic or geometric constraints, metrics, simulation/state, objective checks, rewards, integrity, or physics. This is a transparent metadata heuristic, not a judgment of verifier quality. Categories in the chart are mutually exclusive: verifier-like, other reported feedback, or no feedback listed.

| Scope | Papers | Verifier-like | Other feedback | No feedback listed |
|---|---:|---:|---:|---:|
{chr(10).join(f"| {group} | {values['total']} | {values['verifier']} | {values['broad_only']} | {values['none']} |" for group, values in feedback.items())}

![Feedback and verifier coverage](assets/feedback_coverage.png)

## Research and resource mix

![Research and resource mix](assets/research_resource_mix.png)

## Data-quality notes

- IDs are present and unique in both input collections; the generator stops on missing or duplicate IDs.
- Empty arrays and `null` values are retained as unknown/not listed rather than imputed.
- Publication year is taken directly from each normalized record; no venue-year inference is performed.
- Representation labels remain source-normalized exact strings. Similar technologies (for example, `SVG`, `SVG code`, and `SVG/XML animation`) are not merged.
- Feedback coverage measures metadata presence. It does not establish whether a loop is effective, independent, or reproducible.
"""
    ANALYSIS_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    papers, paper_payload = load_records(DATA_DIR / "papers.json", "papers")
    resources, resource_payload = load_records(DATA_DIR / "resources.json", "resources")
    required_paper_fields = {"id", "year", "relevance", "representation", "feedback"}
    for paper in papers:
        missing = required_paper_fields - paper.keys()
        if missing:
            raise ValueError(f"{paper.get('id')}: missing required fields {sorted(missing)}")
        if paper["relevance"] not in RELEVANCE_ORDER:
            raise ValueError(f"{paper['id']}: unexpected relevance {paper['relevance']!r}")

    set_style()
    plot_papers_by_year(papers)
    representation_counts = plot_representation_landscape(papers)
    feedback = plot_feedback_coverage(papers)
    relevance_counts, resource_counts = plot_research_resource_mix(papers, resources)
    write_analysis(
        papers, resources, paper_payload, resource_payload, representation_counts,
        feedback, relevance_counts, resource_counts,
    )

    overall = feedback["All papers"]
    print(f"Generated 4 charts and analysis.md from {len(papers)} papers and {len(resources)} resources.")
    print("Relevance:", dict(relevance_counts))
    print("Years:", dict(sorted(Counter(p['year'] for p in papers).items())))
    print("Resource types:", dict(resource_counts))
    print("Top representations:", representation_counts.most_common(12))
    print("Feedback:", overall)


if __name__ == "__main__":
    main()
