# Code-Generated Video 的向量图形、Web 视觉程序与程序合成研究

> 检索截止：**2026-10-27**  
> 范围：text-to-SVG、HTML/Canvas/WebGL 视觉代码生成、creative coding、visual program synthesis、diagram/animation code generation、可微/程序化图形，以及其中能直接启发 code-generated video 的工作。  
> 方法：按 **arXiv-first** 流程，先用 `paper-tool` 检索并阅读全文；arXiv 覆盖不足时再以 Web Search 补查论文主页、会议页与项目页。以下优先链接 arXiv 版本，并按论文的**实际输出物**严格分层，而不是按标题中的 “video / animation” 字样分类。

## 1. 分层标准与结论

### 1.1 严格分层

- **Core（直接生成视频代码）**：模型或 agent 直接产生可执行的动画/视频程序（如 HTML/CSS/JS、SVG animation、Manim、逐帧 HTML/Canvas/Three.js），或专门研究这类程序的验证、训练、评测与自改进。
- **Adjacent（生成视觉程序，可迁移到视频）**：输出可执行、可渲染、可编辑的视觉程序，但主要目标是静态 SVG、TikZ、网页或 creative coding；或生成可编辑向量动画，但核心求解不是代码生成。必须能明确迁移到时间维度、执行反馈或结构化编辑。
- **Background（仅基础）**：提供可微渲染、神经符号图形程序合成等基础机制，本身不解决现代 code-generated video。

### 1.2 核心判断

1. **该方向已经从“LLM 写一段动画代码”发展为完整闭环**：规划 → 代码 → 确定性渲染 → 时空/布局验证 → 定位修复 → 可审计记忆。
2. **最大缺口不是语法，而是时间推理**：Animation2Code 中代码执行率可接近 100%，外观相似度最高约 0.84，但时间相似度最高仅约 0.31；“能运行”远不等于“动得对”。
3. **中间表示决定上限**：VAnim 的持久 DOM + Sparse State Updates、MG-Gen 的层级 HTML、Manim 的场景对象、Reels-RSI 的 script/storyboard/frame program，都比逐帧像素或逐帧完整代码更利于身份保持、局部编辑和长时序生成。
4. **视觉反馈必须结构化**：单一 CLIP/VLM 分数信息密度不足；更有效的是中间渲染、对象轨迹、时序谓词、锚点、浏览器几何检查和失败定位。
5. **评测需拆开五层**：执行成功、静态外观、运动/时序、结构可编辑性、最终沟通效果。只看首帧、CLIP 或代码相似度会严重高估能力。
6. **截至截止日，通用栈评测刚出现**：Code2Video-Compass 首次把 Remotion + HTML/CSS/SVG/Canvas/Three.js、T2V/I2V/V2V 和完整视频质量放在同一基准中，但开放世界长视频、多镜头一致性和可靠自动修复仍未解决。

---

## 2. Core：直接生成或验证视频代码

### C1. Code2Video-Compass: A Comprehensive Benchmark for General-Purpose Code-Based Video Generation across T2V, I2V, and V2V

