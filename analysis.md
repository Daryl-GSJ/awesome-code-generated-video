# Catalog analysis

This report is generated from [`data/papers.json`](data/papers.json) and [`data/resources.json`](data/resources.json) by [`scripts/generate_charts.py`](scripts/generate_charts.py). Counts describe catalog metadata, not the size or performance of the research field. Both inputs were last verified on **2026-10-27**; resource metadata reports **2026-10-27**.

## Headline statistics

- **68 deduplicated papers/works** spanning **2020–2026**: 23 core, 11 support, and 34 adjacent.
- **2026 is the largest publication year** in the catalog, with 40 papers (58.8% of all records).
- **63 resources** are indexed: 26 benchmark, 16 tool, 11 dataset, 6 showcase, 4 system.
- **62/68 papers (91.2%)** list at least one feedback mechanism; **51/68 (75.0%)** include verifier-like checks under the reproducible keyword rule below.
- The metadata contains **115 distinct representation labels** and **154 paper–representation incidences** because records may carry multiple labels. The most frequent label is **Manim Python** (12 papers).

## Papers by year and relevance

| Year | All | Core | Support | Adjacent |
|---:|---:|---:|---:|---:|
| 2020 | 1 | 0 | 0 | 1 |
| 2023 | 3 | 0 | 0 | 3 |
| 2024 | 15 | 3 | 0 | 12 |
| 2025 | 9 | 4 | 1 | 4 |
| 2026 | 40 | 16 | 10 | 14 |

![Papers by year and relevance](assets/papers_by_year.png)

## Representation landscape

The chart reports the 12 most frequent **exact strings** in each paper's `representation` array. Counts are multi-label incidences and should not be summed as unique papers.

| Representation | Papers |
|---|---:|
| Manim Python | 12 |
| SVG | 6 |
| Blender Python | 5 |
| Three.js | 5 |
| SVG code | 5 |
| HTML | 4 |
| narration | 3 |
| JavaScript animation | 2 |
| storyboard | 2 |
| Lottie JSON | 2 |
| Canvas | 2 |
| Remotion | 2 |

![Representation landscape](assets/representation_landscape.png)

## Feedback and verifier coverage

“Any feedback” means a non-empty `feedback` array. “Verifier-like checks” are detected case-insensitively from feedback strings using terms for compilation/execution/runtime, rendering, tests/schema/validation, symbolic or geometric constraints, metrics, simulation/state, objective checks, rewards, integrity, or physics. This is a transparent metadata heuristic, not a judgment of verifier quality. Categories in the chart are mutually exclusive: verifier-like, other reported feedback, or no feedback listed.

| Scope | Papers | Verifier-like | Other feedback | No feedback listed |
|---|---:|---:|---:|---:|
| All papers | 68 | 51 | 11 | 6 |
| Core | 23 | 15 | 6 | 2 |
| Support | 11 | 11 | 0 | 0 |
| Adjacent | 34 | 25 | 5 | 4 |

![Feedback and verifier coverage](assets/feedback_coverage.png)

## Research and resource mix

![Research and resource mix](assets/research_resource_mix.png)

## Data-quality notes

- IDs are present and unique in both input collections; the generator stops on missing or duplicate IDs.
- Empty arrays and `null` values are retained as unknown/not listed rather than imputed.
- Publication year is taken directly from each normalized record; no venue-year inference is performed.
- Representation labels remain source-normalized exact strings. Similar technologies (for example, `SVG`, `SVG code`, and `SVG/XML animation`) are not merged.
- Feedback coverage measures metadata presence. It does not establish whether a loop is effective, independent, or reproducible.
