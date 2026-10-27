# Contributing to awesome-code-generated-video

Thanks for improving this research-first index. Please optimize for **verifiability, precise scope, and maintainability**, not list length.

## Before opening a contribution

1. Read [`taxonomy.md`](taxonomy.md), especially the operational definition and tier rules.
2. Search `data/papers.json` by arXiv ID, DOI/ACL identifier, normalized title and project URL.
3. Read the primary paper in full when available. Use official proceedings, project and repository pages only to supplement venue, code, data and artifact status.
4. Verify every URL and fact as of the date in `last_verified`.

## What belongs here

A direct-core submission must produce or materially edit a time-bearing executable visual program and render/execute it into animation or video. Benchmarks, verifiers, inverse-graphics work and hybrid systems may enter `support`. Static visual/3D programs require a concrete temporal-transfer mechanism and normally enter `adjacent`.

Do not submit ordinary pixel-space video generation, prose-only scripts/storyboards, code-conditioned video, static scene/asset generation presented as direct video work, or generic code tools without a documented role.

## Data changes

### Papers

Edit `data/papers.json` and preserve every required field:

`id`, `title`, `year`, `authors`, `venue`, `status`, `paper_url`, `code_url`, `project_url`, `relevance`, `representation`, `generation`, `feedback`, `task`, `dataset`, `evaluation`, `findings`, `limitations`, `source_brief`, `last_verified`.

Rules:

- use an arXiv ID without version as the ID when possible;
- merge preprint and published records;
- use the formal published venue only when verified;
- write all known authors in publication order; if unavailable, use `[]`, never invent or expand “et al.”;
- use `null` for unknown scalar values and `[]` for unknown/empty lists;
- state findings and limitations conservatively, without promotional adjectives;
- `source_brief` must point to one or more repository evidence briefs;
- do not convert author-reported results into independent facts.

### Resources

Use `data/resources.json` for reusable `dataset`, `benchmark`, `system`, `tool`, or `showcase` artifacts. A paper and its repository are not two papers. Keep licenses `null` unless a license is verified at the resource itself.

### Validation

Validate both files against:

- `schema/papers.schema.json`
- `schema/resources.schema.json`

Also check:

- unique IDs;
- valid JSON and HTTPS URLs;
- no arXiv version suffix in canonical IDs;
- no duplicate preprint/proceedings records;
- dates in `YYYY-MM-DD`;
- English and Chinese README summaries remain consistent.

## Evidence note for additions

In the pull request, include:

- primary paper/publication URL;
- code/project/data URLs, if verified;
- proposed relevance tier and one-sentence boundary rationale;
- conflicts encountered and the conservative resolution;
- exact verification date;
- whether numbers are author-reported, independently reproduced, or merely planned.

## Writing and list design

- Keep README core entries to one scannable line.
- Put detailed metadata in JSON and evidence discussion in `research/*.md`.
- Do not rank papers by a single metric.
- Distinguish render success, visual quality, temporal correctness, task outcomes and cost.
- Do not add generated charts to a metadata-only change; chart work has its own review path.

## Pull request checklist

- [ ] I read the scope and exclusion rules.
- [ ] I searched for duplicates by identifier, title and URL.
- [ ] All claims are supported by primary or official sources.
- [ ] Unknown values are `null`/`[]`.
- [ ] Venue, scale, code availability and license are not inferred.
- [ ] Both JSON files validate against their schemas.
- [ ] README files remain concise and synchronized where affected.
- [ ] `last_verified` reflects my actual verification date.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
