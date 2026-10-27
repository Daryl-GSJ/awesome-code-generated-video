# 模型生成可执行代码/程序并渲染为视频：核心论文与系统

> 检索截止：**2026-10-27 14:29 CST**  
> 范围：模型（LLM/MLLM/VLM）生成可执行代码、动画程序、结构化可执行表示或仿真程序，并由确定性渲染器/图形引擎生成视频或动画。普通像素空间 text-to-video、仅以代码为条件但不生成代码的视频模型，不进入核心列表。

## 1. 结论摘要

这一方向已从 2024 年的 Blender/网页动画原型，发展为三条相对清晰的技术线：

1. **教育解释视频（以 Manim 为主）**：TheoremExplainAgent、Manimator、Code2Video、PhysicsSolutionAgent、LLM2Manim、ANVIL、LASEV、ManimAgent、ALGOGEN 等；核心问题是长程规划、API 正确性、布局、教学正确性和视觉反馈。
2. **通用程序化动画/视频**：Kubrick（Blender）、LogoMotion（JavaScript 动画）、MG-Gen（HTML+JS）、DATAREEL（HTML+D3.js）、LottieGPT/InternSVG（结构化矢量动画）、Reels-RSI（HTML/SVG/Canvas/Three.js）、Code2Video-Compass（Remotion 通用栈）。
3. **可验证、逆向与混合范式**：MoVer、SGA、ManiBench 提供验证；Animation2Code、PhySimCode、4DCodeBench 从视频反推可执行程序；VideoCoCo 用 Blender 程序先渲染时空草稿，再经生成式视频编辑器提升写实度。

共同瓶颈不是“能否写出语法正确代码”，而是：**可执行性与视觉/时间语义正确性脱钩、长视频布局错误、精确动态恢复困难、VLM 裁判偏差，以及缺少与真实学习效果或专业制作质量一致的评价**。

## 2. 纳入边界与相关性分级

- **A（直接核心）**：模型输出可执行代码/程序/结构化动画程序，且执行或渲染该输出直接产生最终视频/动画。
- **B（核心支撑）**：代码渲染链是任务中心，但论文主要贡献是 benchmark、verifier、逆向重建，或最终视频还经过像素生成模型。
- **X（排除）**：普通 text-to-video；代码只作为输入条件；只生成脚本/分镜而不生成可执行视觉程序；只生成静态图/3D 场景且视频不是主要输出。

“动画”在本报告中视为视频的程序化母表示：只要论文明确执行程序并得到时间序列画面、MP4/GIF 或可确定性录制的动画，即纳入；纯静态 SVG/Blender 场景则不纳入 A。

## 3. 直接核心论文与系统（Tier A）

### A1. Kubrick: Multimodal Agent Collaborations for Synthetic Video Generation

