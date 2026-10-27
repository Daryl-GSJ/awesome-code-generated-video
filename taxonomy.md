# Taxonomy

> Operational taxonomy for **awesome-code-generated-video**. Evidence cutoff: **2026-10-27**.

## 1. Working definition

**Code-generated video** is a time-based visual artifact for which a model or agent produces an **executable visual program**—source code, a declarative animation program, a simulator/world program, or a structured temporal representation—and an identified runtime executes or renders that output into animation or video.

All four conditions are required for the direct core:

1. **Machine-generated program:** a model or agent creates or materially edits the executable visual representation.
2. **Time-bearing representation:** the output specifies animation, timeline, state changes, simulation, camera motion, or another temporal process.
3. **Identified execution path:** a renderer, browser, DCC, game engine, simulator, or compiler turns the representation into a frame sequence.
4. **Video/animation is a primary output or evaluation target:** a static scene that could be filmed is not enough.

“Code” is used broadly but operationally: Manim/Blender Python, HTML/CSS/JavaScript, D3.js, SVG animation, Lottie JSON, Remotion projects, engine scripts, simulation programs, verified traces, event graphs, and typed animation DSLs qualify when executable. A prose script or storyboard does not.

## 2. Relevance tiers

| Tier | Operational test | Typical examples |
|---|---|---|
| `core` | Generated executable temporal program directly renders the final animation/video. | Manim, browser animation, Lottie, deterministic game-engine cutscene |
| `support` | The code-render chain is central, but the primary contribution is evaluation, verification, inverse reconstruction, or a hybrid final stage. | MoVer, SGA, Animation2Code, 4DCodeBench, VideoCoCo |
| `adjacent` | Generates executable visual/scene programs with a concrete transfer path to temporal rendering, but video is secondary or absent. | static SVG/TikZ, Blender scene code, game/robot worlds |
| `background` | Supplies a reusable renderer, simulator, metric, sandbox, or program-synthesis mechanism without directly solving model-generated video code. | Kubric, BlenderProc, general execution harnesses |

Tier describes **task relevance**, not quality or prestige.

## 3. Inclusion rules

Include a paper when evidence verifies all fields needed to establish its tier and at least one of the following:

- text/image/paper/table/video → executable animation/video program;
- program generation with deterministic render-back as the main evaluation;
- a benchmark or verifier designed specifically for code-rendered video/animation;
- an adjacent executable visual-program contribution with an explicit mechanism transferable to time (persistent identity, sparse updates, compilation, structural editing, engine state, render-in-the-loop feedback);
- a maintained system/tool/dataset that materially enables the above and has a stable public URL.

For repositories and project pages, list the paper once in `data/papers.json`; list independently useful artifacts in `data/resources.json`. Preprint and published versions are one record.

## 4. Exclusion rules

Exclude from the paper core:

- ordinary pixel/latent text-to-video or image-to-video systems that do not output an executable visual program;
- “code-conditioned video” where code is only an input;
- systems that generate only prose scripts, narration, shot lists, slides, or asset playlists;
- static mesh, NeRF, 3DGS, CAD, webpage, SVG, or Blender-scene generation without a verified temporal output (these may be `adjacent`, never `core` solely because they are renderable);
- hand-authored Manim/Blender educational case studies without model-generated code;
- generic coding models, generic UI-to-code systems, or metrics with no specific, documented transfer role;
- demos with unstable or unverifiable identity, claims, or URLs.

Hybrid systems are not excluded, but must be labeled `support` when generated pixels modify the code-rendered draft before the final video.

## 5. Deduplication and evidence policy

1. Canonical key: arXiv ID without version; otherwise ACL/DOI/stable publication identifier.
2. Merge title variants, versions, preprint and proceedings records.
3. Keep a system, its dataset, and its benchmark in one paper record; expose reusable artifacts separately as resources.
4. Do not conflate **ManimBench** (Silva et al. training/evaluation data) with **ManiBench** (Oli's 12-task pilot).
5. Prefer the published venue only when verified; otherwise use `venue: null` and a conservative `status`.
6. Conflicting counts use the full-text, smaller, or otherwise more conservative figure. Planned scale is not recorded as completed scale.
7. Unknown facts are `null` or `[]`; an inferred project URL, DOI, venue, license, or author list is prohibited.
8. `source_brief` records which local evidence brief supports each normalized record; it is not a citation substitute.

## 6. Orthogonal research facets

### Input

`text` · `paper` · `theorem` · `problem` · `table` · `image` · `keyframe` · `video` · `existing-project` · `edit-instruction`

### Task

- `T2V-code`: text to a complete executable video project;
- `I2V-code`: image/design/keyframe to executable animation code;
- `V2V-code`: reference video to executable reconstruction;
- `Edit-code`: localized modification of an existing executable project;
- `Long-form`: multi-scene explanatory or narrative video;
- `Simulation`: code whose dynamics produce the video;
- `Verification`: diagnose or enforce properties of generated animation.

### Representation

- scene programs: Manim Python, Blender Python, engine scripts;
- web programs: HTML/CSS/JS, D3.js, Canvas, Three.js, Remotion;
- vector programs: SVG/SMIL/CSS, Lottie JSON;
- constrained IR: storyboards, scene graphs, sparse state updates, traces, event graphs, typed DSLs;
- simulation programs: physical parameters, ODE/numerical code, articulated world programs.

### Generation strategy

`direct` · `planner-coder` · `multi-agent` · `trained-model` · `SFT/RL` · `tool-generation` · `inverse-graphics` · `human-in-the-loop` · `hybrid-code-pixel`

### Feedback and verification

`parser/compiler` · `runtime-log` · `render-in-the-loop` · `VLM-critic` · `symbolic-geometry` · `temporal-DSL` · `schema` · `unit-test` · `simulation-oracle` · `human-gate` · `persistent-memory`

### Output domain

`education` · `data-storytelling` · `motion-graphics` · `vector-animation` · `physics` · `algorithm-visualization` · `3D/cutscene` · `inverse-reconstruction` · `general-purpose`

## 7. Evaluation layers

A result should never collapse these layers into an unqualified total score:

1. **Safety gate:** policy violations, secret/network/file/process access.
2. **Operational funnel:** parse → dependencies → compile → runtime start → complete render → valid artifact → usable video.
3. **Spatial:** bounds, overlap, occlusion, text readability, object identity.
4. **Temporal/dynamic:** event order, duration, trajectory, phase, motion completion, physics.
5. **Semantic:** atomic prompt constraints and cross-scene state.
6. **Editability:** stable IDs, local patches, unaffected-region preservation, reusable structure.
7. **Outcome:** learning, recall, communication, brand/task success.
8. **Efficiency/reproducibility:** full cost, repeated runs, cold rebuilds, environment drift.

Report hard gates and separate axes; if ranking is unavoidable, gate the geometric mean of applicable quality axes by safety, artifact validity, and render completion.

## 8. Borderline examples

- **SceneCraft:** adjacent—primarily static Blender scene code; downstream video control does not make video its primary output.
- **Animation2Code:** support—video is the input, but generated code is executed and evaluated through render-back.
- **VideoCoCo/GPT4Motion:** support or adjacent hybrid—the executable simulation is a control layer, while the final pixels are generative.
- **LiveSVG/LiveSketch:** adjacent—the final representation is editable and temporal, but optimization/distillation rather than discrete code synthesis is central.
- **InternSVG:** only dynamic SVG/SANI tasks are direct; static subtasks are adjacent.
