# Code-Generated Video 评测研究

> **检索截止时间：2026-10-27。** 本文聚焦“模型生成可执行代码，再由 Remotion / HTML-CSS-SVG-Canvas-Three.js / Manim / Blender 等运行时渲染视频”的评测。检索顺序为 arXiv-first（`paper-tool`），再以官方项目页、官方 GitHub、标准/原作者实现补充。本文区分“直接资源”和“可迁移资源”，避免把像素生成视频、静态 UI-to-code 或一般代码生成的结果直接等同于 code-generated video 能力。

## 1. 结论摘要

截至截止日，最接近通用目标的直接基线是 **Code2Video-Compass**：覆盖 T2V、I2V、V2V，统一使用 Remotion 与 HTML/CSS、SVG、Canvas、Three.js，含 2,104 个任务、10 类视频、24 个子类，并联合评估执行成功、生成 token、视频质量、局部/全局文视对齐、参考保真和主观 checklist。[S1]

但尚无单一 benchmark 同时严谨覆盖：

1. **代码层**：解析、依赖安装、编译、运行、完整渲染和产物可播放；
2. **视频层**：视觉指令遵循、运动/物理、时序一致性、编辑局部性；
3. **系统层**：重复运行一致性、跨机器复现、时延/CPU/GPU/内存/能耗/费用；
4. **代理层**：execution feedback、自我修复、multimodal critique 的收益、代价与回归；
5. **安全层**：不可信代码的文件、网络、进程、资源和秘密信息隔离。

因此，新仓库不宜只复用一个总分。推荐采用 **硬门槛 + 分轴分数 + Pareto 报告**：先以沙箱安全和可执行性作为门槛，再分别报告指令遵循、视觉/时序/物理、编辑局部性、复现性、成本，以及闭环修复能力；禁止用综合平均分掩盖“无法渲染”或“越权执行”。

---

## 2. 任务与评测边界

### 2.1 统一任务定义

给定文本指令，以及可选的参考图、参考视频、既有工程或编辑请求，系统输出：

- 源代码与工程文件；
- 可锁定的依赖与运行配置；
- 渲染后的视频；
- 可选的执行—观察—修复轨迹。

建议至少分四种 track：

| Track | 输入 | 目标 | 代表资源 |
|---|---|---|---|
| T2V-code | 文本 | 从零生成完整可执行视频工程 | Code2Video-Compass、MMMC、ManiBench [S1][S5][S4] |
| I2V-code | 文本 + 关键帧/设计图 | 保留参考外观并生成运动 | Code2Video-Compass [S1] |
| V2V-code / de-rendering | 文本 + 参考视频 | 以代码复刻外观和动态 | Code2Video-Compass、Animation2Code [S1][S3] |
| Edit-code | 既有工程/视频 + 编辑指令 | 只修改目标区域、对象或时间段 | IVEBench、VEFX-Bench、ViTeX-Bench 可迁移 [S15][S16][S17] |

### 2.2 评测对象必须分层

- **代码对象**：源文件、依赖、构建日志、运行日志、退出码、静态安全扫描结果。
- **渲染对象**：逐帧视频、音频、容器元数据、时间戳、关键帧与对象轨迹。
- **过程对象**：每轮 prompt、模型输出、工具调用、执行反馈、critic 反馈、补丁和成本。
- **环境对象**：镜像 digest、运行时/字体/浏览器/ffmpeg/驱动版本、硬件、随机种子、资源限制。

仅看最终 MP4 会遗漏不可复现、越权和高成本；仅看代码会遗漏“成功运行但视觉逻辑错误”。ManiBench 将这种现象称为 visual-logic drift。[S4]

---

## 3. 与 code-generated video 直接相关的现有资源