- **authors**：Liu He; Yizhi Song; Hejun Huang; Daniel Aliaga; Xin Zhou
- **year / venue/status**：2024 arXiv；后见于 CVPR AI for Content Creation Workshop（公开索引为 2025 workshop）
- **arXiv/DOI**：[arXiv:2408.10453](https://arxiv.org/abs/2408.10453)；DOI 未确认
- **code/project**：公开全文未给出可核验官方代码仓；索引标注 code unavailable
- **task**：自然语言到 2D/3D 合成视频。
- **representation**：Python Blender 脚本、可复用函数库、分阶段电影制作流程。
- **method**：Director 分解镜头/制作子过程，Programmer 组合 Blender API 与函数库，Reviewer 根据中间截图和视频反馈迭代代码；RAG 注入 Blender 与电影制作知识。
- **feedback/verifier**：VLM Reviewer 检查提示遵循、物理、光照、相机和时序；代码库随迭代更新。
- **dataset**：作者构建的文本描述/视频测试集；全文未给出可复用标准 benchmark 名称。
- **evaluation**：5 类视频质量与指令遵循指标，加用户研究；对比 Pika、Gen-2、Dream Machine。
- **main finding**：多智能体写 Blender 程序并视觉闭环，可在受控合成视频上优于当时商业像素生成基线。
- **limitations**：依赖资产/函数库与 Blender 知识；合成感明显；论文数据规模、代码可得性和跨开放域泛化有限。
- **relevance tier**：A（早期通用 text→Blender-code→video 代表）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2408.10453v1)、[NSF 公开索引](https://par.nsf.gov/biblio/10698644-kubrick-multimodal-agent-collaborations-synthetic-video-generation)

### A2. From Data to Story: Towards Automatic Animated Data Video Creation with LLM-based Multi-Agent Systems（Data Director）

- **authors**：Leixian Shen; Haotian Li; Yun Wang; Huamin Qu
- **year / venue/status**：2024，IEEE Visualization 作者稿（最终 DOI 在所读版本中仍为占位符）
- **arXiv/DOI**：[arXiv:2408.03876](https://arxiv.org/abs/2408.03876)；DOI 无法确认
- **code/project**：未确认公开代码
- **task**：从原始表格数据自动生成带旁白的动画数据视频。
- **representation**：Vega-Lite 可执行可视化规范、SVG、动画设计参数、时间轴与音频。
- **method**：Data Analyst 发现洞察、生成可视化与旁白；Designer 规划动画/标注；控制器调用可视化渲染、TTS 和视频合成工具。
- **feedback/verifier**：以多阶段提示和工作流迭代为主，没有强执行验证器。
- **dataset**：案例研究使用真实股票价格数据；未建立大规模 benchmark。
- **evaluation**：系统案例与设计经验分析，而非全面模型基准。
- **main finding**：证明 LLM 多智能体能够编排规范、渲染器与音视频工具完成端到端数据视频。
- **limitations**：实证规模小；模型更多生成规范/决策而非自由形式动画源码；全局优化与人工介入仍不足。
- **relevance tier**：A-（模型生成可执行视觉规范并渲染，但“自由代码生成”较弱）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2408.03876v1)

### A3. LogoMotion: Visually-Grounded Code Synthesis for Creating and Editing Animation

- **authors**：Vivian Liu; Rubaiat Habib Kazi; Li-Yi Wei; Matthew Fisher; Timothy Langlois; Seth Walker; Lydia Chilton
- **year / venue/status**：2025，CHI 2025
- **arXiv/DOI**：[arXiv:2405.07065](https://arxiv.org/abs/2405.07065)；[10.1145/3706598.3714155](https://doi.org/10.1145/3706598.3714155)
- **code/project**：论文未给出可核验公开实现仓
- **task**：从分层 logo 文档生成内容感知动画，并允许非专家编辑。
- **representation**：JavaScript 动画代码，连接图层、动作、分组和时间参数。
- **method**：视觉分析→设计概念→代码合成；运行后以截图/渲染结果做 visually-grounded program repair；GUI 控件定点修改代码。
- **feedback/verifier**：视觉检查和最多四轮程序修复；人工可通过 code-connected widgets 介入。
- **dataset**：276 个生成动画；16 人用户研究。
- **evaluation**：内容感知、质量、序列等人工评分；与行业工具和 prompt-only 编辑基线比较。
- **main finding**：内容感知优于行业模板工具；检测到的错误中 96% 可在四轮内修复；代码连接控件改善控制与迭代。
- **limitations**：局限于分层 logo；依赖输入图层质量；动作复杂性和通用视频叙事有限。
- **relevance tier**：A（2D 动画代码生成与视觉修复的关键前驱）。
- **证据来源**：[paper-tool 全文对应 arXiv v2](https://arxiv.org/html/2405.07065v2)、[ACM DOI](https://doi.org/10.1145/3706598.3714155)

### A4. TheoremExplainAgent: Towards Video-based Multimodal Explanations for LLM Theorem Understanding

- **authors**：Max Ku; Thomas Chong; Jonathan Leung; Krish Shah; Alvin Yu; Wenhu Chen
- **year / venue/status**：2025，arXiv 预印本（最终正式 venue 未确认）
- **arXiv/DOI**：[arXiv:2502.19400](https://arxiv.org/abs/2502.19400)；DOI 未确认
- **code/project**：[项目页](https://tiger-ai-lab.github.io/TheoremExplainAgent/)
- **task**：为数学、物理、化学、计算机科学定理生成 5–10 分钟解释视频。
- **representation**：故事计划、旁白、分场景 Python/Manim 动画脚本。
- **method**：Planner 生成长程讲解结构，Coding Agent 逐场景写 Manim，最后拼接视频与旁白。
- **feedback/verifier**：代码执行/渲染成功检查；评估阶段以自动多维指标和人工专家评审为主。
- **dataset**：TheoremExplainBench，240 个定理、4 个 STEM 学科。
- **evaluation**：Accuracy & Depth、Visual Relevance、Logical Flow、Element Layout、Visual Consistency；成功率和整体几何均值。
- **main finding**：agentic planning 将直接生成约 20 秒的能力扩展到最长约 10 分钟；o3-mini 成功率 93.8%，总分 0.77。
- **limitations**：布局是最弱项；长视频会累积文字重叠、尺寸和对齐错误；视觉解释还会暴露文本答案未显现的推理错误。
- **relevance tier**：A（长篇 Manim 教育视频与 benchmark 奠基工作）。
- **证据来源**：[paper-tool 全文对应 arXiv v2](https://arxiv.org/html/2502.19400v2)、[项目页](https://tiger-ai-lab.github.io/TheoremExplainAgent/)

### A5. MG-Gen: Single Image to Motion Graphics Generation

- **authors**：Takahiro Shirakawa; Tomoyuki Suzuki; Takuto Narumoto; Daichi Haraguchi
- **year / venue/status**：2025 arXiv；存在 IEEE 记录，具体会议/DOI 在可访问证据中未确认
- **arXiv/DOI**：[arXiv:2504.02361](https://arxiv.org/abs/2504.02361)
- **code/project**：[GitHub](https://github.com/CyberAgentAILab/MG-GEN)
- **task**：单张栅格设计图（可附动作指令）到 motion graphics 视频。
- **representation**：分层 HTML + LMM 生成的可执行 JavaScript 动画脚本。
- **method**：OCR、检测、分割、修复将图像拆层并重建 HTML；LMM 为图层生成动作程序，浏览器执行并录制视频。
- **feedback/verifier**：无强迭代验证器；使用生成结果的人评和 GPT 评测。
- **dataset**：Crello 用于对象检测训练；自建 motion-graphics 测试样本。
- **evaluation**：动态文字、可读性、输入忠实度；与通用 image-to-video 基线比较。
- **main finding**：代码化分层动画比像素 I2V 更能保持文字可读性与几何稳定性。
- **limitations**：分层/修复错误会向后传播；主要针对平面设计图，非开放世界视频。
- **relevance tier**：A（image→HTML/JS program→video）。
- **证据来源**：[paper-tool 全文对应 arXiv v3](https://arxiv.org/html/2504.02361v3)、[代码](https://github.com/CyberAgentAILab/MG-GEN)

### A6. Manimator: Transforming Research Papers into Visual Explanations

- **authors**：Samarth P; Vyoman Jain; Shiva Golugula; Motamarri Sai Sathvik
- **year / venue/status**：2025；ICML 2025 页面可检索，但具体主会/ workshop track 无法确认
- **arXiv/DOI**：[arXiv:2507.14306](https://arxiv.org/abs/2507.14306)；DOI 未确认
- **code/project**：[GitHub](https://github.com/HyperCluster-Tech/manimator)、[Web](https://manimator.hypercluster.tech/)
- **task**：自然语言、PDF 或 arXiv 论文到解释动画。
- **representation**：结构化 Markdown scene description → 可执行 Python/Manim Scene → MP4。
- **method**：多模态/长上下文模型提取概念和视觉计划；代码模型（主要配置 DeepSeek-V3）生成 Manim；直接执行渲染。
- **feedback/verifier**：生成阶段没有视频反馈闭环；靠详细角色提示、few-shot 和模型选择提高成功率。
- **dataset**：主要使用 TheoremExplainBench；另有工程学生志愿者人工评测。
- **evaluation**：TEB 五维指标；自动总分 0.845，人工归一化总分 0.738。
- **main finding**：简单两阶段规划+代码可达到强基线，元素布局 0.853，优于其引用的 Claude/o3-mini 基线。
- **limitations**：高度依赖底模；复杂细节和教学节奏不稳定；论文明确承认没有基于用户/视频反馈的迭代优化。
- **relevance tier**：A（用户点名，论文/自然语言到 Manim 的代表系统）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2507.14306v1)、[代码](https://github.com/HyperCluster-Tech/manimator)

### A7. Code2Video: A Code-centric Paradigm for Educational Video Generation

- **authors**：Yanzhe Chen; Kevin Qinghong Lin; Mike Zheng Shou
- **year / venue/status**：2026，ICML 2026（PMLR 306）；arXiv 初稿 2025
- **arXiv/DOI**：[arXiv:2510.01174](https://arxiv.org/abs/2510.01174)；PMLR 通常无 DOI
- **code/project**：[GitHub](https://github.com/showlab/Code2Video)、[项目页](https://showlab.github.io/Code2Video/)、[PMLR](https://proceedings.mlr.press/v306/chen26bx.html)
- **task**：从学习主题生成专业、长篇、学科特定教育视频。
- **representation**：storyboard/参考资产 → 多场景可执行 Python/Manim 代码 → 视频。
- **method**：Planner 建立时间连贯讲稿与素材；Coder 并行生成代码并做 scope-guided auto-fix；Critic 用 visual-anchor prompts 修正空间布局。
- **feedback/verifier**：编译/运行日志驱动代码修复；VLM 基于渲染锚帧批评布局；TeachQuiz 检验知识传递。
- **dataset**：MMMC，专业 Manim 教程，13 个学科域；代码/数据公开。
- **evaluation**：VLM aesthetics、逻辑/准确性、生成时间/Token、TeachQuiz、人工研究；与人工、像素 T2V、直接 CodeLLM 比较。
- **main finding**：相对直接代码生成整体提升约 40%，生成视频在部分评价上接近或超过人工教程；直接代码范式本身较像素生成更适合精确教育内容。
- **limitations**：依赖 Manim 与教育域；VLM critic 对细粒度几何冲突仍不稳；TeachQuiz 的“unlearning+恢复”协议和 VLM judge 有效性仍需外部复验。
- **relevance tier**：A（用户点名，当前教育 code-to-video 主干工作）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2510.01174v1)、[PMLR 正式版](https://proceedings.mlr.press/v306/chen26bx.html)、[代码](https://github.com/showlab/Code2Video)

### A8. LLM2Manim: Pedagogy-Aware AI Generation of STEM Animations

- **authors**：Aastha Joshi; Hongyi Ke; Meet Gajjar; Aaron Christian; Qi Wang; Jun Chen
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2604.05266](https://arxiv.org/abs/2604.05266)；DOI 未确认
- **code/project**：未发现可核验公开仓库
- **task**：教师自然语言 brief 到带旁白的数学/物理 Manim 动画。
- **representation**：教学分段计划、旁白、符号台账、Manim Python 代码。
- **method**：CTML/分段/信号提示/双编码原则约束规划；符号 ledger 保持记号一致；只重生成错误片段；最终专家审核。
- **feedback/verifier**：代码自修复、局部重生成、human-in-the-loop 专家门控。
- **dataset**：无公开生成 benchmark；100 名本科生 within-subject A/B 学习实验。
- **evaluation**：后测、学习增益、参与度、认知负荷、完成时间与偏好。
- **main finding**：动画组后测 83% vs 78%（p<.001），学习增益 d=0.67、参与度 d=0.94、认知负荷改善 d=0.41。
- **limitations**：半自动而非全自动；主题和学生样本范围有限；必须专家审核，代码/解释仍可能错误。
- **relevance tier**：A（用户点名；突出“教学设计+人工门控”）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2604.05266v1)

### A9. PhysicsSolutionAgent: Towards Multimodal Explanations for Numerical Physics Problem Solving

- **authors**：Aditya Thole; Anmol Agrawal; Arnav Ramamoorthy; Dhruv Kumar
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2601.13453](https://arxiv.org/abs/2601.13453)；DOI 未确认
- **code/project**：[GitHub](https://github.com/f20220374/PhysicsSolutionAgent)
- **task**：数值/概念物理题到最长约 6 分钟解释视频。
- **representation**：Planner 输出故事板/解题流程；Coder 输出 Manim Python；旁白与视频组合。
- **method**：GPT-5-mini 规划与编码，Manim 文档 RAG，多次执行修复，抽帧给 VLM 反馈。
- **feedback/verifier**：运行日志 + screenshot-driven VLM feedback；15 个自动参数评分。
- **dataset**：32 个生成视频，覆盖数值题和理论题及不同难度。
- **evaluation**：完成率、15 项自动评价、加权 5 分制分数、定性与人工检查。
- **main finding**：100% 视频完成率，自动均分约 3.8/5；数值和概念任务总体自动分接近。
- **limitations**：仅 32 个样本；仍有冗余、布局和物理解释问题；VLM 会错误理解渲染帧并给出误导反馈。
- **relevance tier**：A（用户点名；执行与视觉反馈闭环清晰）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2601.13453v1)、[代码](https://github.com/f20220374/PhysicsSolutionAgent)

### A10. Beyond End-to-End Video Models: An LLM-Based Multi-Agent System for Educational Video Generation（LASEV）

- **authors**：Lingyong Yan; Jiulong Wu; Dong Xie; Weixian Shi; Deguo Xia; Jizhou Huang
- **year / venue/status**：2026，KDD 2026
- **arXiv/DOI**：[arXiv:2602.11790](https://arxiv.org/abs/2602.11790)；[10.1145/3770855.3818323](https://doi.org/10.1145/3770855.3818323)
- **code/project**：[项目页](https://robitsg.github.io/LASEV/)；未确认完整开源代码
- **task**：K–12 教育题到大规模量产的讲解视频。
- **representation**：结构化可执行视频脚本、可执行可视化代码、旁白、模板化装配规则。
- **method**：Orchestrator 协调 Solution、Illustration、Narration agents；共享生产状态、质量门和模板编译器确定性装配。
- **feedback/verifier**：语义 critic、规则约束、工具/编译检查、迭代纠错。
- **dataset**：论文报告生产部署数据与评测集；公开 benchmark 细节/许可未完全确认。
- **evaluation**：逻辑/视觉/音画一致性、接受率、吞吐、成本；报告部署吞吐超过每日一百万条、成本降低 95% 以上。
- **main finding**：受约束的可执行脚本与模板装配可实现工业规模教育视频生产。
- **limitations**：强依赖模板与企业基础设施；部署指标难由公开材料独立复现；开放域艺术表现力有限。
- **relevance tier**：A（工业化代码渲染教育视频）。
- **证据来源**：[paper-tool 全文对应 arXiv v2](https://arxiv.org/html/2602.11790v2)、[ACM DOI](https://doi.org/10.1145/3770855.3818323)、[项目页](https://robitsg.github.io/LASEV/)

### A11. DATAREEL: Automated Data-Driven Video Story Generation with Animations

- **authors**：Ridwan Mahbub; Syem Aziz; Mahir Ahmed; Shadikur Rahman; Mizanur Rahman; Shafiq Joty; Enamul Hoque
- **year / venue/status**：2026，预印本、under review
- **arXiv/DOI**：[arXiv:2604.25220](https://arxiv.org/abs/2604.25220)；DOI 未确认
- **code/project**：[GitHub](https://github.com/vis-nlp/DataReel)
- **task**：表格数据+分析意图+目标时长到带字幕/旁白语义的短数据视频。
- **representation**：结构化动画计划 → 可执行 HTML+D3.js 动画代码 → 浏览器视频。
- **method**：Planner、Plan Critic、Coder、Video Critic；Coder 将批准的计划编译为 D3.js，视频 critic 针对时序、旁白—动画对齐和视觉质量回传修复建议。
- **feedback/verifier**：计划级 critic 和渲染视频级 VLM critic；多轮重生成。
- **dataset**：DATAREEL，328 个真实数据 reels，配表格、图表和旁白转录。
- **evaluation**：自动/VLM 与人工评价；比较 direct prompting 和 multi-agent，多模型实验。
- **main finding**：多智能体优于直接提示，但最强模型仍经常无法协调动画、强调重点、字幕和时间轴。
- **limitations**：真实视频反推的表格/标注可能有噪声；评价仍依赖 VLM；主要局限于图表叙事。
- **relevance tier**：A（数据叙事的 code→render→video 标准化 benchmark）。
- **证据来源**：[paper-tool 全文](https://arxiv.org/html/2604.25220v1)、[代码](https://github.com/vis-nlp/DataReel)

### A12. Training and Agentic Inference Strategies for LLM-based Manim Animation Generation（ManimTrainer / ManimAgent）

- **authors**：Ravidu Suien Rammuni Silva; Ahmad Lotfi; Isibor Kennedy Ihianle; Golnaz Shahtahmassebi; Jordan J. Bird
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2604.18364](https://arxiv.org/abs/2604.18364)；DOI 未确认
- **code/project**：[GitHub](https://github.com/SuienS/manim-trainer)
- **task**：系统研究 text→Manim code→video 的训练策略与推理策略组合。
- **representation**：Manim Python 源码及其渲染视频。
- **method**：SFT 建立 API/语法能力；GRPO 用代码+视觉联合 reward；推理时 Renderer-in-the-loop（RITL）及文档增强 RITL-DOC。
- **feedback/verifier**：编译/渲染错误、API 文档检索、CodeBLEU/CodeBERT 与 SSIM/CLIP 等联合信号。
- **dataset**：ManimBench（论文使用的 paired description/code/video 数据；与下文 ManiBench 不是同一个资源）。
- **evaluation**：17 个开源 30B 以下模型，9 种训练×推理组合；Render Success Rate、Visual Similarity 及代码指标。
- **main finding**：Qwen3-Coder-30B + GRPO + RITL-DOC 达 94% RSR、85.7% VS；SFT 更改善代码，GRPO 更改善视觉，推理闭环与训练互补。
- **limitations**：主要是参考视频相似度而非教学效果；ManimBench 的代表性、视觉指标偏差和高推理成本仍是问题。
- **relevance tier**：A（目前最直接的“训练+agentic inference”系统研究）。
- **证据来源**：[paper-tool 全文对应 arXiv v2](https://arxiv.org/html/2604.18364v2)、[代码](https://github.com/SuienS/manim-trainer)

### A13. ANVIL: Analogies and Videos for Lecturers

- **authors**：Yuri Noviello; Anastasiia Birillo; Gosia Migut
- **year / venue/status**：2026；Springer 章节已上线，具体会议名未从可访问证据确认
- **arXiv/DOI**：[arXiv:2605.16295](https://arxiv.org/abs/2605.16295)；[10.1007/978-3-032-29744-0_23](https://doi.org/10.1007/978-3-032-29744-0_23)
- **code/project**：[GitHub](https://github.com/yurinoviello/AI_Metaphors)、[Web](https://anvil.labs.jb.gg/)
- **task**：计算机科学概念定义到类比式教学动画。
- **representation**：文本类比 → 结构化视觉 screenplay → Python/Manim 代码。
- **method**：分层生成；静态分析与自动 repair 提升代码鲁棒性；允许教师在类比层先审核。
- **feedback/verifier**：Pylint/执行修复；LLM 类比 evaluator；screenplay-to-video fidelity proxy；教师评审。
- **dataset**：系统生成样本；11 名 CS/SE 教师 rubric 评测，9 名教师焦点组。
- **evaluation**：类比质量、动画充分性、screenplay 忠实度、采纳需求和风险。
- **main finding**：经常能生成“足够可用”的材料，教师总体认可价值，但要求可编辑、可审核与风险护栏。
- **limitations**：自动 proxy 不能替代教学正确性；错误类比会系统性传播；用户研究规模小。
- **relevance tier**：A（中间表示与教师审核设计有代表性）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2605.16295v1)、[Springer DOI](https://doi.org/10.1007/978-3-032-29744-0_23)

### A14. ALGOGEN: Tool-Generated Verifiable Traces for Reliable Algorithm Visualization

- **authors**：Kunpeng Liao; Yuexiao Ma; Yisheng Lin; Hualin Zeng; Xiawu Zheng; Rongrong Ji
- **year / venue/status**：2026，Findings of ACL 2026
- **arXiv/DOI**：[arXiv:2605.12159](https://arxiv.org/abs/2605.12159)；DOI 未确认
- **code/project**：[项目/代码页](https://algenlab.github.io/algogen/)、[ACL Anthology](https://aclanthology.org/2026.findings-acl.156/)
- **task**：从算法题生成可靠、可验证的算法可视化视频。
- **representation**：LLM 生成 Python tracker → VTA-JSON 5.0 执行轨迹；另生成 RSL 风格规范；确定性编译到 Manim/TikZ/Three.js。
- **method**：把“算法执行”与“布局渲染”解耦；schema 验证、参考实现对比、多后端渲染。
- **feedback/verifier**：JSON schema、测试用例、轨迹验证、定点 retry；比端到端代码更容易定位错误。
- **dataset**：ALGOGEN-Bench，200 个 LeetCode 任务，6 类算法及多难度。
- **evaluation**：执行/渲染成功、布局稳定性、速度；与 Manim-Direct 和 Code2Video 比较。
- **main finding**：平均成功率 99.8% vs 端到端 82.5%，提升 17.3 个百分点；验证轨迹显著降低幻觉和布局抖动。
- **limitations**：模板化 renderer 限制视觉自由度；主要覆盖可离散追踪算法；成功率不等同于教学有效性。
- **relevance tier**：A（“模型造工具/轨迹→确定性视频”重要替代范式）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2605.12159v1)、[ACL Anthology](https://aclanthology.org/2026.findings-acl.156/)

### A15. ManimAgent: Self-Evolving Multimodal Agents for Visual Education

- **authors**：Wenjia Jiang; Zongyuan Cai; Yuanhang Shao; Chenru Wang; Boyan Han; Zhixue Song; Keyu Chen; Shengwei An; Xu Yang; Zhou Yang
- **year / venue/status**：2026，EMNLP 2026 Main
- **arXiv/DOI**：[arXiv:2606.30296](https://arxiv.org/abs/2606.30296)；ACL Anthology 无 DOI
- **code/project**：[GitHub](https://github.com/jwj1342/Paper2Manim)、[项目页](https://manimagent.github.io/)、[ACL Anthology](https://aclanthology.org/2026.emnlp-main.2542/)
- **task**：从论文段落生成短 Manim 教学动画，并让经验跨任务累积。
- **representation**：论文段落/故事板 → Manim Python；双通道 Episodic Memory Bank（成功理由、失败模式）。
- **method**：渲染关键帧由 VLM 多轴评分；每轮修复后把成功模板和经筛选失败模式写入记忆；新任务检索注入。
- **feedback/verifier**：VLM 评逻辑、遮挡和教学准确性；headline 采用盲人评 Pass@1，避免“同一 VLM 既奖励又裁判”。
- **dataset**：论文段落任务流；memory-building stream 与固定 disjoint probe。
- **evaluation**：固定 probe、不同记忆规模、no-memory/RAG/shuffled-memory；人评首轮通过率和反思轮数。
- **main finding**：记忆增长时盲人评 Pass@1 上升、反思轮数下降；双通道经验优于仅文档 RAG。
- **limitations**：依赖记忆筛选器；错误经验可能污染；任务为单场景/短动画，与长视频系统不完全等价。
- **relevance tier**：A（跨任务自改进的 Manim 代码 agent）。
- **证据来源**：[paper-tool 全文对应 arXiv v3](https://arxiv.org/html/2606.30296v3)、[ACL Anthology](https://aclanthology.org/2026.emnlp-main.2542/)

### A16. LottieGPT: Tokenizing Vector Animation for Autoregressive Generation

- **authors**：Junhao Chen; Kejun Gao; Yuehan Cui; Mingze Sun; Mingjin Chen; Shaohui Wang; Xiaoxiao Long; Fei Ma; Qi Tian; Ruqi Huang; Hao Zhao
- **year / venue/status**：2026，CVPR 2026
- **arXiv/DOI**：[arXiv:2604.11792](https://arxiv.org/abs/2604.11792)；DOI 未确认
- **code/project**：[GitHub](https://github.com/yisuanwang/LottieGPT)、[项目页](https://lottiegpt.github.io/)、[CVF 论文](https://openaccess.thecvf.com/content/CVPR2026/papers/Chen_LottieGPT_Tokenizing_Vector_Animation_for_Autoregressive_Generation_CVPR_2026_paper.pdf)
- **task**：文本、图像或关键帧到可编辑矢量动画。
- **representation**：Lottie JSON 程序；层级几何、变换、关键帧、插值和 easing 的专用 token 序列。
- **method**：Lottie tokenizer + Qwen2.5-VL 微调；静态到动态课程训练；自回归生成结构化动画代码。
- **feedback/verifier**：以解析/渲染有效性和结构/视觉指标为主，无 agentic 修复闭环。
- **dataset**：LottieAnimation-660K、15M 静态 Lottie 图；LottieBench。
- **evaluation**：结构保真、语义、动画质量、文件大小/Token、用户研究；并评静态 SVG。
- **main finding**：证明模型可直接生成轻量、分辨率无关、可编辑的时间程序，而非栅格帧；文件可比视频小 10–50×。
- **limitations**：Lottie 表达范围受限；长复杂动画序列仍难；数据清洗、版权来源和真实专业编辑工作流覆盖度需进一步验证。
- **relevance tier**：A（模型直接生成可执行动画格式）。
- **证据来源**：[paper-tool/HTML 全文](https://arxiv.org/html/2604.11792v1)、[代码](https://github.com/yisuanwang/LottieGPT)

### A17. InternSVG: Towards Unified SVG Tasks with Multimodal Large Language Models

- **authors**：Haomin Wang; Jinhui Yin; Qi Wei; Wenguang Zeng; Lixin Gu; Shenglong Ye; Zhangwei Gao; Yaohui Wang; Yanting Zhang; Yuanqi Li; Yanwen Guo; Wenhai Wang; Kai Chen; Yu Qiao; Hongjie Zhang
- **year / venue/status**：2026，ICLR 2026（arXiv 初稿 2025）
- **arXiv/DOI**：[arXiv:2510.11341](https://arxiv.org/abs/2510.11341)；DOI 未确认
- **code/project**：[项目页](https://hmwang2002.github.io/release/internsvg/)、[Hugging Face](https://huggingface.co/InternSVG)
- **task**：统一 SVG 理解、编辑、静态生成与动态 SVG 动画生成（Text-to-SANI、Video-to-SANI）。
- **representation**：SVG/XML 与其动画属性/程序。
- **method**：SAgoge 大规模多域数据；SVG 特殊 token、子词初始化、从短静态 SVG 到长序列动画的两阶段训练。
- **feedback/verifier**：标准化解析和渲染评测；不是多轮 agent verifier。
- **dataset**：SAgoge 约 16M 样本（含动态动画）；SArena 约 31K benchmark queries。
- **evaluation**：理解、编辑、生成，多领域与难度；动画子集评价结构和渲染结果。
- **main finding**：统一多任务训练产生正迁移，在 SArena 与既有 SVG benchmark 上超过多种开放/闭源模型。
- **limitations**：总体贡献横跨大量静态任务，动态视频不是唯一中心；SVG 动画的长程复杂性仍有限。
- **relevance tier**：A-（动态 SVG 是直接代码渲染，但论文重心并非仅视频）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2510.11341v1)、[ICLR 论文](https://proceedings.iclr.cc/paper_files/paper/2026/file/412f33b7bfecf8d0318113a325339c96-Paper-Conference.pdf)

### A18. Training and Benchmarking Code Generation for Physics-Inspired Animations（SimuScene）

- **authors**：Yanan Wang; Renxi Wang; Yongxin Wang; Xuezhi Liang; Fajri Koto; Timothy Baldwin; Xiaodan Liang; Haonan Li
- **year / venue/status**：2026 arXiv；稿件页含 AAAI 2027 版权字样，截止日只能确认预印本/拟发表状态
- **arXiv/DOI**：[arXiv:2602.10840](https://arxiv.org/abs/2602.10840)；DOI 未确认
- **code/project**：公开代码/项目 URL 未能从全文与 Web 结果确认
- **task**：物理文字场景到可执行代码生成的定性物理动画。
- **representation**：文本场景+验证问题 → 可执行动画代码 → 渲染视频。
- **method**：自动生成难度可控场景；Code-Video-Judge 用视频验证问题产生 reward；以视觉 reward 对文本 LLM 做 RL。
- **feedback/verifier**：代码执行、渲染视频、VLM 回答每个场景的动力学验证问题；做了人评校验和 reward-hacking 检查。
- **dataset**：SimuScene，7,659 场景、52 个概念、5 个物理域；334 条人工验证测试集。
- **evaluation**：10 个模型；Avg@8、pass rate、物理/视觉验证题；最强模型 Avg@8 仅 21.5%。
- **main finding**：生成“可执行且动态语义正确”的动画远难于一般代码；7B 模型用视频 reward 训练后 pass rate 从 0% 到 11.1%。
- **limitations**：强调定性而非数值精确仿真；自动训练数据质量抽检约 84%；VLM reward 仍可能遗漏视觉/物理错误。
- **relevance tier**：A（直接 text→code→physics video 训练与 benchmark）。
- **证据来源**：[paper-tool 全文对应 arXiv v2](https://arxiv.org/html/2602.10840v2)

### A19. Reels-RSI: Program-Level Self-Improvement for Code-Rendered Explainer Videos

- **authors**：Wei Lin
- **year / venue/status**：2026，arXiv 预印本；单作者工程/field study
- **arXiv/DOI**：[arXiv:2610.14495](https://arxiv.org/abs/2610.14495)；DOI 未确认
- **code/project**：[GitHub](https://github.com/agentic-loops-x/Reels-RSI)
- **task**：一句话到带旁白、字幕、音乐、音效的多语言 explainer reel，并在程序层自我改进。
- **representation**：SCRIPT.md、STORYBOARD.md、逐帧 HTML/SVG/Canvas/Three.js composition、可执行 checks/rules。
- **method**：任意 agent harness 驱动确定性 CLI；保存每次代码快照；从 diff 提炼 lesson，再把可静态检测的 lesson 编译成带 must-fail/must-pass 单测的 rule；用 blind pairwise gate 接纳 playbook rewrite。
- **feedback/verifier**：静态规则、装配期 lint/runtime/layout/contrast 检查、渲染像素 judge、人类 gate；支持对旧作品追溯审计。
- **dataset**：共 111 reels，含 field study、2×2 memory ablation、弱导演、48-reel learning curve、judge reliability。
- **evaluation**：违规数、修订轮数、盲成对偏好、绝对 rubric、位置偏差复测。
- **main finding**：规则对强 agent 主要是审计，对弱 agent 可把 30 次违规降到 5 次；lesson 缩短修订但未显示复合增益；作者揭示 pairwise judge 62–81% 的“偏爱第二项”位置偏差。
- **limitations**：单一系统/模型家族、无真人偏好研究、规模小；首轮 11–1 改写胜利被位置偏差夸大；工程论文结论不宜外推为普遍 SOTA。
- **relevance tier**：A（代码渲染视频与程序级持续改进的直接案例）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2610.14495v1)、[代码](https://github.com/agentic-loops-x/Reels-RSI)

## 4. 核心支撑论文、Benchmark 与 Verifier（Tier B）

### B1. MoVer: Motion Verification for Motion Graphics Animations

- **authors**：Jiaju Ma; Maneesh Agrawala
- **year / venue/status**：2025，ACM TOG / SIGGRAPH 2025
- **arXiv/DOI**：[arXiv:2502.13372](https://arxiv.org/abs/2502.13372)；[10.1145/3731209](https://doi.org/10.1145/3731209)
- **code/project**：[GitHub](https://github.com/jama1017/MoVer)、[项目页](https://mover-dsl.github.io/)
- **task**：文本+静态 SVG 到 GSAP 动画，并自动验证提示中的时空约束。
- **representation**：JavaScript/GSAP SVG 动画程序；一阶逻辑 MoVer DSL；逐帧 SVG motion program。
- **method**：LLM 同时合成动画与验证程序；执行 verifier，失败谓词回传给 LLM 多轮修正。
- **feedback/verifier**：方向、幅度、运动类型、相对位置、Allen 时间关系等显式谓词。
- **dataset**：5,600 个合成文本提示及 ground-truth MoVer programs。
- **evaluation**：验证程序正确率、最终动画约束通过率；0 轮 58.8%，最多 50 轮 93.6%。
- **main finding**：符号 verifier 可把“看起来合理”转为可定位的时空约束失败并显著提高正确率。
- **limitations**：50 轮成本高；DSL 只覆盖预定义运动关系；正确约束不保证美学/叙事质量。
- **relevance tier**：B+（本身也是生成系统，但核心贡献是 verifier）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2502.13372v1)、[ACM DOI](https://doi.org/10.1145/3731209)

### B2. SGA: Plug & Play Geometric Verification for Educational Video Synthesis

- **authors**：Jhon Lopez; Carlos Hinojosa; Bernard Ghanem
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2607.18116](https://arxiv.org/abs/2607.18116)；DOI 未确认
- **code/project**：[项目页](https://jhedlp.github.io/projects/sga/)
- **task**：作为 Code2Video/TheoremExplainAgent 的几何验证插件，修复 Manim 布局冲突。
- **representation**：LLM 生成的 Manim 代码；部分执行后提取 symbolic scene graph/AABB。
- **method**：不先完整渲染，直接在符号域发现重叠/距离冲突，再做 targeted refinement；提出 MVQS。
- **feedback/verifier**：确定性的 Manim Visual Quality Score，侧重几何可读性与空间完整性。
- **dataset**：MMMC-Code；4 个 LLM backbone × 2 个 agent pipeline。
- **evaluation**：MVQS、人类成对偏好、与 VLM critic 比较。
- **main finding**：峰值 MVQS 73.11，较 raw baseline 相对提升 16.1%；人评 84.4% 偏好 SGA 胜过 raw，65.0% 胜过 VLM critic。
- **limitations**：只验证几何，不验证知识、时序或教学；AABB 等近似无法覆盖所有视觉冲突。
- **relevance tier**：B（代码视频的符号验证层）。
- **证据来源**：[paper-tool 全文对应 arXiv v2](https://arxiv.org/html/2607.18116v2)、[项目页](https://jhedlp.github.io/projects/sga/)

### B3. ManiBench: A Benchmark for Testing Visual-Logic Drift and Syntactic Hallucinations in Manim Code Generation

- **authors**：Nabin Oli
- **year / venue/status**：2026，LOCUS Research Symposium 2026 / arXiv
- **arXiv/DOI**：[arXiv:2603.13251](https://arxiv.org/abs/2603.13251)；DOI 未确认
- **code/project**：[GitHub](https://github.com/nabin2004/ManiBench)、[数据集](https://huggingface.co/datasets/nabin2004/ManiBench)
- **task**：评测 Manim CE 代码生成中的 API 幻觉与 visual-logic drift。
- **representation**：自然语言任务→Manim CE；参考来自约 53K 行 3Blue1Brown ManimGL 代码。
- **method**：执行、版本冲突扫描、视觉事件/教学元素的静态启发式检测。
- **feedback/verifier**：Executability、VCER、Alignment、Coverage；当前后两者主要基于关键词/模式。
- **dataset**：论文实测是 **12 题 pilot**，不是摘要曾宣称的 150–200 题完成版；143 scene classes、145 个 GL→CE 不兼容项。
- **evaluation**：9 个模型、276 份代码；最强执行率 66.7%，平均 coverage 约 0.17。
- **main finding**：模型规模不等于 Manim 熟练度；few-shot 是 Gemma-3-27B 唯一提升执行率的策略（+11.1pp）。
- **limitations**：无已完成的人评；alignment 指标饱和，关键词存在不等于正确动画；数据仅 12 题，摘要与正文规模表述冲突。
- **relevance tier**：B（重要但早期、规模和指标需谨慎）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2603.13251v1)、[代码](https://github.com/nabin2004/ManiBench)

### B4. Code2Video-Compass: A Comprehensive Benchmark for General-Purpose Code-Based Video Generation across T2V, I2V, and V2V

- **authors**：Zhenghan Chen; Zekai Shao; Xin Lin; Leting Cheng; Siming Chen
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2610.28416](https://arxiv.org/abs/2610.28416)；DOI 未确认
- **code/project**：[GitHub](https://github.com/code2video-compass/Code2Video-Compass)、[项目页](https://code2video-compass.github.io/)
- **task**：通用 code-based T2V/I2V/V2V 完整视频生成。
- **representation**：HTML/CSS、SVG、Canvas、Three.js，多文件程序；Remotion 渲染。
- **method**：统一文本、关键帧和参考视频输入；15 个 MLLM 在同一通用 stack 生成可执行程序。
- **feedback/verifier**：12 个客观指标+5 个主观/MLLM judge 指标；QA checklist 评指令遵循。
- **dataset**：2,104 tasks，10 大类别、24 子类，construction/dynamics/state dependency 三类复杂度。
- **evaluation**：执行成功、Token、技术/美学、平滑度、文本对齐、图像/视频参考忠实度、整体质量。
- **main finding**：领先模型也难稳定生成完整高质量视频；复杂度增加时性能系统下降；执行可靠性与视频质量不总一致。
- **limitations**：高度依赖 2026 年专有模型与 MLLM judge；参考媒体和完整 benchmark 可复现性需持续检查。
- **relevance tier**：B+（截至截止日最广的通用 code-based video benchmark）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2610.28416v1)、[代码](https://github.com/code2video-compass/Code2Video-Compass)

### B5. Animation2Code: Evaluating Temporal Visual Reasoning in Video-to-Code Generation

- **authors**：Anya Ji; Abhijith Varma Mudunuri; David M. Chan; Alane Suhr
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2606.28593](https://arxiv.org/abs/2606.28593)；DOI 未确认
- **code/project**：[项目页](https://anya-ji.github.io/animation2code-website/)
- **task**：从参考动画视频重建可执行网页动画代码。
- **representation**：单文件 HTML（内联 CSS/JavaScript）→浏览器确定性渲染视频。
- **method**：VLM zero-shot、SFT、迭代 refinement；将外观相似与时间相似分离评价。
- **feedback/verifier**：代码执行；帧对齐/图像 embedding 的 appearance metric；轨迹比较的 temporal metric，均做人类一致性验证。
- **dataset**：1,069 个 CodePen 动画视频—代码对。
- **evaluation**：执行率最高可达 100%、appearance 最高约 0.84，但 temporal similarity 最高仅 0.31。
- **main finding**：模型能复原“长得像”的网页，却难恢复精确运动规律；时间推理是独立瓶颈。
- **limitations**：输入方向是 video→code，不是常规 prompt→video；局限网页动画；指标仍无法完全覆盖感知运动质量。
- **relevance tier**：B（逆向任务，但输出代码确实再渲染为视频）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2606.28593v1)、[项目页](https://anya-ji.github.io/animation2code-website/)

### B6. PhySimCode: A Benchmark and Evaluation Method for Physics Video to Code Generation

- **authors**：Souraja Kundu; Aditya Gupta; Joel Julin; Yizhou Zhao; Liuyue Xie; Laszlo A. Jeni
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2610.15722](https://arxiv.org/abs/2610.15722)；DOI 未确认
- **code/project**：[GitHub](https://github.com/SourajaKundu/PhySimCode)、[项目页](https://sourajakundu.github.io/PhySimCode/)
- **task**：只给物理视频，恢复物理规律、参数与可运行仿真代码以重现视频。
- **representation**：SciPy/Matplotlib FuncAnimation 或 PyBullet/Kubric 等 Python 仿真程序。
- **method**：同时评物理观察、定律、ODE/数值方法、参数恢复与可执行重建。
- **feedback/verifier**：物理定律评分、simulation equivalence、代码执行、参数误差、渲染视频比较。
- **dataset**：160.6K 程序化样本、162 个物理现象、9 大物理域；公开 2,430-video evaluation set 和评价代码。
- **evaluation**：10 个开放/闭源 MLLM；物理定律陈述、从视频推断、参数恢复。
- **main finding**：模型会背定律（4.27–4.93/5），但从视频识别仅 1.51–2.47/5；最佳模型只有 7.7% 参数落在真值 ±20%。
- **limitations**：程序化域与真实视频有差距；多种代码可产生相似视频使精确代码监督不唯一；输入方向为 video→code。
- **relevance tier**：B（科学视频逆向到可执行仿真）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2610.15722v1)、[代码](https://github.com/SourajaKundu/PhySimCode)

### B7. 4DCodeBench: Benchmarking Agents on Inverse Graphics of Dynamic Scenes

- **authors**：Ruihong Shen; Žiga Kovačič; Peter Kulits; Xingrui Wang; Zizhang Li; Joshua B. Tenenbaum; Alan Yuille; Jieneng Chen; Jiajun Wu
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2610.03715](https://arxiv.org/abs/2610.03715)；DOI 未确认
- **code/project**：[GitHub](https://github.com/4DCodeBench/4DCodeBench)、[项目页](https://4dcodebench.com/)
- **task**：把真实/合成动态场景视频重建为显式 4D 场景程序。
- **representation**：可执行 graphics code，显式暴露每个时间点的 3D geometry/dynamics，并用 Blender 渲染。
- **method**：不限制动态实现，可用 Blender、Taichi、Warp 或自定义仿真；18 个 agent 统一环境比较。
- **feedback/verifier**：外观、2.5D/3D 几何、动态、VLM Elo 与人类 Elo；合成场景可直接对 4D 真值。
- **dataset**：100 个真实视频+100 个合成场景，含形变、流体、断裂等。
- **evaluation**：视觉保真、几何、动态、成本/Token；人类—VLM 排名高度一致（论文报告 ρ=0.980）。
- **main finding**：静态外观/几何能力不能转化为复杂动态重建能力；动态始终明显落后。
- **limitations**：逆向而非文本生成；执行预算很大；程序策略自由导致公平评价与等价性判定困难。
- **relevance tier**：B（通用动态场景 code reconstruction benchmark）。
- **证据来源**：[paper-tool 全文对应 arXiv](https://arxiv.org/html/2610.03715v1)、[代码](https://github.com/4DCodeBench/4DCodeBench)

### B8. VideoCoCo: Code-as-CoT for Physically-Consistent Video Generation via an Agentic Dual-Engine System

- **authors**：Haodong Li; Tianfei Ren; Xiaoxiao Ma; Chunmei Qing; Zhen Fang; Sipeng He; Ziyu Guo; Haoyu Wu; Juanxi Tian; Yihang Zou; Ruichuan An; Dongzhi Jiang; Boxue Yang; Ji Xie; Xu Huang; Wenhao Yan; Jialv Zou; Zhengrong Yue; Yaxin Luo; Xiaotong Li; Yuzhu Wang; Junyan Ye; Jinjing Zhao; Zehui Chen; Lin Chen; Renye Yan; Feng Zhao; Pheng-Ann Heng
- **year / venue/status**：2026，arXiv 预印本
- **arXiv/DOI**：[arXiv:2607.27380](https://arxiv.org/abs/2607.27380)；DOI 未确认
- **code/project**：[GitHub](https://github.com/micky-li-hd/VideoCoCo)
- **task**：文本到物理一致的写实视频。
- **representation**：coding agent 生成可执行 Blender 程序，先渲染确定性时空草稿；草稿再条件化像素视频编辑器。
- **method**：Executable Simulation Engine + Generative Video Engine 双引擎；code-as-process-level-CoT；VideoCoCo-3K 适配 draft-conditioned editor。
- **feedback/verifier**：沙箱执行、草稿渲染；最终用 PhyGenBench/VBench-2.0 等视频评价。
- **dataset**：VideoCoCo-3K，约 3K draft–instruction–target triplets。
- **evaluation**：PhyGenBench、VBench-2.0 与 ablation。
- **main finding**：相对 OmniWeaving，PhyGenBench 0.475→0.558，VBench-2.0 52.18→77.88；可执行过程草稿提高物理一致性。
- **limitations**：最终视频不是纯确定性代码渲染，而是再经生成式编辑；代码与最终像素间可能重新引入幻觉；paper-tool 因字符编码错误未能直接抽取全文，后改读 arXiv HTML 全文。
- **relevance tier**：B+（代码渲染是核心中间表征，但最终结果仍含像素生成）。
- **证据来源**：[arXiv HTML 全文](https://arxiv.org/html/2607.27380v2)、[代码](https://github.com/micky-li-hd/VideoCoCo)

## 5. 排除或仅作邻近参考的工作

| 工作/类别 | 处理 | 原因 |
|---|---:|---|
| Sora、Veo、Wan、OpenSora、Runway、Luma 等普通 T2V/I2V | X | 直接在像素/latent 空间生成，不输出并执行视觉程序。 |
| LLM-grounded Video Diffusion | X | LLM 只生成布局来条件化 diffusion；不是可执行代码渲染视频。 |
| 普通 code-conditioned video / 以源代码文本为条件的视频模型 | X | “code”是输入条件，而不是模型输出的可执行视频程序。 |
| SceneCraft（arXiv:2403.01248） | X/邻近 | 核心输出是 Blender 静态 3D scene/image；视频只作为下游生成模型的控制信号，不是主要 code-rendered video 任务。 |
| Animation2Code / PhySimCode / 4DCodeBench | B | 虽满足“模型生成代码再渲染”，但输入是视频，研究目标是逆向理解/重建，不是通常意义的正向视频创作。 |
| VideoCoCo | B | Blender 代码只产生草稿，最终写实视频还经过生成式视频编辑器。 |
| InternSVG 的静态理解/编辑/生成子任务 | X | 只有其动态 SANI 子任务纳入；静态 SVG 不属于视频。 |
| Paper2Video 等只生成讲稿、幻灯片或素材拼接的系统 | X，除非可证明生成可执行视觉程序 | “生成视频脚本”不等于“生成可执行代码”。 |
| Manim for STEM Education: Visualizing Complex Problems Through Animation | X | 展示人工使用 Manim 的教育案例，不是模型自动生成 Manim 代码。 |
| Scene/asset-only Blender code generation（如纯 text-to-3D asset） | X | 无时间程序和视频输出时不满足边界。 |

## 6. 检索策略与 Query 日志

### 6.1 arXiv-first（paper-tool）

先确认 `paper-tool` 可用，再以 relevance 排序执行检索；命中的 arXiv ID 均优先用 `paper-tool read <id> --source arxiv` 读取全文。主要 query：

- `Code2Video`
- `LLM2Manim`
- `Manimator`
- `PhysicsSolutionAgent`
- `large language model Manim animation code generation`
- `text to animation executable code rendered video`
- `programmatic video generation code rendering LLM`
- `LLM generated Blender code animation video`
- `text-to-Manim`
- `Manim code generation benchmark`
- `educational video executable Python code LLM`
- `algorithm visualization LLM Manim`
- `animation code generation large language model SVG`
- `Remotion video code generation LLM`
- `procedural animation code generation LLM video`
- `TheoremExplainAgent`
- `ManimAgent Self-Evolving Multimodal Agents for Visual Education`
- `Training and Benchmarking Code Generation for Physics-Inspired Animations`
- `Beyond End-to-End Video Models Multi-Agent Educational Video Generation`
- `Animation2Code Evaluating Temporal Visual Reasoning`
- `MG-Gen Single Image to Motion Graphics Generation`
- `SceneCraft Blender Code`
- `GPT4Motion Scripting Physical Motions Blender`
- `VisualEDU benchmark coding visual educational videos Manim`

说明：paper-tool 对若干精确长标题返回 0，但 Web 检索发现其 arXiv ID 后，均返回 `paper-tool read` 读取；没有用 Web 摘要替代可用的 arXiv 全文。

### 6.2 Web fallback

用于补足非 arXiv venue/DOI、项目仓库以及 arXiv 搜索漏检。代表性 query：

- `"Code2Video" executable code video generation paper`
- `"LLM2Manim" paper project code`
- `"Manimator" research papers visual explanations project`
- `"PhysicsSolutionAgent" paper code project`
- `LLM generates executable Manim code video paper benchmark`
- `programmatic video generation LLM executable code render animation research`
- `LLM generated Remotion code video system research paper`
- `LLM Blender Python code animation video generation paper`
- `site:arxiv.org executable animation script rendered video LLM motion graphics benchmark`
- `site:arxiv.org "code-based video generation" executable code benchmark`
- `site:arxiv.org LLM "rendered into a video" executable animation code`
- `DataReel animated data storytelling LLM code generation paper arxiv`
- `LogoMotion editable logo animations code generation paper arxiv`
- `InternSVG animation code generation paper arxiv`
- `LottieGPT structured vector animation code generation paper arxiv`
- `"Kubrick: Multimodal Agent Collaborations for Synthetic Video Generation" code project`
- `"VideoCoCo" physically consistent video generation code project`
- `"Reels-RSI" code rendered explainer videos`
- `"MoVer: Motion Verification for Motion Graphics Animations" code project venue`
- `"PhySimCode" benchmark physics video code generation arxiv project`
- `"HeyGen Code2Video Benchmark" research paper executable code video`

### 6.3 全文阅读覆盖

使用 paper-tool 成功读取的核心全文包括：Code2Video、Manimator、TheoremExplainAgent、PhysicsSolutionAgent、LLM2Manim、ManimTrainer/ManimAgent、SimuScene、LASEV、ManimAgent（self-evolving）、ANVIL、ALGOGEN、SGA、Code2Video-Compass、ManiBench、MG-Gen、Animation2Code、SceneCraft、LogoMotion、Kubrick、Data Director、DATAREEL、MoVer、LottieGPT、InternSVG、Reels-RSI、PhySimCode、4DCodeBench。  
VideoCoCo 的 `paper-tool read` 因 PDF 文本含非法 surrogate 字符失败，随后成功读取 arXiv HTML 全文。网页仅用于补 venue、DOI、代码与项目链接；报告中已把只靠摘要/索引仍无法确认的信息标为“未确认”。

## 7. 去重规则

1. **arXiv ID 为主键**：版本号不同视为同一工作，记录阅读到的最新可用版本。
2. **标题变体合并**：如 MG-Gen 标题是否带 “with Layer Decomposition”，按同一 arXiv ID 合并。
3. **预印本与正式版合并**：Code2Video arXiv/PMLR、LogoMotion arXiv/CHI、MoVer arXiv/TOG、ManimAgent arXiv/ACL Anthology 只保留一条，venue/status 写正式版本。
4. **系统、数据集、benchmark 同论文合并**：例如 TheoremExplainAgent+TheoremExplainBench、LottieGPT+LottieBench、InternSVG+SAgoge+SArena、SimuScene、DATAREEL 不拆成重复条目。
5. **同名消歧**：ManimTrainer 论文中的 **ManimBench** 与 Nabin Oli 的 **ManiBench** 是不同资源；均保留并明确区分。
6. **代码仓/项目页不单列为“论文”**：没有独立方法论文的工程项目只作为 code/project 证据；避免把论文、GitHub、项目主页重复计数。
7. **继承/插件不并入宿主**：SGA、MoVer 是独立 verifier 贡献，虽接入其他生成器，仍单列 Tier B。

## 8. 无法确认项与证据风险

- **LLM2Manim**：截至截止日未找到可核验官方代码仓和正式 venue/DOI。
- **Manimator**：可确认 ICML 2025 virtual 页面，但无法从一手可访问页面确定是主会论文、workshop 还是其他 track，故不做更强断言。
- **Kubrick**：可确认 workshop 索引，但未找到官方公开代码；不要把 SceneCraft/BlenderGPT 仓误当 Kubrick 实现。
- **Data Director**：所读作者稿 DOI 是占位符；仅确认 IEEE Visualization 作者稿状态。
- **MG-Gen**：能确认 IEEE Xplore 记录与官方仓，但当前证据未给出可靠 DOI/具体会议名。
- **SimuScene**：PDF 有 AAAI 2027 版权字样，但截止 2026-10-27 不据此断言已正式出版；项目/代码链接未确认。
- **LASEV**：吞吐和降本来自作者部署报告，缺少独立复现；项目页不等于完整代码开源。
- **ManiBench**：摘要检索记录曾称 150–200 题，但全文明确当前 pilot 只有 12 题；本报告以全文为准，并把扩展规模视为计划而非既成事实。
- **VideoCoCo**：paper-tool PDF 文本抽取失败，已改用 arXiv HTML；最终视频含生成式编辑，不能与纯代码渲染系统混为一类。
- **HeyGen Code2Video Benchmark**：Code2Video-Compass 全文把它列为相关 benchmark，但公开 Web 搜索未找到足够稳定的一手论文/技术报告元数据，因此未作为独立核心条目；仅在检索日志与无法确认项保留。
- **截至日风险**：2026 年 10 月论文很新，venue、版本、代码开放状态可能在截止日后变化；本文件只陈述截止时可核验证据。

## 9. 面向新仓库的建议分类标签

建议后续 awesome 列表至少使用以下正交标签，避免把不同问题混成一类：

- `input`: text / paper / table / image / video / theorem / problem
- `program`: Manim / Blender Python / HTML-CSS-JS / D3.js / SVG-SMIL / GSAP / Lottie JSON / Remotion / simulation
- `output`: educational-long-form / motion-graphics / data-video / physics / inverse-reconstruction / vector-animation
- `generation`: direct / planner-coder / multi-agent / trained-model / tool-generation / inverse-graphics / hybrid-code-diffusion
- `verification`: compiler / renderer-in-loop / VLM-critic / symbolic-geometry / DSL / schema / unit-test / human-gate
- `evidence`: peer-reviewed / preprint / benchmark / code-open / data-open / project-only
- `tier`: A-direct / B-support / X-excluded
