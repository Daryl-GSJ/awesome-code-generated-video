# Awesome Code-Generated Video

[![数据校验](https://github.com/Daryl-GSJ/awesome-code-generated-video/actions/workflows/validate.yml/badge.svg)](https://github.com/Daryl-GSJ/awesome-code-generated-video/actions/workflows/validate.yml) [![链接检查](https://github.com/Daryl-GSJ/awesome-code-generated-video/actions/workflows/links.yml/badge.svg)](https://github.com/Daryl-GSJ/awesome-code-generated-video/actions/workflows/links.yml) ![许可](https://img.shields.io/badge/license-CC0--1.0-lightgrey) ![截止日](https://img.shields.io/badge/evidence%20cutoff-2026--10--27-f08c00)

这是一个 **research-first** 的研究地图：模型生成 Manim、Blender Python、HTML/CSS/JS、SVG/Lottie、Remotion、仿真或引擎程序，再由明确运行时执行并渲染为动画或视频。

[English](README.md) · [仓库](https://github.com/Daryl-GSJ/awesome-code-generated-video) · [分类法](taxonomy.md) · [研究空白](research-gaps.md) · [论文数据](data/papers.json) · [资源数据](data/resources.json)

> **证据截止：2026-10-27。** 仓库统一四份完整 research brief，合并预印本与正式版本；未知信息保留为 `null`/`[]`，冲突信息采用更保守口径。

## 目录快照

标准化数据目前包含 **62 篇论文/工作**，其中 **21 篇核心**、**8 篇支撑**、**33 篇邻近工作**，另收录 **49 项资源**。论文记录集中于 2026 年（**35 篇**）。**56/62（90.3%）** 的论文列出了反馈机制；按 [`analysis.md`](analysis.md) 中可复现的启发式定义，**45/62（72.6%）** 包含与执行、渲染、结构、符号、指标、规则、测试或状态证据相关的 verifier-like 检查。

<p align="center">
  <img src="assets/papers_by_year.png" alt="按发表年份与相关性分层的论文堆叠柱状图" width="90%">
</p>
<p align="center"><em>按相关性分层的年度目录覆盖。</em></p>

<p align="center">
  <img src="assets/representation_landscape.png" alt="最常见精确表示标签的横向柱状图" width="90%">
</p>
<p align="center"><em>出现频率最高的精确表示标签；一篇论文可包含多个标签。</em></p>

<p align="center">
  <img src="assets/feedback_coverage.png" alt="按相关性分层的反馈与验证器覆盖率" width="90%">
</p>
<p align="center"><em>元数据中报告的反馈机制与 verifier-like 检查覆盖率。</em></p>

<p align="center">
  <img src="assets/research_resource_mix.png" alt="论文相关性与资源类型计数" width="90%">
</p>
<p align="center"><em>论文相关性构成与收录研究资源的类型分布。</em></p>

## 定义

当模型或智能体生成/实质修改一个**带时间语义的可执行视觉表示**，该表示由明确运行时执行，且动画/视频是主要输出或评价目标时，本仓库将工作列为**直接核心**。

可执行表示包括动画源码、声明式时间格式、可验证轨迹以及世界/事件程序。不包括普通像素空间视频生成、仅把代码作为输入条件的模型、只生成文字脚本/分镜的系统，以及“可以被拍成视频”但不含时间程序的静态场景。Benchmark、verifier、逆向重建和 code→pixel 混合系统列为**核心支撑**；具备明确时间迁移机制的静态视觉/3D 程序研究列为**邻近工作**。

完整操作性测试与边界案例见 [`taxonomy.md`](taxonomy.md)。

## 范围速览

| 维度 | 纳入范围 |
|---|---|
| 输入 | 文本、论文、定理/题目、表格、图像/关键帧、参考视频、已有工程 + 编辑指令 |
| 程序 | Manim/Blender Python、HTML/CSS/JS、D3.js、SVG/CSS/SMIL、Lottie JSON、Remotion、引擎/仿真代码、类型化 IR/DSL |
| 任务 | T2V-code、I2V-code、V2V-code、Edit-code、长篇讲解、数据叙事、motion graphics、物理/3D/cutscene |
| 反馈 | 编译/运行日志、renderer-in-the-loop、VLM critic、符号几何、时序谓词、schema/test、人工门控 |
| 评价 | 安全、完整渲染、空间/时间/语义、编辑局部性、任务效果、复现性与全生命周期成本 |

## 核心论文

每条刻意压缩为一行；**Data** 指向统一元数据，**Brief** 指向证据、数字与限制。

### 教育与解释视频

- **TheoremExplainAgent**（2025）— planner → Manim 的多分钟 STEM 解释；[Paper](https://arxiv.org/abs/2502.19400) · [Project](https://tiger-ai-lab.github.io/TheoremExplainAgent/) · [Data](data/papers.json) · [Brief](research/core.md)
- **Manimator**（2025）— 论文/PDF → 场景计划 → Manim，无视频反馈闭环；[Paper](https://arxiv.org/abs/2507.14306) · [Code](https://github.com/HyperCluster-Tech/manimator) · [Data](data/papers.json) · [Brief](research/core.md)
- **Code2Video**（ICML 2026）— planner–coder–critic、局部修复与 TeachQuiz；[Paper](https://arxiv.org/abs/2510.01174) · [Code](https://github.com/showlab/Code2Video) · [Data](data/papers.json) · [Brief](research/core.md)
- **LLM2Manim**（2026）— 教学法规划、符号台账与专家门控；[Paper](https://arxiv.org/abs/2604.05266) · [Data](data/papers.json) · [Brief](research/core.md)
- **PhysicsSolutionAgent**（2026）— 运行日志 + 截图 VLM 反馈的物理讲解；[Paper](https://arxiv.org/abs/2601.13453) · [Code](https://github.com/f20220374/PhysicsSolutionAgent) · [Data](data/papers.json) · [Brief](research/core.md)
- **LASEV**（KDD 2026）— 受约束可执行脚本与模板编译的部署级流水线；[Paper](https://arxiv.org/abs/2602.11790) · [Project](https://robitsg.github.io/LASEV/) · [Data](data/papers.json) · [Brief](research/core.md)
- **ManimTrainer / ManimAgent**（2026）— SFT/GRPO + 渲染器/文档在环推理；[Paper](https://arxiv.org/abs/2604.18364) · [Code](https://github.com/SuienS/manim-trainer) · [Data](data/papers.json) · [Brief](research/core.md)
- **ANVIL**（2026）— 类比 → screenplay → Manim，配合静态修复和教师审核；[Paper](https://arxiv.org/abs/2605.16295) · [Code](https://github.com/yurinoviello/AI_Metaphors) · [Data](data/papers.json) · [Brief](research/core.md)
- **ALGOGEN**（Findings of ACL 2026）— 可验证算法轨迹，确定性编译到多后端；[Paper](https://arxiv.org/abs/2605.12159) · [Project](https://algenlab.github.io/algogen/) · [Data](data/papers.json) · [Brief](research/core.md)
- **ManimAgent: Self-Evolving Multimodal Agents**（EMNLP 2026）— 成功/失败情景记忆与盲人评 Pass@1；[Paper](https://arxiv.org/abs/2606.30296) · [Code](https://github.com/jwj1342/Paper2Manim) · [Data](data/papers.json) · [Brief](research/core.md)

### Web、向量与 motion graphics

- **LogoMotion**（CHI 2025）— 视觉 grounding 的 JavaScript 合成、修复与代码连接控件；[Paper](https://arxiv.org/abs/2405.07065) · [Data](data/papers.json) · [Brief](research/vector_web.md)
- **MG-Gen**（2025）— 栅格设计 → 分层 HTML → JavaScript motion graphics；[Paper](https://arxiv.org/abs/2504.02361) · [Code](https://github.com/CyberAgentAILab/MG-GEN) · [Data](data/papers.json) · [Brief](research/vector_web.md)
- **DATAREEL**（2026）— 表格 → 计划 → HTML/D3.js，含计划和视频 critic；[Paper](https://arxiv.org/abs/2604.25220) · [Code](https://github.com/vis-nlp/DataReel) · [Data](data/papers.json) · [Brief](research/core.md)
- **LottieGPT**（CVPR 2026）— 自回归生成可编辑 Lottie 动画程序；[Paper](https://arxiv.org/abs/2604.11792) · [Code](https://github.com/yisuanwang/LottieGPT) · [Data](data/papers.json) · [Brief](research/core.md)
- **InternSVG**（ICLR 2026）— 统一 SVG 任务，含文本/视频到动态 SVG；[Paper](https://arxiv.org/abs/2510.11341) · [Project](https://hmwang2002.github.io/release/internsvg/) · [Data](data/papers.json) · [Brief](research/core.md)
- **VAnim**（ICML 2026）— 持久 SVG DOM + 稀疏状态更新 + 渲染感知训练；[Paper](https://arxiv.org/abs/2605.01517) · [Data](data/papers.json) · [Brief](research/vector_web.md)
- **Keyframer**（CHI 2024）— SVG + 自然语言 → 可编辑 CSS 动画；[Paper](https://arxiv.org/abs/2402.06071) · [Data](data/papers.json) · [Brief](research/vector_web.md)
- **Reels-RSI**（2026）— HTML/SVG/Canvas/Three.js reels、可执行规则与程序级记忆；[Paper](https://arxiv.org/abs/2610.14495) · [Code](https://github.com/agentic-loops-x/Reels-RSI) · [Data](data/papers.json) · [Brief](research/vector_web.md)

### 通用、3D 与结构化视频

- **Kubrick**（2024/2025 workshop 记录）— 多智能体生成 Blender 程序并由 VLM 复核；[Paper](https://arxiv.org/abs/2408.10453) · [Data](data/papers.json) · [Brief](research/core.md)
- **Data Director**（2024）— 表格洞察 → Vega-Lite/SVG/时间轴/音频数据视频；[Paper](https://arxiv.org/abs/2408.03876) · [Data](data/papers.json) · [Brief](research/core.md)
- **SimuScene**（2026）— 文本 → 可执行物理启发动画的训练与 benchmark；[Paper](https://arxiv.org/abs/2602.10840) · [Data](data/papers.json) · [Brief](research/core.md)

## 数据集与 Benchmark

| 资源 | 评测对象 | 关键边界 |
|---|---|---|
| [Code2Video-Compass](https://github.com/code2video-compass/Code2Video-Compass) | 2,104 个 Remotion Web 栈 T2V/I2V/V2V 任务 | 最广直接 benchmark；修复、安全、跨环境覆盖仍不足 |
| [Animation2Code](https://anya-ji.github.io/animation2code-website/) | 视频 → HTML/CSS/JS，分离外观与时间相似度 | 短 Web 动画逆向任务 |
| [MMMC / Code2Video](https://github.com/showlab/Code2Video) | 13 学科专业 Manim 教程与教学评价 | 教育/Manim 特定 |
| [TheoremExplainBench](https://tiger-ai-lab.github.io/TheoremExplainAgent/) | 4 个 STEM 学科、240 个定理 | 长篇解释，不代表通用 motion design |
| [MoVer](https://github.com/jama1017/MoVer) | 5,600 个提示及时间/空间验证程序 | 预定义 2D 谓词词表 |
| [ManiBench](https://github.com/nabin2004/ManiBench) | Manim CE 幻觉与 visual-logic drift | 当前论文仅为 12 题 pilot |
| [4DCodeBench](https://github.com/4DCodeBench/4DCodeBench) | 视频 → 可执行动态 3D 场景程序 | 逆图形且执行成本高 |
| [PhySimCode](https://github.com/SourajaKundu/PhySimCode) | 视频 → 物理规律、参数与仿真代码 | 程序化域差距与多解问题 |
| [3DCodeBench](https://github.com/gaoypeng/3dcodebench) | Blender 代码的执行、2D 与 3D 评价 | 偏资产生成，属于视频邻近方向 |
| [Code4Scene](https://simworld-ai-code4scene.static.hf.space/index.html) | Unreal 持久场景构建/编辑与完整性 | UE 特定，属于视频邻近方向 |

LottieBench、SAgoge/SArena、SVGAnim-134k、DATAREEL、SimuScene，以及可迁移的视频/编辑 benchmark 均见 [`data/resources.json`](data/resources.json)。


## 系统与工具

- **运行时：** [Manim](https://www.manim.community/)、[Remotion](https://www.remotion.dev/)、[Blender](https://www.blender.org/)、浏览器 HTML/SVG/Canvas/Three.js、Unity、Unreal Engine。
- **程序化/真值基础设施：** [Infinigen](https://github.com/princeton-vl/infinigen)、[Kubric](https://github.com/google-research/kubric)、[BlenderProc](https://github.com/DLR-RM/BlenderProc)、[AI2-THOR](https://github.com/allenai/ai2thor)。
- **Agent 工程：** [BlendHarness](https://github.com/cccky0813/BlendHarness)、[blender-agent-studio](https://github.com/ifBars/blender-agent-studio)、[blenderwright](https://github.com/HoldMyBeer-gg/blenderwright)、[better-blender-mcp](https://github.com/marlonka/better-blender-mcp)。
- **评价基础设施：** [VBench](https://github.com/Vchitect/VBench)、[VMAF](https://github.com/Netflix/vmaf)、[InterCode](https://github.com/princeton-nlp/intercode)、[HumanEval](https://github.com/openai/human-eval)。这些是可迁移组件，不直接证明 code-video 质量。

## 研究观察

1. **能运行不等于动得对。** Animation2Code 的可执行性/外观与时间重建明显脱钩；物理与 4D benchmark 也显示同样的静态—动态鸿沟。
2. **表示本身是算法选择。** 持久对象、稀疏状态更新、可验证轨迹和受约束事件图能减少身份漂移，并支持局部修复。
3. **结构化证据优于泛化自省。** 编译日志、几何、时序谓词、schema 和引擎状态比无 grounding 的 VLM 总分更可定位；VLM 更适合语义和构图。
4. **长视频首先是状态管理问题。** 随时长与依赖深度增加，布局、旁白对齐和跨场景连续性持续恶化。
5. **裁判也必须被评测。** 已观察到位置偏差、同源偏好和误导性视觉反馈；应报告 critic 检出、定位与回归。
6. **单一总分不安全。** 应使用安全/渲染硬门槛，并分别报告空间、时间、语义、编辑性、任务效果、复现性与成本。
7. **混合系统有价值但不能混类。** 代码草稿后接像素生成可提高真实感，但最终不再是确定性渲染，也可能重新引入幻觉。


## 数据模型与研究方法

- [`data/papers.json`](data/papers.json)：每项工作仅一条去重记录，包含标识、链接、相关性、表示、生成、反馈、任务、数据、评价、发现与限制。
- [`data/resources.json`](data/resources.json)：datasets、benchmarks、systems、tools、showcases。
- [`schema/papers.schema.json`](schema/papers.schema.json) 与 [`schema/resources.schema.json`](schema/resources.schema.json)：JSON Schema 2020-12 契约。
- [`research/core.md`](research/core.md)、[`research/vector_web.md`](research/vector_web.md)、[`research/3d_agents.md`](research/3d_agents.md)、[`research/evaluation.md`](research/evaluation.md)：完整证据 briefs。

方法：arXiv/全文优先；正式会议页、项目页和官方仓库仅补 venue 与 artifact；按稳定标识去重；不推测 venue、规模、代码地址和许可证；冲突采用保守口径。除非特别说明，数字均为作者报告而非独立复现。

## 贡献

请先阅读 [`CONTRIBUTING.md`](CONTRIBUTING.md)，并使用 `git clone https://github.com/Daryl-GSJ/awesome-code-generated-video.git` 克隆仓库。有效贡献应包含一手来源、明确分级理由、真实核验日期、保守元数据和通过 schema 的 JSON。README 保持一行可扫描，细节进入 data 与 research briefs。

参与项目即同意遵守 [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)。仓库元数据采用 [CC0-1.0](LICENSE)。