- **元数据**：Zhenghan Chen, Zekai Shao, Xin Lin, Leting Cheng, Siming Chen；2026；预印本；[arXiv:2610.28416v1](https://arxiv.org/abs/2610.28416v1)；项目采用 Remotion，目标栈含 HTML/CSS、SVG、Canvas、Three.js。
- **主要发现**：提出 2,104 个任务、10 类视频、24 个子类，同时覆盖 text-to-video、image-to-video、video-to-video。以 construction、dynamic animation、state dependency 三轴标注复杂度；评测结合 12 个客观指标与 5 个主观指标。对 9 个模型家族的 15 个 MLLM 评测显示，执行可靠性与成片质量并不同步，复杂度上升时普遍退化。
- **限制**：基准重于诊断而非新生成算法；短参考片段和既定 Remotion 工具链不能代表任意长片、复杂音频或交互视频；MLLM judge 仍可能有偏差。
- **为何相关**：这是目前最接近新仓库目标的**通用 code-generated video 基准蓝图**。可直接借鉴任务分类、三维复杂度、执行沙箱，以及“技术成功 + 视觉质量 + 指令遵循 + 参考保真”的双层评测。

### C2. Reels-RSI: Program-Level Self-Improvement for Code-Rendered Explainer Videos

- **元数据**：Wei Lin；2026；预印本；[arXiv:2610.14495v1](https://arxiv.org/abs/2610.14495v1)；[代码与规则](https://github.com/agentic-loops-x/Reels-RSI)。
- **主要发现**：把解释视频定义为 script、storyboard 与逐帧 animation program，经确定性渲染得到视频。提出四层程序记忆：运行日志/快照、带作用域的 lessons、带 must-fail/must-pass 的可执行规则、基准门控的 playbook 演化。规则既能回溯审计旧作品，也能约束后续生成；论文同时揭示 pairwise judge 的位置偏置和“画面更精致但事实丢失”的风险。
- **限制**：单系统、单模型家族、小规模 field study；无大规模人类偏好研究；结果不能当作普遍效应量。
- **为何相关**：直接给出仓库级 agent 的工程范式：**视频是可 lint、diff、test、audit 的程序**。尤其适合把失败案例沉淀为跨模型可复用的静态检查，而不是只改 prompt。

### C3. Code2Video: A Code-centric Paradigm for Educational Video Generation

- **元数据**：Yanzhe Chen, Kevin Qinghong Lin, Mike Zheng Shou；2025；预印本；[arXiv:2510.01174](https://arxiv.org/abs/2510.01174)；[项目](https://showlab.github.io/Code2Video/)。
- **主要发现**：Planner 规划时间流与素材，Coder 生成可执行 Manim/Python 并做 scope-guided auto-fix，Critic 用视觉锚点改进空间布局。提出 MMMC 与 TeachQuiz，以“观看视频后能否恢复知识”衡量教学效果；完整 agent 相对直接代码生成有显著提升。
- **限制**：集中于教育视频和 Manim；VLM 评审及“先遗忘再学习”的 TeachQuiz 具有模型依赖；论文中的人类视频对比不等价于开放域创意质量。
- **为何相关**：证明 code video 不应只优化画面相似度，而应优化**任务结果**。Planner/Coder/Critic 分工与 temporal flow / spatial layout 解耦，是通用视频 agent 的合理骨架。

### C4. Animation2Code: Evaluating Temporal Visual Reasoning in Video-to-Code Generation

- **元数据**：Anya Ji, Abhijith Varma Mudunuri, David M. Chan, Alane Suhr；2026；预印本；[arXiv:2606.28593v1](https://arxiv.org/abs/2606.28593v1)；1,069 个 web animation 视频—代码对。
- **主要发现**：把视频反演为自包含 HTML（内联 CSS/JS），再确定性浏览器渲染；分别提出 appearance similarity 与 temporal similarity。当前 VLM 即使执行率近乎完美、外观重建较好，时间动态仍明显失败；微调与迭代修复也未消除差距。
- **限制**：数据主要来自自动播放的 CodePen 动画，偏短、偏 Web motion graphics；不覆盖音频、多镜头叙事或复杂 3D；相同视频可由多种等价程序产生，代码级监督天然多解。
- **为何相关**：为 video-to-code 提供最直接的数据、渲染环境和**静态/动态解耦指标**；也警示仓库不要用逐帧图像平均分掩盖错误节奏、相位、轨迹和循环周期。

### C5. VAnim: Rendering-Aware Sparse State Modeling for Structure-Preserving Vector Animation

- **元数据**：Guotao Liang, Zhangcheng Wang, Chuang Wang, Juncheng Hu, Haitao Zhou, Junhua Liu, Jing Zhang, Dong Xu, Qian Yu；2026；ICML 2026；[arXiv:2605.01517v1](https://arxiv.org/abs/2605.01517v1)。
- **主要发现**：将动画建模为持久 SVG DOM 上的 **Sparse State Updates (SSU)**，而非逐帧重写完整 SVG；序列长度压缩超过 9.8×。Identification-First Motion Planning 先把语言绑定到视觉实体，再生成状态更新；用渲染感知 GRPO 和视频感知奖励对齐离散代码与动态视觉，支持路径级非刚性形变；同时发布 SVGAnim-134k。
- **限制**：聚焦 SVG，复杂光栅效果、视频素材、声音和跨镜头叙事不在范围；视频编码器奖励仍可能漏掉 DOM 语义与可维护性；大规模训练成本高。
- **为何相关**：SSU 是 code-generated video 最值得迁移的表示：**静态场景只写一次，时间只记录差量**。这能降低上下文爆炸、身份漂移，并让局部回滚和对象级编辑自然成立。

### C6. MoVer: Motion Verification for Motion Graphics Animations

- **元数据**：Jiaju Ma, Maneesh Agrawala；2025；ACM TOG / SIGGRAPH 2025；[arXiv:2502.13372v2](https://arxiv.org/abs/2502.13372v2)；DOI [10.1145/3731209](https://doi.org/10.1145/3731209)。
- **主要发现**：提出基于一阶逻辑的 motion verification DSL，以方向、幅度、运动类型、相对位置和 Allen 时间区间关系检查 SVG motion graphics。LLM 同时合成动画和验证程序，再将失败谓词反馈给生成器；在 5,600 个合成 prompt 上，正确率由无迭代的 58.8% 提升至最多 50 次修复后的 93.6%。
- **限制**：谓词覆盖的是可离散化的 2D 时空属性，不等于审美、自然运动或叙事质量；50 次迭代代价较高；验证程序本身也可能生成错误。
- **为何相关**：给出比“让 VLM 看视频再点评”更可解释的闭环。仓库可采用 **prompt → temporal contract → code → trace → failed predicates → patch**。

### C7. Training and Agentic Inference Strategies for LLM-based Manim Animation Generation

- **元数据**：Ravidu Suien Rammuni Silva, Ahmad Lotfi, Isibor Kennedy Ihianle, Golnaz Shahtahmassebi, Jordan J. Bird；2026；预印本；[arXiv:2604.18364v2](https://arxiv.org/abs/2604.18364v2)。
- **主要发现**：ManimTrainer 将 SFT 与基于代码、渲染视觉联合奖励的 GRPO 结合；ManimAgent 使用 renderer-in-the-loop（RITL）和 API 文档增强 RITL。对 17 个 30B 以下开源模型、9 种训练/推理组合进行评测；最佳配置报告 94% render success 与 85.7% visual similarity。推理闭环提升视觉结果，却削弱代码指标与视觉指标的相关性。
- **限制**：依赖参考视频相似度，可能惩罚语义正确但视觉实现不同的解；ManimBench 的域和 API 较窄；报告结果需在独立环境复现。
- **为何相关**：清楚区分训练期 API/视觉能力学习与推理期执行修复，并证明**代码指标不能替代渲染指标**。适合用于决定仓库先做 agentic RITL，还是进一步做 SFT/RL。

### C8. TheoremExplainAgent: Towards Video-based Multimodal Explanations for LLM Theorem Understanding

- **元数据**：Max Ku, Thomas Chong, Jonathan Leung, Krish Shah, Alvin Yu, Wenhu Chen；2025；ACL 2025；[arXiv:2502.19400v2](https://arxiv.org/abs/2502.19400v2)；[项目](https://tiger-ai-lab.github.io/TheoremExplainAgent/)。
- **主要发现**：planner 先生成长篇故事与旁白，coding agent 再生成 Manim；可生成 5–10 分钟解释视频。TheoremExplainBench 含 240 个跨数学、物理、化学、计算机科学的主题和五类指标；agentic planning 显著优于无 agent 的约 20 秒输出，并暴露出纯文本评测无法看到的推理错误。
- **限制**：频繁出现文本重叠、尺寸不一致和布局瑕疵；重点是 theorem understanding，不是通用 motion design；长视频“生成成功”不保证教学最优。
- **为何相关**：说明长视频必须使用分层计划与逐段程序，而非一次性长代码；也提示视觉化会把抽象推理错误变成可检测的几何/时序错误。

### C9. MG-Gen: Single Image to Motion Graphics Generation

- **元数据**：Takahiro Shirakawa, Tomoyuki Suzuki, Takuto Narumoto, Daichi Haraguchi；2025；预印本；[arXiv:2504.02361v3](https://arxiv.org/abs/2504.02361v3)；[代码](https://github.com/CyberAgentAILab/MG-GEN)。
- **主要发现**：先用 OCR、检测、分割、修复把单张光栅海报重建成分层 HTML，再由 LMM 为各层生成 JS animation script，最后渲染成视频。相比直接 image-to-video，更能保持文字可读性、对象几何与元素级运动控制。
- **限制**：分层错误会级联到动画；适合平面 motion graphics，不适合自然视频；LMM 运动规划仍依赖输入层级质量。
- **为何相关**：展示了从任意视觉参考进入代码视频的实用途径：**先恢复可编辑图层，再生成时间行为**，比直接让模型重画每帧更稳。

### C10. LogoMotion: Visually-Grounded Code Synthesis for Creating and Editing Animation

- **元数据**：Vivian Liu, Rubaiat Habib Kazi, Li-Yi Wei, Matthew Fisher, Timothy Langlois, Seth Walker, Lydia Chilton；2025；CHI 2025；[arXiv:2405.07065v2](https://arxiv.org/abs/2405.07065v2)；DOI [10.1145/3706598.3714155](https://doi.org/10.1145/3706598.3714155)。
- **主要发现**：视觉分析先识别图层语义并提出 animation concept，再生成动画代码；运行后通过视觉检查做 program repair。时间线、图层面板和快捷控件直接绑定代码位置，实现运动、分组、时间的定点修改。276 个动画对比与 16 人用户研究支持其内容感知与可控编辑价值。
- **限制**：输入是分层 logo/PDF，域较窄；用户研究规模有限；设计质量有主观性。
- **为何相关**：把生成、执行视觉检查和**GUI—代码双向绑定**整合起来。对仓库而言，生成后的参数化编辑能力应被视为一等目标，而非附加功能。

### C11. Keyframer: Empowering Animation Design using Large Language Models

- **元数据**：Tiffany Tseng, Ruijia Cheng, Jeffrey Nichols；2024；CHI 2024；[arXiv:2402.06071v1](https://arxiv.org/abs/2402.06071v1)。
- **主要发现**：输入静态 SVG 与自然语言，LLM 生成 CSS animation；用户可通过连续提示、CSS 编辑器、属性控件和 variants 迭代。专业访谈与 13 人研究显示，用户常采用“分解式提示”：逐个元素、逐步完善动画，而不是一次写完需求。
- **限制**：依赖现有 SVG；主要是 CSS 支持的刚性 transform 与关键帧；不是自动质量优化算法，用户研究也不衡量开放域生成性能。
- **为何相关**：提供重要 HCI 结论：动画需求天然难以一次说清，系统应保存连续编辑上下文、对象引用和参数级控制。

---

## 3. Adjacent：视觉程序生成，可迁移到视频

### A1. Render-in-the-Loop: Vector Graphics Generation via Visual Self-Feedback

- **元数据**：Guotao Liang, Zhangcheng Wang, Juncheng Hu, Haitao Zhou, Ziteng Xue, Jing Zhang, Dong Xu, Qian Yu；2026；预印本；[arXiv:2604.20730v3](https://arxiv.org/abs/2604.20730v3)。
- **主要发现**：把 SVG 生成拆成若干可渲染步骤，将累计画布回送给 MLLM；以细粒度 path decomposition 构造训练轨迹，并用 Render-and-Verify 过滤退化或冗余 primitive。单纯给现成模型看中间图无效，必须训练其理解“局部画布—下一段代码”的映射。
- **限制**：静态 SVG；频繁渲染增加时延；逐 path 顺序未必是最优语义分解。
- **为何相关**：可沿时间轴推广成 **render segment → inspect accumulated video/state → emit next segment**，并说明视觉闭环需要专门数据，而不是在 prompt 中简单附截图。

### A2. CANVAS: Consistency-Aware Navigation via Visual Adaptive Sampling for Long-Context Text-to-SVG Generation

- **元数据**：Yichen Wu, Haoxuan Qu, Yihang Lou, Hossein Rahmani, Jun Liu；2026；预印本；[arXiv:2608.30689v1](https://arxiv.org/abs/2608.30689v1)。
- **主要发现**：在每个完整 stroke 边界，对候选的未来完整 SVG 做有限 rollout；联合模型轨迹概率与渲染质量，并按不确定性、决策影响和 rollout 成本分配预算。无需再训练即可改善长 SVG 的几何、遮挡、布局和整体构图。
- **限制**：静态图；多次 future rollout 成本高；视觉打分器决定搜索偏好。
- **为何相关**：为动画代码提供“**关键时间段/操作级 lookahead**”思路：在不可逆的早期运动决策前，对多个未来轨迹短暂渲染并选择长期质量更好的分支。

### A3. Hierarchical SVG Tokenization: Learning Compact Visual Programs for Scalable Vector Graphics Modeling（HiVG）

- **元数据**：Ximing Xing et al.；2026；预印本；[arXiv:2604.05072v2](https://arxiv.org/abs/2604.05072v2)。
- **主要发现**：将 raw SVG 拆成 atomic tokens，再把 command—parameter 组合压成受几何约束的 segment tokens；配合保留数值顺序的 HMN 初始化与课程学习，序列缩短约 62.7%–63.8%，相似质量下训练 token 约减少 2.7×。
- **限制**：静态 SVG、专用词表；压缩词元可能降低任意细节编辑的透明度；迁移到 JS/Canvas 需重设语法单元。
- **为何相关**：动画程序更长且坐标/关键帧密集，可构造“对象、轨迹段、easing、持续时间、状态更新”层级词元，降低上下文和坐标幻觉。

### A4. VectorGym: A Multi-Task Benchmark for SVG Code Generation, Sketching and Editing

- **元数据**：Joan Rodriguez et al.；2026；预印本；[arXiv:2603.29852v2](https://arxiv.org/abs/2603.29852v2)。
- **主要发现**：统一 Sketch2SVG、复杂 SVG 编辑、Text2SVG、captioning，采用真实 SVG 与专家标注；多任务 GRPO 基线使用渲染奖励，并给出经人类相关性验证的 VLM judge。
- **限制**：没有时间维；judge 仍可能偏向光栅外观而忽略代码结构；任务分布不等于视频设计。
- **为何相关**：其“生成 + 理解 + 多步编辑”联合训练比单一 text-to-video 更适合可编辑代码视频；可扩展为 sketch/keyframe-to-animation、instruction editing 与 animation captioning。

### A5. StarVector: Generating Scalable Vector Graphics Code from Images and Text

- **元数据**：Joan Rodriguez et al.；2024/2025 版本；[arXiv:2312.11556v3](https://arxiv.org/abs/2312.11556v3)。
- **主要发现**：将 SVG 明确视为 code generation，由视觉编码器与 CodeLLM 从图像或文本生成完整 SVG code；支持比纯曲线拟合更丰富的 primitive 与语义结构，并提出 SVG-Bench。
- **限制**：静态输出；长代码与复杂结构仍困难；训练主要优化最终渲染，未建模运动身份。
- **为何相关**：是“视觉输入 → 可执行图形代码”的直接先例，可作为图像/关键帧转视频代码编码器；真正迁移时必须加入时间状态和跨帧对象绑定。

### A6. OmniSVG: A Unified Scalable Vector Graphics Generation Model

- **元数据**：Yiying Yang et al.；2025；NeurIPS 2025；[arXiv:2504.06263](https://arxiv.org/abs/2504.06263)；[项目](https://omnisvg.github.io/)。
- **主要发现**：统一 Text-to-SVG、Image-to-SVG 与角色参考生成，能从简单图标扩展到复杂角色和长 SVG，体现预训练 VLM + 自回归 SVG 程序的可扩展性。
- **限制**：静态 SVG；复杂遮挡和冗余命令仍是问题；不保证动画友好的分组、拓扑或命名。
- **为何相关**：可为视频代码先生成高质量、角色一致的初始 scene graph；但需要额外的 animation-ready 约束，如稳定 ID、语义 group 和可变形路径拓扑。

### A7. DeTikZify: Synthesizing Graphics Programs for Scientific Figures and Sketches with TikZ

- **元数据**：Jonas Belouadi, Simone Paolo Ponzetto, Steffen Eger；2024；NeurIPS 2024 Spotlight；[arXiv:2405.15306](https://arxiv.org/abs/2405.15306)；[代码](https://github.com/potamides/detikzify)。
- **主要发现**：从科学图或手绘草图合成可编译 TikZ 程序，以大规模 TikZ 数据学习视觉—代码映射，并通过编译/渲染选择候选。强调科学图形的结构化、可编辑与语义保真。
- **限制**：静态科学图；TeX 编译慢且错误信息复杂；数据偏论文插图。
- **为何相关**：对讲解视频中的公式图、几何图、流程图非常有价值；可将 TikZ program 当作静态场景模块，再由时间 DSL 调度 reveal、transform 与 camera。

### A8. Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End Engineering

- **元数据**：Chenglei Si, Yanzhe Zhang, Zhengyuan Yang, Ruibo Liu, Diyi Yang 等；2024/2025；预印本；[arXiv:2403.03163v3](https://arxiv.org/abs/2403.03163v3)；484 个真实网页。
- **主要发现**：系统评测截图到 HTML/CSS 的前端代码生成，并引入更贴近视觉布局的度量；真实网页显著暴露模型在细节、空间关系和长代码上的问题。
- **限制**：静态网页，属于普通网页代码生成；不涉及 animation timeline 或视频级时间指标。
- **为何仍收录**：仅作为**场景构建与浏览器执行评测**先例。其价值是首帧/静态 layout grounding、DOM 可编辑性和截图回归，而不是直接提供视频方法。

### A9. Spellburst: A Node-based Interface for Exploratory Creative Coding with Natural Language Prompts

- **元数据**：Tyler Angert, Miroslav Ivan Suzara, Jenny Han, Christopher Lawrence Pondoc, Hariharan Subramonyam；2023；UIST 2023；[arXiv:2308.03921v1](https://arxiv.org/abs/2308.03921v1)；DOI [10.1145/3586183.3606719](https://doi.org/10.1145/3586183.3606719)。
- **主要发现**：面向 p5.js creative coding，以节点图保存代码及视觉结果，支持分支、合并、自然语言大步探索、动态控件和直接代码微调。重点不是一次生成最优图，而是保留创作路径和可组合变体。
- **限制**：HCI 原型与小规模艺术家研究；主要针对生成艺术，不专门评估时间一致性或成片质量。
- **为何相关**：视频创作同样需要非线性探索。可把节点从“静态 sketch”升级为“scene/shot/timeline variant”，用代码合并实现镜头与运动风格组合。

### A10. DeepSVG: A Hierarchical Generative Network for Vector Graphics Animation

- **元数据**：Alexandre Carlier, Martin Danelljan, Alexandre Alahi, Radu Timofte；2020；NeurIPS 2020；[arXiv:2007.11301v3](https://arxiv.org/abs/2007.11301v3)。
- **主要发现**：以层级网络建模 SVG commands 与 paths，支持图标重建、生成、插值和 latent 操作；插值可形成平滑的向量动画。
- **限制**：标题中的 animation 主要来自 latent interpolation，并非自然语言到通用动画代码；图标域窄，缺少显式时间语义和复杂对象行为。
- **为何相关**：说明 path-level 层级和固定拓扑插值有助于形变动画；可作为代码生成器之外的参数化补间器，但不应误列为直接视频代码生成。

### A11. Breathing Life Into Sketches Using Text-to-Video Priors（LiveSketch）

- **元数据**：Rin Gal et al.；2023/2024；[arXiv:2311.13608](https://arxiv.org/abs/2311.13608)；[项目](https://livesketch.github.io/)。
- **主要发现**：借助预训练 text-to-video diffusion 的运动先验和 score distillation，直接优化向量 stroke 的时间变化，得到可编辑短动画，不需专门动画训练集。
- **限制**：优化慢；稀疏 stroke 易出现拓扑不稳定、分叉/折叠；对文字、闭合形状、遮挡与复杂专业 SVG 不稳；输出重点是参数优化而非离散代码合成。
- **为何相关**：提供“视频模型作为 motion prior、向量程序作为最终表示”的桥梁，可用于生成候选轨迹或奖励；但工程上应避免把昂贵 SDS 放入每次交互闭环。

### A12. LiveSVG: Zero-Shot SVG Animation via Video Generation

- **元数据**：Matan Levy, Ran Margolin, Bar Cavia, Dvir Samuel, Yael Pritch, Shmuel Peleg, Alex Rav-Acha, Ariel Shamir, Dani Lischinski；2026；预印本；[arXiv:2605.30174v1](https://arxiv.org/abs/2605.30174v1)；[项目](https://levymsn.github.io/LiveSVG/)。
- **主要发现**：先用 image-to-video 生成可预览目标视频，再用可微渲染把原 SVG 拟合到该固定序列；以 group homography 表示粗运动、Bézier control-point offset 表示局部形变，并用临时重着色解决路径对应歧义。
- **限制**：生成的不是由 LLM 直接编写的动画程序；依赖目标视频质量与昂贵拟合；复杂遮挡和拓扑变化仍困难。
- **为何相关**：适合成为混合系统的“运动提案器/蒸馏器”：先由视频模型提出自然运动，再压回可编辑向量状态；其 coarse-to-fine 运动参数化也可直接移植到动画 DSL。

---

## 4. Background：基础方法，仅保留直接可复用机制

### B1. Differentiable Vector Graphics Rasterization for Editing and Learning（DiffVG）

- **元数据**：Tzu-Mao Li, Michal Lukáč, Michaël Gharbi, Jonathan Ragan-Kelley；2020；ACM TOG / SIGGRAPH Asia 2020；[论文](https://people.csail.mit.edu/tzumao/diffvg/diffvg.pdf)；DOI [10.1145/3414685.3417871](https://doi.org/10.1145/3414685.3417871)。
- **主要发现**：使 Bézier path、圆、椭圆、矩形等 SVG primitive 的光栅化可微，从像素损失反传到几何和颜色参数；成为大量 text/image-to-SVG 与向量动画优化方法的基础。
- **限制**：本身不做语言理解、程序结构搜索或时间建模；局部梯度难以处理离散拓扑、对象创建/删除与长程语义。
- **为何相关**：可作为代码视频中连续参数（坐标、颜色、路径、关键帧）的局部优化器，但应与离散程序合成、对象级约束和执行验证组合。

### B2. Learning to Infer Graphics Programs from Hand-Drawn Images

- **元数据**：Kevin Ellis et al.；2017/2018；NeurIPS；[arXiv:1707.09627v5](https://arxiv.org/abs/1707.09627v5)。
- **主要发现**：以神经模型从带噪手绘输入提出图形程序，再用程序合成/搜索纠正感知误差；将感知、DSL 与符号约束结合，而不是直接回归像素。
- **限制**：小型 2D drawing DSL、简单几何、合成数据为主；远离现代 Web/视频工具链。
- **为何相关**：奠定“神经 proposal + 符号 search/verification”的可靠范式，可迁移为 LLM 提议动画结构、执行器与约束求解器负责校正。

### B3. SPIRAL: Synthesizing Programs for Images using Reinforced Adversarial Learning

- **元数据**：Yaroslav Ganin et al.；2018；ICML；[arXiv:1804.01118](https://arxiv.org/abs/1804.01118)。
- **主要发现**：agent 顺序输出图形程序片段，每一步经 renderer 改变画布，并以对抗/强化信号学习产生目标图像；把图像生成表述为与不可微图形引擎交互的序列决策。
- **限制**：静态图、低层绘制动作、训练不稳定；缺乏现代语言条件、对象结构与编辑接口。
- **为何相关**：提供 renderer-as-environment 的基础视角；现代版本可把动作提升为 scene graph/timeline 操作，用可验证奖励替代单一对抗分数。

### B4. Neurosymbolic Models for Computer Graphics

- **元数据**：Paul Guerrero et al.；2023；综述；[arXiv:2304.10320](https://arxiv.org/abs/2304.10320)。
- **主要发现**：系统化总结“用户意图 + 图形 DSL → 可执行视觉程序”的神经符号路线，包括结构归纳、程序搜索、可微近似和神经后处理。
- **限制**：综述性质；大量案例聚焦静态 2D/3D/CAD，不提供现成视频系统。
- **为何相关**：用于设计仓库的技术版图：离散结构由程序合成负责，连续参数由优化负责，渲染器提供反馈，神经模型负责 proposal 与语义评分。

---

## 5. 横向方法对照

| 方法族 | 代表工作 | 程序表示 | 时间建模 | 反馈/验证 | 可编辑性 | 主要风险 |
|---|---|---|---|---|---|---|
| 通用 Web 视频代码 | Code2Video-Compass, Reels-RSI | Remotion + HTML/CSS/SVG/Canvas/Three.js | 帧/场景/timeline | 执行、静态规则、VLM、主客观指标 | 高 | 长代码、跨场景状态、评审偏差 |
| Manim 教育视频 | Code2Video, TheoremExplainAgent, ManimAgent | Python scene program | scene/animation calls | 编译、RITL、视觉锚点、教学指标 | 高 | API 幻觉、布局、长片一致性 |
| SVG/CSS 动画代码 | Keyframer, LogoMotion, MoVer, VAnim | CSS/SMIL/JS/DOM state updates | keyframe、interval、SSU | visual repair、逻辑谓词、RL | 很高 | 刚性运动偏置、路径形变与身份漂移 |
| 光栅图到 motion graphics | MG-Gen | 分层 HTML + JS | layer-wise script | 人评/VLM/输入保真 | 高 | 分层误差级联 |
| 视频到 Web 代码 | Animation2Code | 自包含 HTML/CSS/JS | 从视频反演轨迹与节奏 | appearance + temporal metrics | 高 | 外观好但运动错 |
| 视频先验到向量动画 | LiveSketch, LiveSVG | 连续向量参数/状态 | 视频先验或目标序列 | 可微渲染 | 中高 | 慢、拓扑不稳、不是直接代码生成 |
| 静态视觉程序 | Render-in-the-Loop, CANVAS, StarVector, OmniSVG | SVG/TikZ/HTML | 无 | 中间渲染、rollout、编译 | 高 | 静态指标无法代表时间质量 |

---

## 6. 对 awesome-code-generated-video 的直接研究建议

### 6.1 建议的统一中间表示

采用 **persistent scene graph + sparse temporal updates**，而不是逐帧完整 HTML：

```text
Project
├── assets / fonts / audio
├── scenes[]
│   ├── static DOM or scene graph
│   ├── semantic object IDs and groups
│   ├── timeline tracks[]
│   │   ├── target object
│   │   ├── property / path / effect
│   │   ├── keyframes or procedural function
│   │   ├── easing / duration / synchronization
│   │   └── temporal pre/post-conditions
│   └── camera / transition
├── narration and word-level timing
└── executable checks
```

关键点来自 VAnim（SSU）、MoVer（时序谓词）、LogoMotion（代码连接控件）、Reels-RSI（可执行规则）和 MG-Gen（层级对象）。底层可编译到 Remotion + HTML/SVG/Canvas/Three.js；不要让模型在多个渲染后端之间直接自由拼接无约束代码。

### 6.2 建议的生成闭环

1. **Planner**：把需求拆成叙事 beat、scene、对象、音频和时间约束。
2. **Asset/Scene Builder**：从文本、图片或图表生成稳定 ID 的可编辑场景；必要时使用 SVG/TikZ 模块。
3. **Motion Planner**：先对象 grounding，再生成轨迹、同步关系和 sparse updates。
4. **Compiler/Renderer**：固定依赖与浏览器版本，确定性渲染关键帧、低帧率预览和最终视频。
5. **Verifier**：
   - 代码：编译、异常、依赖、资源、确定性；
   - 空间：越界、重叠、遮挡、文字可读性、anchor；
   - 时间：开始/结束、并发、顺序、轨迹、循环、速度连续性；
   - 视觉：appearance、motion、aesthetic；
   - 任务：教学/品牌/信息传达 checklist。
6. **Localized Repair**：失败报告必须落到 scene/object/track/time interval/code span，禁止默认整片重写。
7. **Memory**：把稳定缺陷编译成带 bad/good 测例的规则，并回扫历史作品。

### 6.3 最小评测矩阵

| 层级 | 必测指标 | 不应使用的单一替代指标 |
|---|---|---|
| Operational | build/render success、超时、token/时延、确定性 | “代码看起来正确” |
| Spatial | 边界、重叠、锚点、文字可读性、对象身份 | 单帧 CLIP |
| Temporal | 轨迹距离、速度/加速度、相位、顺序、并发、循环周期 | 帧平均相似度 |
| Semantic | prompt checklist、对象—动作绑定、跨 scene 一致性 | 全局 VLM 总分 |
| Editability | 稳定 ID、局部修改影响范围、结构复杂度、复用率 | 文件是否为代码 |
| Outcome | 教学增益、信息回忆、品牌约束或用户任务成功 | 纯审美偏好 |

### 6.4 推荐的首批 benchmark 切片

- **T2V**：文字描述 → 5–15 秒完整 motion graphic。
- **I2V**：海报/logo/首帧 → 分层可编辑动画。
- **V2V**：参考短片 → Web animation code，分别评外观与时间。
- **Edit**：在不改变其余 scene 的条件下改某对象轨迹、颜色、节奏或字幕。
- **Long-form**：多 scene 的 1–5 分钟 explainer，检查 narration—visual alignment 与跨场景一致性。
- **Adversarial**：相同首尾帧但不同运动、错相位循环、对象身份交换、文字短暂越界、遮挡次序错误，用于防止静态指标“作弊”。

### 6.5 明确不建议

- 不把普通 screenshot-to-HTML 当作视频能力；它最多覆盖场景搭建。
- 不只检查执行成功；Animation2Code 已显示执行正确可与时间错误并存。
- 不只用逐帧 CLIP/VLM 平均分；应加入对象轨迹、时序关系和事件级 checklist。
- 不让 agent 每轮重写整片；应以 persistent IDs、SSU 和局部 patch 为默认。
- 不把视频扩散模型与代码路线对立起来；LiveSVG 表明视频模型可提供 motion proposal，但最终应蒸馏回可编辑结构。
- 不把“有 SVG/HTML 输出”自动等同于可编辑；需要稳定分组、语义 ID、低耦合 timeline 和可定位代码映射。

---

## 7. 纳入与排除说明

- **纳入静态 SVG/TikZ 工作的条件**：只有当它明确提供长视觉程序压缩、中间渲染反馈、可执行验证、结构化编辑或 animation-ready 表示时才纳入。
- **Design2Code 的例外**：它是普通静态网页代码生成，故仅因浏览器执行环境、真实布局评测和首帧 scene reconstruction 的具体迁移价值而保留，且明确放在 adjacent。
- **未纳入**：通用代码 LLM、普通 text-to-image/video、纯网页 UI 生成、只做视频像素生成或压缩、与可执行视觉程序无关的图表/布局论文。
- **“Animation” 标题不自动进入 Core**：DeepSVG 的 animation 主要是 latent interpolation；LiveSketch/LiveSVG 主要是连续优化，因此均列 adjacent，而不是“直接生成视频代码”。

## 8. 研究优先级

1. **P0：复现与统一评测**——优先对齐 Code2Video-Compass、Animation2Code、MoVer 的任务和指标。
2. **P0：表示层**——实现 scene graph + stable IDs + SSU + timeline contract。
3. **P1：闭环修复**——浏览器/渲染器反馈必须能定位到对象与时间区间。
4. **P1：编辑与审计**——加入 code-connected controls、diff、规则测试和历史回扫。
5. **P2：训练**——有高质量执行轨迹后，再做 SFT/GRPO；奖励必须联合执行、视觉、时间与结构质量。
6. **P2：混合 motion prior**——用视频模型生成候选运动，再压回向量/程序轨迹，而非直接作为不可编辑终稿。
