# Research gaps

> Evidence synthesis for **awesome-code-generated-video**, frozen at **2026-10-27**. Priorities reflect missing evidence, not product commitments.

## Priority rubric

- **P0:** blocks valid comparison or safe reproduction now.
- **P1:** likely to unlock reliable long-form/editable systems after P0 infrastructure exists.
- **P2:** high-upside direction that needs stronger datasets or measurement first.

Each proposal below is falsifiable: it names a contrast, measurable outcomes, and a result that would reject the hypothesis.

## P0 — A reproducible execution and safety protocol

**Evidence.** Code2Video-Compass is the broadest direct benchmark but does not fully cover cross-environment rebuilds, security attacks, lifecycle cost, or multi-round repair. The evaluation brief finds that no benchmark jointly covers code, video, system, agent and safety layers. Blender/UE studies additionally report substantial engine-version and asset fragility.

**Gap.** “Execution success” is not standardized; parse success, partial preview and complete playable render are often mixed.

**Falsifiable experiment.** Run the same submissions three times in the same container, after a cold rebuild, and on a second node. Compare a pinned environment with an ordinary lockfile-only setup. Measure the full execution funnel, perceptual variance, cross-machine success, security-policy violations, and cost per successful rendered second.

**Reject the hypothesis if** pinning plus isolated execution does not improve cold-build/cross-node success or does not change the ranking confidence while adding material cost.

## P0 — Temporal correctness beyond executability and appearance

**Evidence.** Animation2Code reports near-perfect execution for some settings while temporal similarity remains far below appearance similarity. ManiBench shows that code-keyword alignment can saturate without proving rendered correctness. 4DCodeBench and PhySimCode find dynamics/parameter recovery much harder than static appearance or law recall.

**Gap.** Frame-average similarity and global VLM scores under-detect wrong order, phase, loop period, trajectory, contact and identity swaps.

**Falsifiable experiment.** Build paired adversarial tasks with identical first/last frames but different event order, phase, trajectories and occlusion. Compare frame-average embeddings, a video VLM, object tracking, and event/temporal predicates against blinded human labels.

**Reject the hypothesis if** frame-average or global VLM scoring matches the structured stack within confidence intervals on both detection and ranking.

## P0 — Calibrated critics and judges

**Evidence.** PhysicsSolutionAgent documents misleading VLM feedback. Reels-RSI observes 62–81% second-position preference in a pairwise judge. ManimAgent explicitly uses blind human Pass@1 to reduce same-model reward/judge circularity. SGA reports symbolic geometry outperforming a VLM critic on layout.

**Gap.** Most systems report final quality but not critic precision, localization accuracy, induced regressions, or position/style bias.

**Falsifiable experiment.** Create fault-injected videos/code with known labels across layout, timing, semantics and physics. Randomize pair order and style; test same-family and cross-family critics. Measure precision/recall, frame-interval and object localization, repair success and new-regression rate.

**Reject the hypothesis if** the same-family VLM critic is calibrated, order-invariant and no worse than deterministic/specialized checks at equal cost.

## P1 — Persistent scene identity and sparse temporal state

**Evidence.** VAnim reports major sequence compression with a persistent SVG DOM and sparse state updates. MG-Gen, LogoMotion and Reels-RSI benefit from layered objects and code-linked artifacts. Long-form Manim systems repeatedly report overlap, identity and layout accumulation.

**Gap.** There is no cross-runtime test of whether persistent IDs plus sparse updates improve long-duration generation over scene-local or frame-oriented code.

**Falsifiable experiment.** Implement equivalent tasks in (a) monolithic/frame-oriented code and (b) persistent scene graph + stable IDs + sparse updates. Stratify by duration and scene count. Measure token length, render success, identity errors, edit locality, repair regressions and quality at equal model/compute budgets.

**Reject the hypothesis if** the structured representation fails to improve long-duration identity/edit locality or loses enough expressive quality to erase its reliability gains.

## P1 — Localized repair versus full regeneration

**Evidence.** Code2Video uses scope-guided fixes; SGA targets geometric conflicts; BlenderAlchemy favors small reversible node edits; Code4Scene checks unintended scene changes. Self-repair research warns that gains can disappear against compute-matched best-of-N and may introduce regressions.

**Gap.** Repair is rarely evaluated for spatial, temporal and code-level spillover.

**Falsifiable experiment.** Inject one localized defect per task. Compare whole-project regeneration, file-level rewrite, dependency-sliced patch and object/time-scoped patch against compute-matched best-of-N. Measure target repair, preservation outside the target, diff locality, new failures and total cost.

**Reject the hypothesis if** scoped patches do not improve preservation-adjusted repair success or if whole regeneration dominates on the quality–cost frontier.

## P1 — Long-form narrative and audio–visual synchronization

