# Catalog analysis

This report is generated from [`data/papers.json`](data/papers.json) and [`data/resources.json`](data/resources.json) by [`scripts/generate_charts.py`](scripts/generate_charts.py). Counts describe catalog metadata, not the size or performance of the research field. Both inputs were last verified on **2026-10-27**; resource metadata reports **2026-10-27**.

## Headline statistics

- **62 deduplicated papers/works** spanning **2020–2026**: 21 core, 8 support, and 33 adjacent.
- **2026 is the largest publication year** in the catalog, with 35 papers (56.5% of all records).
- **49 resources** are indexed: 21 benchmark, 10 dataset, 10 tool, 5 system, 3 showcase.
- **56/62 papers (90.3%)** list at least one feedback mechanism; **45/62 (72.6%)** include verifier-like checks under the reproducible keyword rule below.
- The metadata contains **106 distinct representation labels** and **134 paper–representation incidences** because records may carry multiple labels. The most frequent label is **Manim Python** (9 papers).

## Papers by year and relevance

| Year | All | Core | Support | Adjacent |
|---:|---:|---:|---:|---:|
| 2020 | 1 | 0 | 0 | 1 |
| 2023 | 3 | 0 | 0 | 3 |
| 2024 | 15 | 3 | 0 | 12 |
| 2025 | 8 | 4 | 1 | 3 |
| 2026 | 35 | 14 | 7 | 14 |

![Papers by year and relevance](assets/papers_by_year.png)

## Representation landscape

The chart reports the 12 most frequent **exact strings** in each paper's `representation` array. Counts are multi-label incidences and should not be summed as unique papers.

| Representation | Papers |
|---|---:|
| Manim Python | 9 |
| Blender Python | 5 |
| SVG | 5 |
| SVG code | 5 |
| HTML | 3 |
| JavaScript animation | 2 |
| narration | 2 |
| storyboard | 2 |
| Canvas | 2 |
| Three.js | 2 |
| joints | 2 |
| Vega-Lite | 1 |

![Representation landscape](assets/representation_landscape.png)

## Feedback and verifier coverage

“Any feedback” means a non-empty `feedback` array. “Verifier-like checks” are detected case-insensitively from feedback strings using terms for compilation/execution/runtime, rendering, tests/schema/validation, symbolic or geometric constraints, metrics, simulation/state, objective checks, rewards, integrity, or physics. This is a transparent metadata heuristic, not a judgment of verifier quality. Categories in the chart are mutually exclusive: verifier-like, other reported feedback, or no feedback listed.

| Scope | Papers | Verifier-like | Other feedback | No feedback listed |
|---|---:|---:|---:|---:|
| All papers | 62 | 45 | 11 | 6 |
| Core | 21 | 13 | 6 | 2 |
| Support | 8 | 8 | 0 | 0 |
| Adjacent | 33 | 24 | 5 | 4 |

![Feedback and verifier coverage](assets/feedback_coverage.png)

## Research and resource mix

![Research and resource mix](assets/research_resource_mix.png)

## Data-quality notes

- IDs are present and unique in both input collections; the generator stops on missing or duplicate IDs.
- Empty arrays and `null` values are retained as unknown/not listed rather than imputed.
- Publication year is taken directly from each normalized record; no venue-year inference is performed.
- Representation labels remain source-normalized exact strings. Similar technologies (for example, `SVG`, `SVG code`, and `SVG/XML animation`) are not merged.
- Feedback coverage measures metadata presence. It does not establish whether a loop is effective, independent, or reproducible.