| 资源 | 数据/任务 | 已覆盖指标或 verifier | 可直接复用 | 主要限制 | 来源 |
|---|---|---|---|---|---|
| **Code2Video-Compass** | 2,104 个 T2V/I2V/V2V 任务；10 类、24 子类；HTML/CSS、SVG、Canvas、Three.js，经 Remotion 渲染 | Execution Success、输出 token、DOVER++ technical quality、Aesthetic Predictor、AMT 插帧误差式运动平滑度、ViCLIP-L 局部文视对齐、全局 embedding 对齐、DINOv3/SSIM/clip 参考保真；MLLM checklist 与整体质量 | 首选主干：任务 taxonomy、三种输入模态、失败样本记零、checklist QA、参考帧/片段对齐 | 尚未系统覆盖编辑局部性、跨环境复现、端到端资源/能耗、安全攻击和多轮修复曲线 | [论文](https://arxiv.org/abs/2610.28416) · [代码](https://github.com/code2video-compass/Code2Video-Compass) · [项目页](https://code2video-compass.github.io/) [S1] |
| **HeyGen Code2Video Benchmark** | 面向短 motion graphics / 产品发布片段的 code-to-video | 强调布局、运动、时机、节奏和视觉润色 | 可作为短营销动画 track 与人工偏好模板 | 商业 benchmark；覆盖面比完整、多场景视频窄 | [官方介绍](https://www.heygen.com/research/introducing-code2video-benchmark) · [Leaderboard](https://www.kaggle.com/benchmarks/heygen/code2video) [S2] |
| **Animation2Code** | 1,069 个 web animation 视频—HTML/CSS/JS 对；视频到代码 de-rendering | 代码可执行率；经帧对齐的 appearance similarity；基于运动轨迹比较的 temporal similarity；含微调与迭代 refinement | 最适合 V2V-code、确定性浏览器渲染、外观与动态解耦评分 | 偏短 web 动画；不覆盖叙事、音频、长视频和一般素材合成 | [论文](https://arxiv.org/abs/2606.28593) · [项目页](https://anya-ji.github.io/animation2code-website/) · [数据](https://huggingface.co/datasets/anim2code/dataset) [S3] |
| **ManiBench** | Manim CE 数学动画；当前论文为 12 题 pilot、5 个难度；分析约 53k 行 ManimGL 代码与 145 个 GL→CE 不兼容点 | Executability、Version-Conflict Error Rate、按必要事件与时序加权的 Alignment、教学元素 Coverage；AST/正则/60 秒沙箱渲染 | API 版本约束、可执行率、时序事件规格、调试与多场景任务模板 | pilot 很小；Alignment/Coverage 主要基于代码关键词，论文明确指出会饱和，不能证明渲染正确 | [论文](https://arxiv.org/abs/2603.13251) · [代码](https://github.com/nabin2004/ManiBench) [S4] |
| **Code2Video / MMMC** | 13 个学科的专业 Manim 教学视频；Planner–Coder–Critic | VLM-as-Judge 美学/结构、生成时间、token 成本、TeachQuiz 知识迁移；scope-guided auto-fix 与视觉 anchor critic | 可迁移到教育/解释视频；适合测 execution feedback、视觉 critique 和教学效用 | 领域集中于教学；TeachQuiz 依赖 VLM unlearning/再学习流程，需额外校准 | [论文](https://arxiv.org/abs/2510.01174) · [代码/数据](https://github.com/showlab/Code2Video) · [项目页](https://showlab.github.io/Code2Video/) [S5] |
| **ManimTrainer / ManimAgent** | 17 个开源 sub-30B 模型、9 种训练/推理组合；ManimBench | Render Success Rate、代码指标、SSIM、CLIP 视觉相似；Renderer-in-the-loop（RITL）和文档增强 RITL-DOC | 直接用于 renderer feedback、自我修复、API 文档反馈的 ablation | 指标仍偏参考相似；不等同通用创意质量，且应独立复验其训练数据与环境 | [论文](https://arxiv.org/abs/2604.18364) · [实现](https://github.com/SuienS/manim-fine-tune-v1) [S6] |
| **ManimBench-v1** | Manim 代码—自然语言描述对 | 可用于训练/评测文本到 Manim 代码与渲染成功 | 可补充 Manim 数据和 code/visual 双评测 | 数据卡所述范围有限；需做数据泄漏、许可证和版本清理 | [数据卡](https://huggingface.co/datasets/SuienR/ManimBench-v1) [S7] |
| **VibeVideoBench** | 239 个中英双语端到端任务、12 类；agent 在 Docker 沙箱内 1 小时交付带声音 MP4 | 程序检查、约 13k rubric、5 个质量维度、3 个 VLM 评审团、盲人偏好；2,151 次 rollout | 首个以原生 coding-agent harness 为对象的 code-driven video benchmark；时间预算与渲染调度可直接复用 | 代码尚未发布；单视频层面评审一致性中等 | [论文](https://arxiv.org/abs/2610.35864) · [项目页](https://vibevideobench.github.io/) |
| **VisPhyBench (VisPhyWorld)** | 108 模板 / 209 场景；物理视频 → 可执行仿真代码 | 重建有效率（97.7%）、视觉相似、物理一致性；多后端对比 | 逆向物理推理与后端选择（Three.js/P5.js vs SVG/Manim）的对照实验 | 仅合成刚体场景 | [论文](https://arxiv.org/abs/2602.13294) · [代码](https://github.com/TIGER-AI-Lab/VisPhyWorld) |

### 3.1 直接资源给出的关键经验

- **执行成功不代表视频正确**：Animation2Code 中模型可接近满执行率，但 temporal similarity 仍明显落后；ManiBench 也显示关键词式 alignment 可在无法执行时虚高。[S3][S4]
- **代码相似度不应作为主指标**：同一视觉结果存在大量等价程序；应以可执行结果和渲染结果为主，代码指标只用于诊断。[S6]
- **局部与全局对齐应拆开**：完整视频可能整体主题正确，但漏掉局部事件或时间位置；Code2Video-Compass 的滑窗局部对齐与全局对齐值得直接采用。[S1]
- **反馈必须外部落地**：renderer/compiler 日志和视觉截图通常比“纯自省”更可靠；但要报告每轮收益、成本和回归，而不是只报最终最好结果。[S5][S6][S21]

---

## 4. 可迁移的数据集、benchmark、指标与 verifier

### 4.1 视频生成：视觉指令遵循、运动、物理与时序

| 资源 | 可迁移内容 | 建议接入方式 | 来源 |
|---|---|---|---|
| **VBench / VBench++ / VBench-2.0** | 16 个细粒度维度（主体/背景一致、闪烁、运动平滑、动作、颜色、空间关系等）；2.0 加入 Human Fidelity、Controllability、Physics、Commonsense | 抽取 prompt suite 和各维度 evaluator；对程序化视频禁用不适用的自然视频先验并重新做人类相关性校准 | [VBench 论文](https://arxiv.org/abs/2311.17982) · [VBench++](https://arxiv.org/abs/2411.13503) · [VBench-2.0](https://arxiv.org/abs/2503.21755) · [统一代码](https://github.com/Vchitect/VBench) [S8] |
| **EvalCrafter** | 真实提示归纳；视觉、内容、运动、文视对齐；约 17/18 个客观指标，并用人类意见拟合组合 | 作为经典多指标池和人类校准范式；不直接照搬其总分权重 | [论文](https://arxiv.org/abs/2310.11440) · [代码](https://github.com/evalcrafter/EvalCrafter) [S9] |
| **T2V-CompBench** | 700 prompts、7 类组合性：属性、空间关系、动作绑定、对象交互、数量等 | 将 prompt 分解成原子断言/checklist；适合视觉指令遵循 | [论文](https://arxiv.org/abs/2407.14505) · [代码](https://github.com/KaiyueSun98/T2V-CompBench) [S10] |
| **TC-Bench** | 初态—终态、概念出现与关系变化的 temporal compositionality；带 ground-truth 视频 | 用状态机/事件图标注程序化动画：前置条件、开始/结束区间、状态转移完成度 | [论文](https://arxiv.org/abs/2406.08656) · [代码](https://github.com/weixi-feng/TC-Bench) [S11] |
| **PhyGenBench / PhyGenEval** | 160 prompts、27 条物理规律、4 个物理域；细粒度物理常识 judge | 为重力、碰撞、流体、刚体、遮挡等可程序化场景建立事件级物理断言 | [论文](https://arxiv.org/abs/2410.05363) · [代码](https://github.com/OpenGVLab/PhyGenBench) [S12] |
| **VideoPhy / VideoPhy2** | 行为/动作中心的物理常识与语义遵循 | 用于动作真实性、人—物交互和高动态片段；与轨迹/速度/接触几何 verifier 组合 | [代码](https://github.com/Hritikbansal/videophy) · [VideoPhy2 项目](https://videophy2.github.io/) [S13] |
| **VideoScore / VideoFeedback** | 人工标注的视觉质量、时序一致、动态程度、文视对齐、事实一致；VideoScore-Bench 约 7,000 视频 | 可作为 learned reward / VLM judge；用 Spearman、pairwise accuracy 与人类判断校准，不当作真值 | [论文](https://arxiv.org/abs/2406.15252) · [代码](https://github.com/TIGER-AI-Lab/VideoScore) [S14] |

### 4.2 编辑局部性与参考保持

| 资源 | 可迁移内容 | 建议接入方式 | 来源 |
|---|---|---|---|
| **IVEBench** | 600 个高质量源视频；覆盖多类 instruction-guided edit；三轴为 Video Quality、Instruction Compliance、Video Fidelity | 构造“应改 mask/时间段”和“禁止改 mask/时间段”，分别测 edit success 与 preservation | [论文](https://arxiv.org/abs/2510.11647) · [代码](https://github.com/RyanChenYN/IVEBench) [S15] |
| **VEFX-Bench / VEFX-Reward** | 通用视频编辑与视觉特效；重点暴露 instruction following 和 edit locality；含数据、reward model、标准 benchmark | 作为 code-edit track 的 learned evaluator，并保留显式像素/对象/时间局部性指标 | [论文](https://arxiv.org/abs/2604.16272) · [代码](https://github.com/Visko-Platform/VEFX-Bench) [S16] |
| **ViTeX-Bench** | 387 个 720p 真实视频、精确文本区域 mask、编辑指令；文本正确、视觉质量、编辑局部性共 13 项指标 | 对字幕、标题、数字、标签替换尤其适用；使用 OCR 正确率 + mask 内改变 + mask 外保持 | [项目页](https://vitex-bench.github.io/) [S17] |
| **LOVEU-TGVE** | 公开 text-guided video editing competition 数据与提交格式 | 用作早期兼容集和人工评测协议参考 | [官方代码](https://github.com/showlab/loveu-tgve-2023) [S18] |

### 4.3 代码执行、execution feedback、自我修复与 verifier

| 资源 | 可迁移内容 | 建议接入方式 | 来源 |
|---|---|---|---|
| **HumanEval** | 单元测试执行、pass@k；官方明确警告不可信生成代码必须在强沙箱运行 | 借用 pass@k 与执行 harness 设计；视频任务主报 render-pass@k，不仅是 parse-pass@k | [论文](https://arxiv.org/abs/2107.03374) · [代码](https://github.com/openai/human-eval) [S19] |
| **InterCode** | 把代码作为 action、执行反馈作为 observation；Bash/SQL/Python；自包含 Docker 环境 | 定义 generate→execute→observe→patch 的标准轨迹；记录每轮 reward、动作数与 wall time | [论文](https://arxiv.org/abs/2306.14898) · [代码](https://github.com/princeton-nlp/intercode) [S20] |
| **Self-repair 系统研究** | 在 HumanEval/APPS 上发现：考虑成本后，自修复收益常有限，瓶颈在反馈质量；强外部反馈更有效 | 必须与 compute-matched best-of-N 比较，并报告修复成功、破坏原正确样本和边际收益 | [论文](https://arxiv.org/abs/2306.09896) [S21] |
| **LEVER** | 联合自然语言、代码和执行结果训练 verifier，再重排候选 | 视频场景可输入 prompt + code + logs + sampled frames，学习预测最终正确性 | [论文](https://arxiv.org/abs/2302.08468) [S22] |
| **FeedbackEval** | compiler、test、expert、混合反馈；单轮/多轮修复；收益通常在 2–3 轮后递减 | 设计反馈类型 ablation；严格限制轮数并画 cost–success 曲线 | [论文](https://arxiv.org/abs/2504.06939) [S23] |
| **SWE-bench** | Docker 可复现评测、真实项目 issue、patch 是否通过 fail-to-pass/pass-to-pass tests | 借用实例镜像、补丁评测、回归测试和环境 digest；每题独立镜像 | [官方代码](https://github.com/SWE-bench/SWE-bench) · [官方文档](https://www.swebench.com/SWE-bench/) [S24] |
| **CodeSecEval** | 255 个 Python 任务、77 个 CWE；功能测试 + 漏洞定向测试；支持生成和修复 | 建立“功能正确但不安全”的双 oracle；扩充视频运行时特有 CWE/越权行为 | [论文](https://arxiv.org/abs/2407.02395) [S25] |

### 4.4 Multimodal critique 与视觉代码生成

| 资源 | 可迁移内容 | 建议接入方式 | 来源 |
|---|---|---|---|
| **Design2Code** | 真实网页 screenshot-to-code；语义、结构、视觉保真 | 把静态首/中/末帧布局作为 spatial verifier；不要替代运动评估 | [论文/项目](https://salt-nlp.github.io/Design2Code/) · [代码](https://github.com/NoviScl/Design2Code) [S26] |
| **Vision-Guided Iterative Refinement for Frontend Code Generation** | VLM critic 读取实际渲染页面，给结构化反馈并迭代代码 | 直接迁移为“采样关键帧 + 时间轴摘要 + 结构化 critique”；报告每轮增益与失败回归 | [论文](https://arxiv.org/abs/2604.05839) [S27] |
| **R³-Bench** | Reason–Reflect–Rectify 闭环；区分 reflective verdict 和 rectification | 分开测“是否发现问题”和“是否修对问题”，避免把 critic 识别能力与 actor 修改能力混成一个分数 | [代码](https://github.com/xiaomoguhz/R3-Bench) [S28] |
| **MMC** | actor–critic、多模态 critique 数据、MCTS 生成纠错路径 | 用于训练/评估 frame-grounded critique；要求反馈带帧号、bbox/track、违反的原子约束 | [论文](https://arxiv.org/abs/2504.11009) [S29] |

### 4.5 视觉质量、成本、复现与沙箱基础设施

| 资源 | 可迁移内容 | 注意事项 | 来源 |
|---|---|---|---|
| **VMAF / PSNR / SSIM / MS-SSIM** | 有参考视频/参考帧的技术质量与结构保持；官方 libvmaf 同时实现多指标 | 对创意 T2V 无参考任务不适用；必须固定缩放、色彩空间、fps 与时间对齐 | [Netflix VMAF](https://github.com/Netflix/vmaf) [S30] |
| **CLIPScore** | 图文 embedding 相似，可做粗粒度 prompt alignment | 原本是图像描述评测；逐帧平均会忽略顺序、绑定和物理，不可单独使用 | [论文](https://arxiv.org/abs/2104.08718) · [代码](https://github.com/jmhessel/clipscore) [S31] |
| **FVD / Beyond FVD / content-bias 分析** | 分布级视频质量；对整体生成集合做比较 | FVD 对 temporal distortion 可能不敏感、受内容偏置且样本量敏感；不能当单视频时序 verifier | [Beyond FVD](https://arxiv.org/abs/2410.05203) · [Content Bias](https://content-debiased-fvd.github.io/) [S32] |
| **MLPerf Inference / MLPerf Power** | 标准化 latency、throughput、功耗/能耗测量思想 | 视频任务应报告每成功视频和每有效秒，而非只报单次调用 | [Inference 代码](https://github.com/mlcommons/inference) · [Power 论文](https://arxiv.org/abs/2410.12032) [S33] |
| **SWE-ReX / Docker 思路** | 每实例可重建、资源隔离、执行审计 | Docker 便于复现但不是完整安全边界；高风险执行应叠加 rootless、seccomp、只读根文件系统、网络默认拒绝，必要时 gVisor/microVM | [SWE-bench 组织](https://github.com/swe-bench) · [InterCode](https://github.com/princeton-nlp/intercode) [S34] |

---

## 5. 指标与 verifier 设计建议

### 5.1 代码可执行率、编译/运行成功率

不要只报一个“成功率”，应保留阶段化漏斗：

1. `parse_rate`：语法/AST/TS parser 成功；
2. `dependency_resolve_rate`：锁定依赖后可安装；
3. `compile_rate`：TypeScript/build/bundle 成功；
4. `runtime_start_rate`：入口可启动；
5. `render_complete_rate`：在超时与资源限额内完成所有帧；
6. `artifact_valid_rate`：ffprobe 可读，时长/fps/分辨率/音轨满足契约；
7. `usable_video_rate`：无空白、冻结、全黑、缺帧或严重截断。

核心报告：

- `render-pass@1`；若允许多采样再报无偏 `render-pass@k`；
- 按错误类型分桶：syntax、missing dependency、API/version、asset、browser、OOM、timeout、encoder、security violation；
- 所有失败样本在下游主分中记 0，同时另报“conditional-on-success”诊断分，防止只剔除难例造成虚高。[S1][S19]

### 5.2 视觉指令遵循

将每条 prompt 编译为原子、可验证 checklist：

- 实体存在/数量；
- 属性绑定（颜色、字体、材质、形状）；
- 空间关系；
- 动作绑定与相互作用；
- 摄像机/转场；
- 文本/OCR 与数字；
- 事件先后与时间窗口；
- 音画要求。

建议分数：`atomic_constraint_recall`、`all_constraints_pass`、按难度加权的 `checklist_score`。Verifier 采用 **专用 detector/OCR/track/几何规则优先，VLM judge 兜底**；VLM 输出必须引用帧号和证据，且用人工集校准 pairwise accuracy、Spearman/Kendall 与置信度。[S1][S10][S14]

### 5.3 运动与物理一致性

至少拆为：

- 运动存在与动态程度；
- 轨迹、速度、加速度、方向；
- 运动平滑与 jerk；
- 物体 identity/形状在运动中的保持；
- 接触、碰撞、支撑、遮挡；
- 重力、惯性、弹性、流体等物理规律；
- 动作是否完成，而非只有起始姿态。

Verifier 组合：tracking/optical flow + 事件检测 + 物理规则 + 视频 VLM。运动平滑不能奖励静止视频：需同时设 `required_motion_completion` 门槛，再计算 smoothness；FVD、逐帧 CLIP、仅插帧误差都不能独立证明物理正确。[S8][S12][S13][S32]

### 5.4 时序一致性

建议四层：

1. **帧级**：flicker、纹理抖动、字幕跳动；
2. **对象级**：identity、颜色、大小、拓扑和轨迹连续；
3. **事件级**：事件完整性、先后顺序、持续时间、状态转移；
4. **叙事级**：跨场景因果、指代和主题连续。

参考视频任务优先采用 Animation2Code 的外观/时序解耦思想；开放式 T2V 则用 TC-Bench 式初态—终态与事件图，不强迫像素对齐。[S3][S11]

### 5.5 编辑局部性

每个编辑任务保存四类区域：

- `target_spatial_mask`：应改变区域；
- `preserve_spatial_mask`：不应改变区域；
- `target_time_ranges`：应改变时间；
- `preserve_time_ranges`：不应改变时间。

推荐同时报告：

- `edit_success_in_target`；
- `preservation_outside_target`；
- `temporal_spill`（修改扩散到邻近帧）；
- `identity_preservation`；
- `code_diff_locality`（修改文件/组件/行数，仅作诊断）；
- `regression_pass_rate`。

总分可取 target success 与 preservation 的调和平均，但二者原始值必须保留。文本编辑增加 OCR CER/WER 与非文本区域保持。[S15][S16][S17]

### 5.6 可复现性

同一提交至少运行 3 次，并分三档：

- **同容器重复**：相同 seed 和环境；
- **冷启动重建**：从 lockfile 和镜像重新安装；
- **跨执行节点**：相同 ISA/不同机器，必要时另设跨 OS track。

记录：代码 hash、镜像 digest、依赖 lock、字体/浏览器/ffmpeg/driver、seed、环境变量白名单、输入素材 hash。指标：

- `build_repro_rate`；
- `bit_exact_rate`（适用时）；
- `perceptual_repro_score`；
- `metric_std_across_runs`；
- `cross_machine_success_rate`。

对浏览器/GPU 非确定性，不应强制 bit-exact；应同时使用 ffprobe 元数据一致性、帧 hash 容差与感知距离。[S24][S34]

### 5.7 渲染成本

至少报告：

- 模型侧：输入/输出 token、API 费用、模型 wall time；
- 构建侧：依赖安装、bundle/compile 时间；
- 渲染侧：端到端 wall time、CPU/GPU 时间、峰值 RSS/VRAM、磁盘/网络 I/O；
- 能耗侧：Wh/J（可测时）；
- 归一化：`cost_per_success`、`seconds_per_rendered_second`、`joules_per_rendered_second`、`cost_per_quality_point`。

失败尝试与所有修复轮次都计入成本。比较自我修复与 best-of-N 时必须 compute-matched。[S1][S5][S21][S33]

### 5.8 安全沙箱

生成代码一律视为不可信。每实例使用一次性、无特权执行环境，最低要求：

- 非 root 用户；只读 rootfs；仅工作目录可写；
- 默认禁网，素材通过预下载、hash 校验的只读挂载提供；
- 不注入宿主凭据；环境变量白名单；阻断 metadata service；
- seccomp/AppArmor/SELinux；drop all capabilities；禁止 privileged、宿主 socket 和设备直通；
- PID、CPU、内存、GPU、磁盘、文件数、进程数、wall time 配额；
- 拦截 fork bomb、路径穿越、symlink escape、`/proc`/`/sys` 探测、端口监听和子进程逃逸；
- 高风险/多租户场景使用 gVisor/Kata/Firecracker 等更强隔离；
- 保存 syscall/文件/网络/进程审计日志，命中策略即 `security_pass=0`。

安全评分必须是门槛，而非可以被画质抵消的软分。Docker 提供复现便利但不应被表述为绝对安全边界；HumanEval 官方也明确要求强沙箱。[S19][S20][S25][S34]

---

## 6. Execution feedback、自我修复与 multimodal critique 的专门评测

### 6.1 标准闭环

统一为：

`generate → static-check → execute/render → collect evidence → critique → patch → re-run`

每轮保存完整 trace，且设置相同的最大轮数、token、wall time、工具调用和渲染预算。

### 6.2 四个独立能力

| 能力 | 测什么 | 指标 |
|---|---|---|
| Fault detection | critic 能否发现真实问题 | precision/recall、frame-grounding IoU、错误类型准确率 |
| Fault localization | 能否定位文件/组件/帧/对象/时间段 | file/line top-k、frame interval IoU、bbox/track IoU |
| Repair efficacy | 修改后目标问题是否消失 | repair success、Δquality、iterations-to-pass |
| Non-regression | 是否破坏原本正确部分 | regression rate、preservation、new security violations |

### 6.3 必需对照组

1. 单次生成；
2. 同模型纯 self-critique；
3. compiler/runtime feedback；
4. renderer frame/video feedback；
5. 独立 VLM critic；
6. 混合反馈；
7. compute-matched best-of-N + verifier selection；
8. oracle/human feedback 小样本上界。

报告 `success@round-r`、累积成本、每轮边际增益和“正确→错误”转移矩阵。FeedbackEval 与 self-repair 研究说明，多轮收益会递减，反馈质量比“是否自省”更关键。[S21][S23]

### 6.4 防止 critic 投机

- critic 不得读取隐藏参考实现；
- judge 与 generator/critic 尽量不同家族；
- 随机交换候选顺序，检查位置偏差；
- 加入“无需修改”的阴性样本，测过度编辑；
- critique 必须绑定可验证证据；
- 用盲人工子集测 judge-human 一致性；
- 公开 judge prompt、版本、采样参数和原始输出。

---

## 7. 现有评测盲区

| 盲区 | 为什么重要 | 现有资源缺口 | 推荐补法 |
|---|---|---|---|
| 执行漏斗不完整 | “可解析”与“完整可播放”差异巨大 | 多数论文只报 render/execution 一项 | 分阶段状态机与错误 taxonomy |
| 音频与音画同步 | 完整视频常含旁白、音乐、音效 | 主流 code-video benchmark 仍以视觉为主 | ASR 文本正确、音频质量、事件—音效时间偏差、响度/削波 |
| 长时叙事与跨场景状态 | 10 秒内正确不代表 1–5 分钟稳定 | Animation2Code 偏短，MMMC 领域较窄 | 长度分桶；跨场景 entity/state graph |
| 运动平滑与运动正确混淆 | 静止视频可获得高平滑分 | 多个 smoothness 指标有静止偏好 | 先过动作完成门槛，再评分平滑/jerk |
| 物理 judge 可被视觉 plausibility 欺骗 | “看起来像”不等于满足物理规律 | VLM judge 难作精确测量 | 可控合成场景 + 轨迹/碰撞/守恒规则 oracle |
| 开放式创意缺少唯一参考 | 像素相似会惩罚合法多样性 | 参考指标不适合 T2V-code | checklist + 无参考质量 + 人类 pairwise；参考分仅用于 I2V/V2V |
| 编辑局部性缺少代码—画面联动 | 代码 diff 小不等于视觉影响小，反之亦然 | 编辑 benchmark 多只看视频 | 同时记录 code dependency slice 与时空影响 mask |
| 复现性未成为主指标 | 字体、浏览器、GPU、依赖漂移会改结果 | 直接 benchmark 多固定单环境 | 三档重复实验、镜像 digest、lockfile 和方差 |
| 成本报告不完整 | 多轮 agent 可用大量 token/渲染换分 | 常只报输出 token 或生成时间 | 全生命周期成本；失败也计费；Pareto frontier |
| 沙箱安全缺少攻击集 | 生成代码可能读密钥、联网、炸资源 | Docker 常被误当作安全答案 | benign + adversarial 双集，策略命中、逃逸与越权测试 |
| 自修复只报最终最好分 | 会掩盖回归、挑样和预算差异 | 多数闭环工作未做 compute match | 轨迹级评测、best-of-N 对照、边际增益/回归 |
| judge 污染与同源偏差 | 同家族 generator/judge 可能偏好自己的风格 | learned evaluator 依赖模型版本 | 多 judge + 人工校准 + 固定版本 + 证据输出 |
| 数据泄漏与模板记忆 | CodePen、公开 Manim、网页代码可能已在预训练中 | 公开资源难排除记忆 | 时间切分、私有 holdout、变体生成、代码相似/URL 去重 |
| 可访问性与文本准确性 | 字幕溢出、对比度和可读性影响实用性 | 美学分无法覆盖 | OCR、safe-area、contrast、font size、caption timing |
| 资产来源和外部依赖 | 网络素材会造成不可复现或越权 | benchmark 常只看成片 | 资产 manifest、hash、离线镜像、缺失资产测试 |

---

## 8. 推荐的最小 benchmark schema

### 8.1 最小任务集

建议首版 **240 个公开开发题 + 隐藏测试集**，分层抽样：

- 80 个 T2V-code；
- 40 个 I2V-code；
- 40 个 V2V-code / de-rendering；
- 40 个 Edit-code；
- 20 个 execution-feedback/debug；
- 20 个 adversarial sandbox/safety。

每个 track 覆盖短/中/长时长、2D/3D、文本/图表/UI/角色/抽象 motion、单/多场景，以及低/中/高 construction、dynamic、state-dependency 难度。公开 dev 集提供完整 oracle；测试集隐藏部分 checklist、安全攻击和回归测试。

### 8.2 最小数据记录

```yaml
schema_version: "1.0"
task_id: "cgv_t2v_000001"
track: "t2v_code"                 # t2v_code | i2v_code | v2v_code | edit_code | repair
category: "data_infographic"
subtype: "animated_bar_chart"
difficulty:
  construction: 2                  # 1..3
  dynamics: 2
  state_dependency: 3
instruction: "..."
inputs:
  images: []                       # {uri, sha256, role}
  videos: []                       # {uri, sha256, role, time_range}
  starter_repo: null
output_contract:
  runtime: "remotion"
  entrypoint: "src/index.ts"
  duration_s: 12
  fps: 30
  width: 1920
  height: 1080
  audio_required: false
  allowed_dependencies: "manifest.lock"
assertions:
  - id: "a1"
    type: "entity_attribute"
    text: "蓝色柱表示类别 A"
    weight: 1.0
    time_range: [0.0, 12.0]
    spatial_region: null
    verifier: "detector_color_rule"
  - id: "a2"
    type: "event_order"
    text: "标题出现后柱状图依次增长"
    weight: 2.0
    time_range: [0.0, 6.0]
    verifier: "event_graph"
edit_spec: null                    # target/preserve spatial masks and time ranges
reference:
  code: null
  images: []
  video: null
  event_graph: "events.json"
sandbox_policy:
  network: "deny"
  cpu_cores: 4
  memory_mb: 8192
  gpu: false
  wall_time_s: 180
  writable_paths: ["/workspace"]
  secret_access: "deny"
seeds: [11, 23, 47]
license_and_provenance:
  source: "curated"
  asset_manifest: "assets.json"
  split: "test"
```

### 8.3 最小运行记录

```yaml
run_id: "..."
model:
  name: "..."
  version: "..."
  decoding: {temperature: 0, top_p: 1, seed: 11}
environment:
  image_digest: "sha256:..."
  lockfile_hash: "sha256:..."
  runtime_versions: {node: "...", chromium: "...", ffmpeg: "..."}
  hardware: {cpu: "...", gpu: null}
trajectory:
  - round: 0
    prompt_hash: "sha256:..."
    output_hash: "sha256:..."
    tool_calls: []
    execution_feedback: null
  - round: 1
    execution_feedback: {exit_code: 1, error_type: "api_version"}
    critic_feedback: {frames: [42], assertion_ids: ["a2"]}
artifacts:
  source_hash: "sha256:..."
  video_hash: "sha256:..."
  logs_hash: "sha256:..."
status:
  parse: true
  dependencies: true
  compile: true
  runtime_start: true
  render_complete: true
  artifact_valid: true
  security_pass: true
metrics:
  instruction_following: 0.0
  temporal_consistency: 0.0
  motion_physics: 0.0
  visual_quality: 0.0
  edit_locality: null
  reproducibility: 0.0
cost:
  input_tokens: 0
  output_tokens: 0
  api_cost_usd: 0.0
  wall_time_s: 0.0
  render_time_s: 0.0
  peak_rss_mb: 0
  peak_vram_mb: null
  energy_wh: null
```

### 8.4 最小 verifier 栈

按确定性和专用性从高到低：

1. **静态 verifier**：parser、AST、依赖 allowlist、锁文件、危险 API/命令扫描；
2. **执行 verifier**：分阶段退出状态、日志分类、ffprobe、空白/冻结/缺帧检测；
3. **规则 verifier**：OCR、颜色/几何、对象计数、时间窗口、事件图、mask 局部性；
4. **视觉 verifier**：detector、tracker、optical flow、DINO/LPIPS/SSIM/VMAF、动作/物理模型；
5. **VLM judge**：只处理规则难覆盖的语义与整体创意，输出证据；
6. **人工审计**：每个版本固定抽样，校准自动指标并复核安全失败。

每个 verifier 必须固定版本、阈值和输入预处理，并在人工标注校准集上报告：accuracy/F1、Spearman/Kendall、pairwise accuracy、分组误差与置信区间。

### 8.5 最小 leaderboard 指标

**硬门槛：**

- `security_pass_rate`；
- `render-pass@1`；
- `artifact_valid_rate`。

**质量分轴：**

- Instruction Following：原子 checklist + all-correct；
- Visual Quality：technical + aesthetic；
- Motion/Physics：motion completion + smoothness + physical correctness；
- Temporal：frame/object/event/narrative；
- Edit Locality：target success + outside preservation；
- Reproducibility：重复与重建成功率、跨运行方差。

**效率与闭环：**

- end-to-end latency、rendered-second ratio、token、费用、峰值资源、能耗；
- first-pass success、repair uplift、iterations-to-pass、regression rate；
- cost-matched success 与 quality–cost Pareto frontier。

不建议只公布单一总分。若产品必须排序，可使用以下 gated score，并同时展示所有原始轴：

```text
eligible = security_pass AND artifact_valid
quality  = geometric_mean(
  instruction_following,
  visual_quality,
  motion_physics,
  temporal_consistency,
  edit_locality_if_applicable
)
final = eligible * render_complete * quality
```

几何平均能惩罚短板，但复现性和成本仍应独立展示，不能被画质抵消。

---

## 9. 推荐实施优先级

### P0：能安全、可复现地跑

- 冻结两条 runtime：Remotion/web stack 与 Manim CE；
- 建立一次性沙箱、默认禁网、资源配额、审计日志；
- 实现 parse→dependency→compile→run→render→artifact 漏斗；
- 固定镜像 digest、lockfile、字体和 ffmpeg/browser 版本。

### P1：建立可解释的核心质量轴

- 采用 Code2Video-Compass taxonomy 和 checklist；
- 接入 OCR、对象检测/跟踪、事件图、局部/全局文视对齐；
- 用 Animation2Code 的 appearance/temporal 解耦；
- 用 TC-Bench、PhyGenBench、IVEBench/VEFX-Bench 补时序、物理和局部编辑。

### P2：评测 agent 闭环

- 实现 InterCode 式 action–observation trace；
- 分离 compiler/runtime、renderer 和 VLM critique；
- 加入纯 self-critique、best-of-N、oracle feedback 对照；
- 报告每轮收益、回归和全成本。

### P3：人类校准与长期治理

- 建立 10%–15% 双人盲评集，分任务类型报告一致性；
- 固定 judge 版本并保留原始证据；
- 每次 runtime/metric 升级重跑锚点集；
- 使用时间切分和私有 holdout 控制数据污染。

---

## 10. 来源索引

- **[S1]** Chen et al., *Code2Video-Compass*, 2026：[arXiv](https://arxiv.org/abs/2610.28416)，[GitHub](https://github.com/code2video-compass/Code2Video-Compass)。
- **[S2]** HeyGen Research, *Code2Video Benchmark*：[官方页](https://www.heygen.com/research/introducing-code2video-benchmark)。
- **[S3]** Ji et al., *Animation2Code*, 2026：[arXiv](https://arxiv.org/abs/2606.28593)，[项目页](https://anya-ji.github.io/animation2code-website/)。
- **[S4]** Oli, *ManiBench*, 2026：[arXiv](https://arxiv.org/abs/2603.13251)，[GitHub](https://github.com/nabin2004/ManiBench)。
- **[S5]** Chen et al., *Code2Video: A Code-centric Paradigm for Educational Video Generation*, 2025：[arXiv](https://arxiv.org/abs/2510.01174)，[GitHub](https://github.com/showlab/Code2Video)。
- **[S6]** Silva et al., *Training and Agentic Inference Strategies for LLM-based Manim Animation Generation*, 2026：[arXiv](https://arxiv.org/abs/2604.18364)。
- **[S7]** *ManimBench-v1*：[Hugging Face](https://huggingface.co/datasets/SuienR/ManimBench-v1)。
- **[S8]** Huang et al., *VBench* / *VBench++*；Zheng et al., *VBench-2.0*：[GitHub](https://github.com/Vchitect/VBench)。
- **[S9]** Liu et al., *EvalCrafter*, CVPR 2024：[arXiv](https://arxiv.org/abs/2310.11440)，[GitHub](https://github.com/evalcrafter/EvalCrafter)。
- **[S10]** Sun et al., *T2V-CompBench*, CVPR 2025：[arXiv](https://arxiv.org/abs/2407.14505)，[GitHub](https://github.com/KaiyueSun98/T2V-CompBench)。
- **[S11]** Feng et al., *TC-Bench*：[arXiv](https://arxiv.org/abs/2406.08656)，[GitHub](https://github.com/weixi-feng/TC-Bench)。
- **[S12]** Meng et al., *PhyGenBench*：[arXiv](https://arxiv.org/abs/2410.05363)，[GitHub](https://github.com/OpenGVLab/PhyGenBench)。
- **[S13]** Bansal et al., *VideoPhy*：[GitHub](https://github.com/Hritikbansal/videophy)。
- **[S14]** He et al., *VideoScore*, EMNLP 2024：[arXiv](https://arxiv.org/abs/2406.15252)，[GitHub](https://github.com/TIGER-AI-Lab/VideoScore)。
- **[S15]** Chen et al., *IVEBench*, ICLR 2026：[arXiv](https://arxiv.org/abs/2510.11647)，[GitHub](https://github.com/RyanChenYN/IVEBench)。
- **[S16]** Gao et al., *VEFX-Bench*, 2026：[arXiv](https://arxiv.org/abs/2604.16272)，[GitHub](https://github.com/Visko-Platform/VEFX-Bench)。
- **[S17]** *ViTeX-Bench*：[项目页](https://vitex-bench.github.io/)。
- **[S18]** LOVEU-TGVE 2023：[GitHub](https://github.com/showlab/loveu-tgve-2023)。
- **[S19]** Chen et al., *Evaluating Large Language Models Trained on Code* / HumanEval：[arXiv](https://arxiv.org/abs/2107.03374)，[GitHub](https://github.com/openai/human-eval)。
- **[S20]** Yang et al., *InterCode*, NeurIPS 2023 Datasets & Benchmarks：[arXiv](https://arxiv.org/abs/2306.14898)，[GitHub](https://github.com/princeton-nlp/intercode)。
- **[S21]** Olausson et al., *Is Self-Repair a Silver Bullet for Code Generation?*：[arXiv](https://arxiv.org/abs/2306.09896)。
- **[S22]** Ni et al., *LEVER*：[arXiv](https://arxiv.org/abs/2302.08468)。
- **[S23]** Dai et al., *FeedbackEval*：[arXiv](https://arxiv.org/abs/2504.06939)。
- **[S24]** Jimenez et al., *SWE-bench*：[GitHub](https://github.com/SWE-bench/SWE-bench)，[官方文档](https://www.swebench.com/SWE-bench/)。
- **[S25]** Wang et al., *CodeSecEval*：[arXiv](https://arxiv.org/abs/2407.02395)。
- **[S26]** Si et al., *Design2Code*：[项目页](https://salt-nlp.github.io/Design2Code/)，[GitHub](https://github.com/NoviScl/Design2Code)。
- **[S27]** Sansford et al., *Vision-Guided Iterative Refinement for Frontend Code Generation*, 2026：[arXiv](https://arxiv.org/abs/2604.05839)。
- **[S28]** *R³-Bench*：[GitHub](https://github.com/xiaomoguhz/R3-Bench)。
- **[S29]** Liu et al., *MMC: MCTS-based Multimodal Critique*：[arXiv](https://arxiv.org/abs/2504.11009)。
- **[S30]** Netflix, *VMAF*：[GitHub](https://github.com/Netflix/vmaf)。
- **[S31]** Hessel et al., *CLIPScore*, EMNLP 2021：[arXiv](https://arxiv.org/abs/2104.08718)，[GitHub](https://github.com/jmhessel/clipscore)。
- **[S32]** Luo et al., *Beyond FVD*：[arXiv](https://arxiv.org/abs/2410.05203)；Ge et al., *On the Content Bias in FVD*：[项目页](https://content-debiased-fvd.github.io/)。
- **[S33]** MLCommons, *MLPerf Inference / Power*：[Inference](https://github.com/mlcommons/inference)，[Power](https://arxiv.org/abs/2410.12032)。
- **[S34]** SWE-bench execution infrastructure：[GitHub organization](https://github.com/swe-bench)；InterCode Docker environments：[GitHub](https://github.com/princeton-nlp/intercode)。