**Evidence.** TheoremExplainAgent and Code2Video extend generation to multi-minute output, but layout errors accumulate. DATAREEL reports persistent coordination failures among animation, emphasis, subtitles and timeline. Existing broad benchmarks emphasize short visual tasks and under-cover audio.

**Gap.** No direct benchmark combines multi-scene entity/state continuity, narration-word timing, caption readability, sound-event alignment and causal narrative.

**Falsifiable experiment.** Construct duration buckets (15 s, 60 s, 3 min, 5 min) from the same underlying event graphs. Add word-level narration and sound-event anchors. Measure execution, cross-scene state consistency, event completion, ASR/OCR accuracy, synchronization error and human comprehension.

**Reject the hypothesis if** performance does not degrade with length/state depth, or if short-task metrics predict long-form comprehension without adding state/audio measures.

## P1 — Outcome validity for educational video

**Evidence.** Code2Video introduces TeachQuiz; LLM2Manim reports a controlled student study; most other educational systems use VLM rubrics, visual similarity or expert preference. ALGOGEN notes that execution success is not learning effectiveness.

**Gap.** It is unknown whether automatic teaching scores transfer across learners, topics and video styles.

**Falsifiable experiment.** On a preregistered topic-stratified set, compare TeachQuiz/VLM scores, expert factual review and randomized learner pre/post tests with delayed retention. Test rank correlations and calibration across domains.

**Reject the hypothesis if** automatic scores robustly predict immediate and delayed human learning across held-out domains after controlling for prior knowledge.

## P1 — Valid-by-construction temporal and physical programs

**Evidence.** ALGOGEN separates verified traces from rendering. MoVer uses explicit temporal predicates. Living Worlds moves state constraints into transactional tools and strongly improves executability over a staged baseline. SimuScene still shows low dynamically correct success despite executable code.

**Gap.** General animation lacks a shared temporal contract with pre/postconditions, state invariants and renderer-independent tests.

**Falsifiable experiment.** Compare unconstrained direct code with a typed temporal IR compiled to at least two runtimes. Use identical prompts and budgets; measure invalid-state rate, event/physics correctness, renderer parity, repair count and expressiveness loss.

**Reject the hypothesis if** the typed IR does not reduce invalid dynamics, or if compiler/runtime restrictions materially lower human-rated task fulfillment.

## P2 — 3D multi-view and hidden-state verification

**Evidence.** SceneCraft and LL3M note that selected renders hide 3D errors. 3DCodeBench combines 2D/3D/execution metrics; Code4Scene checks persistent engine state. Current video-centric evaluation often sees only final camera views.

**Gap.** There is no standard method to combine final-shot quality with canonical views, geometry, contact and hidden engine state.

**Falsifiable experiment.** Seed back-face, hidden-intersection, collision and joint-range defects that are invisible in the hero camera. Compare hero-view VLM, fixed multi-view rendering, structural state checks and their combination.

**Reject the hypothesis if** hero-view evaluation detects hidden faults as reliably as structural/multi-view verification at lower cost.

## P2 — Hybrid video priors distilled back into editable programs

**Evidence.** LiveSVG and LiveSketch use video priors to propose motion while preserving vector outputs. GPT4Motion and VideoCoCo use executable simulation as a control draft but may reintroduce geometry/identity errors in the pixel stage.

**Gap.** The trade-off among realism, physical correctness, editability and program recovery is not quantified.

**Falsifiable experiment.** Compare pure code rendering, code→pixel refinement, and video-prior→program distillation on matched prompts. Apply post-generation edits and re-render. Measure realism, constraint pass, identity, edit success, determinism and cost.

**Reject the hypothesis if** distillation offers no editability/constraint advantage over pixel refinement or no realism advantage over pure code.

## P2 — Data leakage, licenses and provenance as benchmark variables

**Evidence.** Public CodePen, Manim and web code may be present in pretraining. The evaluation brief identifies URL/code deduplication, temporal splits, private holdouts and asset manifests as unresolved. Several resources have unconfirmed licenses or external assets.

**Gap.** Reported gains may mix capability, memorization and unavailable dependencies.

**Falsifiable experiment.** Use URL/hash/AST similarity deduplication, a post-cutoff holdout and privately authored variants; provide an offline asset manifest. Compare performance and confidence intervals to the original public split.

**Reject the hypothesis if** rankings and absolute performance remain stable after strict deduplication and private holdout evaluation.

## Suggested execution order

1. **P0 protocol:** frozen runtimes, safety gate, execution funnel, trace schema.
2. **P0 measurement:** temporal adversarial set and calibrated critic study.
3. **P1 representation/repair:** persistent state, typed contracts, local patches.
4. **P1 application validity:** long-form audio and educational outcomes.
5. **P2 expansion:** 3D hidden state, hybrid priors, leakage/provenance.

The machine-readable evidence is in [`data/papers.json`](data/papers.json) and [`data/resources.json`](data/resources.json); definitions are fixed in [`taxonomy.md`](taxonomy.md).
