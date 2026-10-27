# 可执行 3D / 游戏引擎场景智能体研究

> 检索截止：**2026-10-27**。主题边界：LLM/VLM 生成并执行 Blender/Python、3D scene program、Unity/Unreal 脚本、程序化动画或机器人仿真场景代码，以及 **generate → execute → render/simulate → critique/test → repair** 闭环。

## 1. 范围、方法与分级

### 1.1 纳入与排除

**纳入条件（至少满足一项）**：

1. 输出可执行的 Blender Python、CAD/DSL、游戏引擎脚本、场景图/事件图或仿真代码；
2. 输出可被 Blender、Unity、Unreal、AI2-THOR、物理引擎或确定性场景执行器直接加载、执行和渲染；
3. 明确研究生成—执行—视觉/结构/运行时反馈—修复闭环；
4. 虽不使用 LLM，但提供可执行程序化场景基础设施、数据生成器或该方向的关键评测基座。

**排除条件**：普通 text-to-3D mesh/NeRF/3DGS、仅输出不可执行静态几何或视频像素、只做 3D 理解/问答、只生成 NPC 对话的工作，除非它能直接支撑可执行场景或视频渲染闭环。

### 1.2 分级

- **Core**：直接生成/编辑可执行 3D、动态场景或游戏/仿真程序，或直接评测此能力。
- **Adjacent**：可执行表示与引擎在环明确，但目标偏材质编辑、电影制作、机器人训练等相邻任务。
- **Background**：非 LLM 的程序化生成/渲染基础设施，是构建代码生成智能体和可控视频流水线的重要底座。

### 1.3 检索方法

先使用 `paper-tool` 对 arXiv 做主题检索与全文读取，再用 Web Search 补充论文官网、会议页、项目页和源码仓库。重点全文核查了 SceneCraft、3D-GPT、Holodeck、LL3M、aDSL、AutoUE、Authoring for Living Worlds、Scene Co-pilot；其余项目用 arXiv/会议原文与官方仓库交叉核对。日期以首次公开论文为主，2026 年工作均按截止日版本记录。

## 2. 总览与关键结论

### 2.1 代表性系统矩阵

| 分级 | 系统 | 年份 | 执行目标 | 输出表示 | 自动反馈 | 开源/可复现性 |
|---|---:|---:|---|---|---|---|
| Core | SceneCraft | 2024 | Blender | Python + scene graph + constraints | 渲染图 + VLM + 外循环技能库 | 论文充分；代码公开状态不如后续系统清晰 |
| Core | LL3M | 2025 | Blender | 可读 Python、节点与修改器 | 多视图渲染 + critic + debug | [代码](https://github.com/threedle/ll3m)，但原模型服务已停 |
| Core | aDSL | 2026 | 自研 DSL/几何执行器 | 层级组件 + 关系算子 + 约束 | 执行日志 + 几何/视觉/约束 critic | [代码](https://github.com/sig-pku/aDSL) |
| Core | SceneCode | 2026 | Blender/仿真器 | 场景程序 + 分件资产 + joints | planner–designer–critic | [代码](https://github.com/wangpuyi/SceneCode) |
| Core | GS-Agent | 2026 | 物理仿真引擎 | 物理场景代码 + 相机/灯光 | 渲染帧/多模态反馈 + 修复 | 项目页公开；代码状态需按仓库复核 |
| Core | AutoUE | 2026 | Unreal Engine | PCG 图 + C++ gameplay/interaction | 编译、运行时命令、自动 play-test | [代码](https://github.com/Pluto156/AutoUE) |
| Core | UnrealLLM | 2025 | Unreal Engine 5 | 文本蓝图/PCG 配置 | 规则与引擎约束；交互式修订 | [代码](https://github.com/XGRIDS-3D/Interactive-3D-Scene-Creation-via-LLM-Driven-Procedural-Generation) |
| Core | Living Worlds | 2026 | GEST-Engine/GTA SA | 时空事件图 GEST | 工具层状态约束 + 执行反馈 | 系统、引擎、数据均有版本化发布 |
| Core | Cutscene Agent | 2026 | Unreal Engine | 工具调用轨迹 + cutscene 状态 | API 依赖校验 + 引擎反馈 | 项目页公开；源码状态未充分确认 |
| Core | GPT4Motion | 2024 | Blender physics | Blender Python | 主要是单向执行；弱修复闭环 | [代码](https://github.com/jiaxilv/GPT4Motion) |
| Core | 4DCodeBench | 2026 | 图形/物理程序 | 从视频重建可执行动态程序 | render-back + 时序几何检查 | [代码](https://github.com/4DCodeBench/4DCodeBench) |
| Core | 3DCodeBench | 2026 | Blender/Infinigen | 独立 Blender 脚本 | 编译/执行 + 2D/3D/LLM 评分 | [代码](https://github.com/gaoypeng/3dcodebench) |
| Core | Code4Scene | 2026 | Unreal Engine | 构建/编辑代码 | 引擎原生状态、物理与完整性检查 | 190 个案例；项目/论文公开 |
| Adjacent | FilmAgent | 2024/2025 | Unity | 剧本、演员动作、机位指令 | Critique-Correct-Verify / Debate-Judge | [代码](https://github.com/HSwotch/FilmAgent) |
| Background | Infinigen | 2023–2025 | Blender | 大规模程序化 Python/节点 | 确定性生成与渲染，不含 LLM critic | [代码](https://github.com/princeton-vl/infinigen) |

### 2.2 研究发现

1. **代码/程序是最有工程价值的 3D 生成表示**：它天然支持版本控制、局部编辑、参数暴露、引擎执行、结构检查和重渲染；mesh-only 结果很难支持后续游戏逻辑、关节、物理和精确修复。
2. **最有效的闭环不是只让 VLM“看图挑错”**。成熟系统把三类反馈组合起来：语法/异常反馈、结构与约束检查、渲染/视频感知反馈。SceneCraft 偏视觉与关系约束；LL3M 加入代码 debug 和多视图 critic；aDSL、Living Worlds、AutoUE 更进一步，把不可违反的规则放入执行器或工具层。
3. **表示与智能体必须共同设计**。直接生成低层 `bpy` 或 UE API 调用表达力强但脆弱；scene graph、aDSL、GEST、PCG graph 等中间表示能把绝对坐标和 API 细节变成关系、能力与状态约束。
4. **“有效即构造（valid by construction）”优于事后修补**。Living Worlds 的工具约束方案将可执行率从分阶段基线的 0/50 提升到 20/25；其意义不是某个模型更强，而是约束从 prompt 移到了不可绕过的状态后端。
5. **动态世界的评测正从图像相似度转向持久状态**。4DCodeBench 检查逐帧几何与动力学，Code4Scene 检查 UE 原生场景状态、完整性和物理有效性，AutoUE 运行自动 play-test；这比 CLIP 或单张 hero render 更接近真实生产要求。
6. **视频生成可把执行场景作为“结构控制层”**。GPT4Motion 用物理模拟生成 depth/edge 序列，SceneCraft 用 3D scene 辅助视频模型，Scene Co-pilot 和 GEST-Engine 直接输出时序一致视频；优势是身份、接触、遮挡和相机轨迹有显式状态可查。
7. **当前主要瓶颈**：长程状态与跨镜头连续性、资产许可/检索覆盖、相机与灯光联合优化、动画/接触的可微或可验证评分、Blender/UE 版本漂移、非确定性 LLM 与高昂渲染成本，以及缺少覆盖“脚本正确—场景正确—画面好看—运动可信”的统一基准。

## 3. Core：直接可执行的 3D / 动态场景智能体

### 3.1 SceneCraft: An LLM Agent for Synthesizing 3D Scene as Blender Code

- **元数据**：Hu et al.，ICML 2024；[arXiv:2403.01248](https://arxiv.org/abs/2403.01248)，[PMLR](https://proceedings.mlr.press/v235/hu24g.html)。
- **任务**：把复杂文本描述转换为最多包含约百个资产的 Blender 场景，并支持电影场景重建与视频生成控制。
- **表示**：场景图作为蓝图；LLM 生成 Python，将空间关系转为数值约束，再由专用 solver 求位置、朝向和尺度。
- **反馈**：内循环执行 Blender、渲染、由 GPT-V 判断文本—画面对齐并定位错误关系后修脚本；外循环把跨任务复用的代码模式写入空间技能库。
- **数据**：自建带真值空间约束的合成集；Sintel 电影场景；外部 3D asset library。
- **评测**：constraint pass、CLIP、人类偏好与下游视频条件效果；论文报告相对 BlenderGPT 的 CLIP 提升 45.1%/40.9%，constraint passing 88.9 对 5.6。
- **Finding**：scene graph + solver 负责精确布局，VLM 负责语义诊断，比让 LLM 直接输出大量绝对坐标稳健；非参数技能库可跨场景积累修复经验。
- **Limitations**：强依赖资产库与闭源模型；渲染视角可能隐藏 3D 错误；对复杂材质、拓扑、动画和物理的覆盖有限。
- **可复现性**：论文、算法与评测描述充分；需自行准备 Blender、资产库与模型 API，完整端到端复现门槛中高。

### 3.2 3D-GPT: Procedural 3D Modeling with Large Language Models

- **元数据**：Sun et al.，2023/2024；[arXiv:2310.12945](https://arxiv.org/abs/2310.12945)，[项目页](https://chuny1.github.io/3DGPT/3dgpt.html)。
- **任务**：自然语言驱动程序化 3D 建模、场景修改、动画与简单物理模拟。
- **表示**：调用已有程序化函数的 Blender Python；三个角色为 task dispatch、conceptualization、modeling agent。
- **反馈**：支持用户连续指令和执行结果，但没有 SceneCraft/LL3M 式系统化多视图 critic-repair。
- **数据**：不训练；依赖程序化资产/函数与 prompt 中的函数说明。
- **评测**：主要为多类场景、材质、网格编辑、动画和物理案例的定性实验与用户协作展示。
- **Finding**：早期明确提出“LLM 生成代码控制 DCC”而非直接生成网格，证明程序化参数和 Blender API 可作为可编辑输出层。
- **Limitations**：函数库边界限制开放世界能力；量化基准弱；LLM 对函数选择、参数和 Blender 上下文仍会出错。
- **可复现性**：项目页和实现资源可用性尚可，但依赖模型/API 与具体 Blender 环境。

### 3.3 LL3M: Large Language 3D Modelers

- **元数据**：Lu et al.，2025；[arXiv:2508.08228](https://arxiv.org/abs/2508.08228)，[项目页](https://threedle.github.io/ll3m/)，[源码](https://github.com/threedle/ll3m)。
- **任务**：从文本生成开放词汇 3D 资产，并执行局部几何、材质和样式编辑。
- **表示**：模块化、带注释的 Blender Python，覆盖 BMesh、modifier、shader node；共享代码上下文支持局部改写。
- **反馈**：planner → coder/retriever → execute/debug → critic；critic 多视图渲染后以 VLM 发现断裂、比例或语义问题，再让代码代理修复；另有用户引导细化阶段。
- **数据**：无需专用 3D 训练；BlenderRAG 从 Blender API 文档和代码示例检索知识。
- **评测**：多类别生成、精确编辑、样式/材质编辑、人类与自动视觉评价、消融 RAG 和自动细化。
- **Finding**：共享可执行代码既是生成表示也是记忆；RAG 提升高级 Blender API 使用；多角色比单次脚本生成更能兼顾可执行性与外观。
- **Limitations**：物体级结果多于复杂场景级；视觉 critic 会漏掉背面、内部拓扑与严格尺寸错误；原使用的 Claude Sonnet 3.7 已退役。
- **可复现性**：源码公开，但官方仓库说明原模型退役并停止 LL3M server；替换模型后结果不保证完全复现。

### 3.4 Agentic 3D Creation via Joint Agent–Program Design（aDSL）

- **元数据**：Wang et al.，2026；[arXiv:2608.17975](https://arxiv.org/abs/2608.17975)，[源码](https://github.com/sig-pku/aDSL)。
- **任务**：文本/图像条件的 3D 建模、编辑、关节资产与结构化场景组合。
- **表示**：agent-centric DSL；层级组件、可组合模块与 `align/on-top-of/contact` 等关系算子替代脆弱绝对坐标。
- **反馈**：Plan–Execute–Critic；执行后收集日志、几何测量、视觉和约束违反信号，循环修复到满足约束或耗尽预算。
- **数据**：training-free；依赖 DSL 标准库、任务提示与评测样例。
- **评测**：文本/图像到 shape，对比 LLM Blender/CAD 基线；考察结构、可控性、约束满足和编辑。
- **Finding**：关键不是单纯换更强 LLM，而是让语言抽象匹配 LLM 擅长的语义分解与空间关系推理，再由执行器解数值几何。
- **Limitations**：DSL 的上限受操作集与组件库限制；风格化自由形体和复杂拓扑仍不及低层 Blender；需要额外编译/执行栈。
- **可复现性**：代码已公开，表示、agent loop 和消融较完整，是研究“表示—智能体共设计”的优先复现对象。

### 3.5 SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects

- **元数据**：Wang et al.，2026；[arXiv:2605.19587](https://arxiv.org/abs/2605.19587)，[项目页](https://scene-code.github.io/)，[源码](https://github.com/wangpuyi/SceneCode)。
- **任务**：从文本生成完整室内世界，既包含布局，也按需生成可分件、可关节化、可进仿真器的对象。
- **表示**：可执行 world program；场景级布局程序 + 对象级 part/assembly/joint/metadata，而非单体静态 mesh。
- **反馈**：planner–designer–critic 迭代，对对象结构、场景关系与可执行产物做检查。
- **数据**：室内提示、资产/对象程序与下游机器人交互设置；论文强调不只继承资产库已有 articulation。
- **评测**：场景合成、对象质量、人类判断、mesh 结构、simulator-loadable articulation 和机器人交互。
- **Finding**：把“场景”和“可交互资产”统一为程序，补齐普通 scene layout 系统只能摆放静态库资产的缺口。
- **Limitations**：室内域为主；代码生成对象的美术细节、碰撞体、质量/摩擦参数和关节真实性仍是薄弱点。
- **可复现性**：论文、项目和官方仓库齐全；重现完整机器人评测仍需要相应 simulator/asset 环境。

### 3.6 Nova3D: Code-Native Generation of Programmable 3D Assets

- **元数据**：Noor et al.，2026；[arXiv:2607.22738](https://arxiv.org/abs/2607.22738)，[源码](https://github.com/RareSense/Nova3D)。
- **任务**：生成可编程、可编辑、带装配层级和关节的 3D 资产，面向游戏、配置器与机器人仿真。
- **表示**：Blender 可执行源码是主资产；GLB mesh 只是编译产物。程序显式保留 named parts、assembly tree、约束、edit handle、pivot 和 joint。
- **反馈**：代码生成、编译、结构/约束验证与必要修复；源码工作区支持版本化编辑。
- **数据**：自建 54 项 Nova3D-Bench 与程序化资产任务。
- **评测**：对 11 类基线比较视觉质量、结构可编程性、约束与关节信息。
- **Finding**：评价 3D 资产不应只看表面相似度；原生可寻址部件和关节决定其能否进入真实生产/仿真流程。
- **Limitations**：benchmark 较小且真值构造与系统关系密切；资产级为主，复杂多物体世界和动态闭环不是核心。
- **可复现性**：官方仓库和 benchmark 可用，工程化程度较高。

### 3.7 BlenderLLM: Training LLMs for CAD with Self-improvement

- **元数据**：Du et al.，2024；[arXiv:2412.14203](https://arxiv.org/abs/2412.14203)，[源码](https://github.com/FreedomIntelligence/BlenderLLM)，[CADBench](https://huggingface.co/datasets/FreedomIntelligence/CADBench)。
- **任务**：从开放式 CAD 指令生成可在 Blender 执行并渲染的脚本。
- **表示**：`bpy`/Blender CAD Python；基于 Qwen2.5-Coder-7B-Instruct 微调。
- **反馈**：训练阶段用 self-improvement 生成、筛选和再训练；推理闭环弱于 agentic critic 系统。
- **数据**：BlendNet；CADBench 含 500 个模拟样本和 200 个在线论坛样本。
- **评测**：执行/渲染结果，由 MLLM-as-judge 对 CAD 质量多维评分，并与通用/代码模型比较。
- **Finding**：领域数据和自提升可让中等规模代码模型掌握 Blender CAD 脚本，说明“专模 + 执行器”可替代每次调用超大闭源模型。
- **Limitations**：CAD 对象偏简单；MLLM judge 的偏差、脚本安全和跨 Blender 版本兼容需要额外控制。
- **可复现性**：模型、数据、benchmark、源码均公开，Apache-2.0 模型卡；是较完整训练型基线。

### 3.8 GS-Agent: Creating 4D Physical Worlds with Generative Simulation

- **元数据**：Zhang et al.，2026；[arXiv:2607.21522](https://arxiv.org/abs/2607.21522)，[项目页](https://umass-embodied-agi.github.io/gs-agent/)。
- **任务**：自然语言生成包含刚体、软体、流体交互以及电影化相机/灯光的 4D 物理世界。
- **表示**：多智能体编写物理引擎场景代码，显式指定资产、材质、初始状态、动力学、相机和灯光。
- **反馈**：执行仿真并渲染帧；多模态 reviewer 检查物理/视觉与 prompt 对齐，代理据此修改代码。
- **数据**：文本物理场景任务、资产集合与仿真轨迹；不依赖纯视频训练来隐式学习物理。
- **评测**：物理合理性、文本一致性、场景多样性及相机/灯光质量，配合视频案例和人类/模型评价。
- **Finding**：确定性/数值物理引擎置于生成环中，可把难以约束的 text-to-video 动力学变成可执行、可检查程序。
- **Limitations**：对资产与物理参数初始化敏感；仿真正确不等于真实；高质量渲染和多材料仿真成本高。
- **可复现性**：论文与项目视频公开；应在采用前进一步核实完整代码、资产和仿真配置是否全量发布。

### 3.9 GPT4Motion: Scripting Physical Motions in Text-to-Video Generation

- **元数据**：Lv et al.，CVPRW 2024；[arXiv:2311.12631](https://arxiv.org/abs/2311.12631)，[源码](https://github.com/jiaxilv/GPT4Motion)。
- **任务**：文本生成具有连贯基础物理运动的视频。
- **表示**：GPT-4 生成 Blender Python，驱动内置 physics engine；从模拟得到逐帧 depth/edge，再控制图像生成模型。
- **反馈**：Blender 提供确定性物理执行与控制序列，但核心管线主要是单向计划—执行—生成，不是强自修复 agent loop。
- **数据**：训练免费；依赖 prompt 模板、Blender 基元/物理和预训练图像扩散模型。
- **评测**：运动连贯性、视频质量、与文本一致性，并展示碰撞、落体等基础物理场景。
- **Finding**：低保真但物理正确的 3D 动画可作为高保真视频扩散的结构条件，是“代码生成视频”的重要混合范式。
- **Limitations**：动作/物理原语有限，复杂角色动画、接触和镜头叙事不足；扩散阶段仍可能破坏几何与身份。
- **可复现性**：论文、项目与 GitHub 公开；依赖外部扩散模型和 GPT API。

### 3.10 AutoUE: Automated Generation of 3D Games in Unreal Engine via Multi-Agent Systems

- **元数据**：Yin et al.，2026；[arXiv:2603.07106](https://arxiv.org/abs/2603.07106)，[源码](https://github.com/Pluto156/AutoUE)。
- **任务**：从描述端到端生成 UE 3D 游戏：模型检索、场景、gameplay、交互对象和自动测试。
- **表示**：UE PCG layout graph、模块化 C++ gameplay/interaction code、结构化跨代理规格和 MCP runtime commands。
- **反馈**：RAG 检索 UE 工具文档；编译/运行时日志；play-testing agent 生成并执行测试命令，检查动态行为。
- **数据**：858K 3D 模型嵌入库；20 个 game-generation tasks；UE 文档和 game design patterns。
- **评测**：场景质量、代码与交互行为、运行时日志、自动测试成功率和组件消融。
- **Finding**：游戏不是一张场景图；只有同时验证可编译代码、互动流程和运行时行为，才算端到端生成成功。
- **Limitations**：任务集仅 20 个；UE 版本、插件、资产路径与构建环境很脆弱；自动测试难覆盖开放式玩法和审美。
- **可复现性**：源码公开，但需要匹配 UE 工程、资产库、编译工具链与模型服务，硬件和环境成本高。

### 3.11 UnrealLLM

- **元数据**：Tang et al.，Findings of ACL 2025；[ACL Anthology](https://aclanthology.org/2025.findings-acl.994/)，[源码](https://github.com/XGRIDS-3D/Interactive-3D-Scene-Creation-via-LLM-Driven-Procedural-Generation)。
- **任务**：自然语言驱动 UE5 程序化场景生成，要求可控、可交互、game-ready。
- **表示**：多代理把需求映射到 UE5 PCG 系统和文本化 blueprint/配置；结合大规模资产库。
- **反馈**：知识库约束 PCG/API 使用，生成结果可在引擎中交互式编辑；闭环偏引擎规则和用户修订，而非强视觉自动 critic。
- **数据**：UE/PCG 知识库、资产库、文本—蓝图样例。
- **评测**：场景可控性、多样性、交互性、质量与用户评价。
- **Finding**：调用成熟 PCG 系统比让 LLM 逐对象硬编码更具规模性；文本蓝图保留专业引擎工作流的可编辑性。
- **Limitations**：UE 工程依赖重；PCG graph 能表达的玩法/逻辑有限；美术资产质量与检索覆盖决定结果上限。
- **可复现性**：官方仓库公开；需按仓库固定 UE 版本、插件和资产配置。

### 3.12 Authoring for Living Worlds: Tool-Constrained LLM Agents for Executable Multi-Actor Scenarios

- **元数据**：Cudlenco et al.，2026；[arXiv:2604.10383v4](https://arxiv.org/abs/2604.10383v4)，[agent release](https://github.com/ncudlenco/multiagent_story_system/releases/tag/v1.1-eccv2026)，[GEST-Engine](https://github.com/ncudlenco/mta-sim/releases/tag/v1.0-iclr2026)，[GTASA 数据](https://huggingface.co/datasets/nnc-001/gtasa-01)。
- **任务**：自由文本生成多场景、多演员、状态依赖的可执行故事，并渲染为带逐帧真值的叙事视频。
- **表示**：Graphs of Events in Space and Time（GEST）；节点为动作/实体/地点，边编码 Allen 时间关系、逻辑和语义关系。
- **反馈**：30+ validated tools 接到事务型状态后端；能力分页探索、POI 容量、姿态、持物、对象生命周期、原子动作链和无环时间约束均在写入时检查；错误返回代理重规划。
- **数据**：GTASA 场景图、视频、描述与逐帧空间/语义/分割真值；游戏世界含 70+ 环境、733 对象、2,500+ 动画和 312 角色皮肤。
- **评测**：执行成功、图→文→代理→图重建 F1、动作次序 bigram；tool-constrained 20/25 可执行，分阶段 GPT-5 基线 0/50；事件+实体 F1 0.83，对随机 0.55。
- **Finding**：状态约束必须在每一步操作时执行，而非最终 JSON 上事后校验；弱模型 + 强工具约束可胜过强模型 + 长 prompt。
- **Limitations**：世界能力由固定游戏资产/动作注册表限制；视觉渲染与动画质量继承旧游戏引擎；5 次失败来自执行器运行时而非规格非法。
- **可复现性**：系统、引擎、数据均给出论文对应 tag，是动态叙事与 ground-truth 视频方向最完整的开放复现链之一。

### 3.13 Cutscene Agent

- **元数据**：He et al.，2026；[arXiv:2604.25318](https://arxiv.org/abs/2604.25318)，[项目页](https://kuaishou-gamemind.github.io/cutscene_agent/)。
- **任务**：在 Unreal 中自动完成剧本、角色动作、镜头、声音与技术调度，生成 3D cutscene。
- **表示**：面向引擎能力的工具调用与 cutscene state；通过 API-derived dependency graph 约束调用依赖。
- **反馈**：引擎执行反馈、轨迹/API 依赖校验和多角色生产流程；重点是调用轨迹合法性与成片质量。
- **数据**：论文评测 65 个不同复杂度的 cutscene scenarios，并组织分层评分。
- **评测**：工具轨迹、完成度、画面/叙事/镜头质量与复杂度分层表现。
- **Finding**：cutscene 生成把 3D scene code、procedural animation、摄像机和音频整合为统一的时序 authoring 问题。
- **Limitations**：API 轨迹合法不等于世界状态始终合法；预制角色动画和工具集合限制开放性；引擎工程复现成本高。
- **可复现性**：论文和项目页公开；截至截止日未在已核实来源中确认完整训练/执行代码全量开放。

### 3.14 评测基准：3DCodeBench、Code4Scene、4DCodeBench

#### 3DCodeBench

- **元数据**：Gao et al.，2026；[arXiv:2606.01057](https://arxiv.org/abs/2606.01057)，[源码](https://github.com/gaoypeng/3dcodebench)。
- **任务**：文本/图像条件下由 coding agent 编写程序化 3D；覆盖 single-shot、multi-turn、full agent。
- **表示**：基于 Infinigen/Indoors 提炼并转换的独立 Blender 5.0 脚本。
- **反馈**：评测端执行脚本并渲染；agent setting 可依据执行错误和图像继续修复。
- **数据**：3DCodeData，类别和程序来自 Infinigen 生态的程序化资产。
- **评测**：executability、SigLIP-2/DINOv3 图像相似、Chamfer/Uni3D 3D 距离、LLM judge。
- **Finding**：同时测 2D render、3D geometry 和执行成功，避免只凭单视图判断代码建模。
- **Limitations**：以资产为主；来源于 Infinigen 的分布可能偏向其程序风格；LLM judge 仍有主观性。
- **可复现性**：官方代码与数据公开，适合做 Blender coding agent 回归测试。

#### Code4Scene

- **元数据**：Ye et al.，2026；[arXiv:2609.36777](https://arxiv.org/abs/2609.36777)，[项目页](https://simworld-ai-code4scene.static.hf.space/index.html)。
- **任务**：coding agent 在 Unreal Engine 中构建和编辑持久 3D 场景。
- **表示**：引擎内代码/操作作用于 UE 原生 scene state，而不是只产出最终截图。
- **反馈**：共享执行接口；可检查对象、变换、关系、碰撞/物理和非目标对象是否被意外改动。
- **数据**：190 个由人类组装场景构造的 cases，覆盖 construction 与 editing。
- **评测**：task fulfillment、artifact integrity、physical validity，并结合渲染。
- **Finding**：好看的 render 可能掩盖穿插、关系错误和无意修改；必须检查持久场景状态。
- **Limitations**：UE 特定；人类组装案例规模仍有限；结果受引擎版本和工具暴露面影响。
- **可复现性**：论文和可视化项目公开；完整 UE 运行包与许可依项目发布内容而定。

#### 4DCodeBench

- **元数据**：Shen et al.，2026；[arXiv:2610.03715](https://arxiv.org/abs/2610.03715)，[源码](https://github.com/4DCodeBench/4DCodeBench)。
- **任务**：给定视频，agent 用代码重建动态场景，即 inverse graphics of dynamic scenes。
- **表示**：显式可执行 graphics program，包含几何、轨迹、动画或物理模拟抽象。
- **反馈**：执行程序并 render-back 为视频，同时逐帧检查提交 mesh、轨迹和 3D 测量。
- **数据**：动态物理场景视频、参考几何/轨迹和可执行评测资产。
- **评测**：视频匹配、3D 几何、时间轨迹和动态行为，而非只测静态最后一帧。
- **Finding**：动态场景代码是连接视频理解、物理推理与可控渲染的关键 benchmark 形式。
- **Limitations**：逆图形存在多解；像素接近不代表因果机制正确，几何接近也不保证材质/镜头一致。
- **可复现性**：官方仓库公开，可用于 procedural animation 和闭环视频重建研究。

## 4. Adjacent：强相关但目标不完全是通用场景代码

### 4.1 Holodeck: Language Guided Generation of 3D Embodied AI Environments

- **元数据**：Yang et al.，CVPR 2024；[arXiv:2312.09067](https://arxiv.org/abs/2312.09067)，[源码](https://github.com/allenai/Holodeck)。
- **任务**：文本生成可交互 AI2-THOR 室内环境，用于 embodied navigation 训练。
- **表示**：LLM 生成 floor plan、材质、门窗、对象选择和对象间空间约束；优化器求布局后写入模拟器场景。
- **反馈**：主要通过约束优化、碰撞/可放置规则和模块化对话；没有以渲染 VLM 自动修图为核心。
- **数据**：Objaverse 50K+ 资产候选、ProcTHOR/AI2-THOR 材质和交互属性；680 人用户研究。
- **评测**：住宅/开放类型场景的人类偏好、对象选择与布局质量、在新场景类型上的 object navigation。
- **Finding**：交互属性和 simulator compatibility 比 photorealism 更重要；LLM 常识 + 约束优化能扩展硬编码程序化房间分布。
- **Limitations**：单房间生成约 3 分钟（论文实现）；资产检索与布局为主，不生成新对象拓扑/关节；闭环视觉修复有限。
- **可复现性**：官方代码公开，AI2-THOR 环境可复现；需模型 API 与 Objaverse/资产预处理。

### 4.2 RoboGen

- **元数据**：Wang et al.，ICML 2024；[arXiv:2311.01455](https://arxiv.org/abs/2311.01455)，[PMLR](https://proceedings.mlr.press/v235/wang24cc.html)，[源码](https://github.com/Genesis-Embodied-AI/RoboGen)。
- **任务**：自动提出机器人任务、生成场景与训练监督，再选择 RL、motion planning 或 trajectory optimization 学习技能。
- **表示**：任务规范、仿真场景配置/代码、奖励与训练程序；开源重实现使用 PyBullet。
- **反馈**：仿真 rollout、成功判定和学习信号形成生成—训练—验证循环，但不以渲染审美 critic 为目标。
- **数据**：模型自动产生任务/环境/监督和技能轨迹。
- **评测**：多类操控与移动任务的生成多样性、训练成功和策略表现。
- **Finding**：LLM 不必直接输出动作；让其生成“可训练世界 + 监督程序”可放大机器人数据生产。
- **Limitations**：任务/奖励错误可能产生 reward hacking；仿真资产与动力学现实差距明显；原 Genesis 与公开 PyBullet 重实现存在差异。
- **可复现性**：PyBullet 版本公开；论文原始引擎环境的完全一致复现需谨慎。

### 4.3 FilmAgent

- **元数据**：Xu et al.，SIGGRAPH Asia 2024 / arXiv 2025；[arXiv:2501.12909](https://arxiv.org/abs/2501.12909)，[项目页](https://filmagent.github.io/)，[源码](https://github.com/HSwotch/FilmAgent)。
- **任务**：在预建 Unity 虚拟空间内端到端完成创意、剧本、演员调度和摄影。
- **表示**：结构化剧本 JSON、演员位置/动作、镜头和音频指令，在 Unity sandbox 执行。
- **反馈**：多代理扮演导演、编剧、演员、摄影；使用 Critique-Correct-Verify 与 Debate-Judge 协作策略。
- **数据**：15 个 Unity 电影空间/故事设置及生成影片资源。
- **评测**：人类对叙事、镜头、角色表演和整体影片质量评价。
- **Finding**：电影制作适合角色化代理和阶段性 artifact；引擎确保演员身份、场景与镜头状态可持续。
- **Limitations**：主要从预定义 stage positions、actions、shots 中选择，不等价于开放式 Unity 代码生成；视觉与动作上限受沙盒资产限制。
- **可复现性**：代码资源公开，但完整 Unity 项目/大文件和精确编辑器版本需要额外下载配置。

### 4.4 Scene Co-pilot

- **元数据**：Qian et al.，2024；[arXiv:2411.18644](https://arxiv.org/abs/2411.18644)，[项目页](https://abolfazl-sh.github.io/Scene_co-pilot_site/)。
- **任务**：让非专家通过文本和 Blender UI 控制 Infinigen，产出程序化场景与视频。
- **表示**：Scene Codex 将文本转成 Infinigen/Blender Python；BlenderGPT 负责细节修改；程序化资产以代码/geometry node 形式保存。
- **反馈**：人类在环查看 Blender 即时视觉结果并反复编辑；不是全自动 VLM critic。
- **数据**：300+ node-based procedural assets，配合 Infinigen 生成器与检索。
- **评测**：场景/视频定制能力、可控性和案例展示。
- **Finding**：对视频生产而言，人机协作闭环可能比完全自治更实际；代码资产库可同时提供多样性与可编辑性。
- **Limitations**：自动评测与强基线有限；依赖人工选择和修订；论文中算法描述部分比系统演示弱。
- **可复现性**：项目页与论文公开；完整数据/代码发布程度需逐项核实。

### 4.5 BlenderAlchemy

- **元数据**：Huang et al.，ECCV 2024；[arXiv:2404.17672](https://arxiv.org/abs/2404.17672)，[项目页/代码](https://ianhuang0630.github.io/BlenderAlchemyWeb/)。
- **任务**：根据文本或参考图编辑 Blender 的程序化材质、几何与产品灯光。
- **表示**：对已有 Blender visual program/node graph 生成可执行编辑序列，涉及参数、节点类型与连边。
- **反馈**：visual state evaluator、visual edit generator、搜索与 edit reversion；可用生成的“想象参考图”给抽象描述视觉落地。
- **数据**：程序化材质/场景编辑任务和参考图。
- **评测**：文本/图像条件的材质与灯光编辑，人类/视觉对齐和搜索组件消融。
- **Finding**：对已有场景做小步可回退编辑，比一次重写全场景更适合稳定闭环；节点图是高价值结构状态。
- **Limitations**：任务集中于材质/灯光和局部编辑，不是通用场景生成；搜索成本随编辑空间快速增长。
- **可复现性**：论文、项目和代码入口公开；依赖具体 Blender 版本及 VLM/图像模型。

### 4.6 The Scene Language

- **元数据**：Zhang et al.，2024/2025；[arXiv:2410.16770](https://arxiv.org/abs/2410.16770)。
- **任务**：从文本或图像推断可控 3D/4D scene representation，并由传统、神经或混合 renderer 渲染。
- **表示**：三部分 Scene Language：层级/关系程序、实体语义词、实体视觉 identity embeddings。
- **反馈**：以预训练模型推断和 renderer 验证为主，不是完整执行错误—修复 agent。
- **数据**：多类图像/场景输入与生成设置。
- **评测**：结构、语义、身份保持、渲染质量和可编辑性。
- **Finding**：程序负责结构，词负责类别，embedding 负责外观身份，提供了连接代码场景与神经渲染的分层表示。
- **Limitations**：程序是否能映射到成熟 DCC/游戏引擎及其交互/物理语义，仍弱于 Blender/UE 原生脚本系统。
- **可复现性**：论文明确；采用前需核实官方代码与模型权重的完整发布情况。

## 5. Background：程序化生成与可执行渲染底座

### 5.1 Infinigen / Infinigen Indoors

- **元数据**：Raistrick et al.，CVPR 2023/2024 及后续室内扩展；[源码](https://github.com/princeton-vl/infinigen)。
- **任务**：用 Blender 程序化生成无限、多样、可渲染的自然/室内世界及视觉真值。
- **表示**：Python、Geometry Nodes、Shader Nodes、程序化资产/材质/布局。
- **反馈**：确定性执行、几何/可见性约束与渲染；本身不是 LLM critique-repair agent。
- **数据**：代码即数据生成器，可输出 RGB、depth、normal、segmentation、flow 等。
- **评测**：逼真度、多样性、视觉任务合成数据效用与性能。
- **Finding**：为 Scene Co-pilot、3DCodeBench 等提供高质量程序分布和可执行渲染环境。
- **Limitations**：作者程序开发成本高、生成重；API/节点复杂，正是 LLM agent 需要解决的可用性问题。
- **可复现性**：大型官方开源工程，环境、Blender 版本、缓存和硬件要求较高。

### 5.2 ProcTHOR / AI2-THOR

- **元数据**：Deitke et al.，2022；[AI2-THOR](https://github.com/allenai/ai2thor)，[ProcTHOR](https://github.com/allenai/procthor)。
- **任务**：程序化生成大规模、可交互室内环境，用于 embodied AI。
- **表示**：结构化房屋、房间、资产、放置和交互属性；在 Unity/AI2-THOR 执行。
- **反馈**：碰撞、可达性、交互规则和 embodied task rollout。
- **数据**：大量程序化房屋与交互对象。
- **评测**：导航/交互智能体在程序化环境中的泛化。
- **Finding**：Holodeck 将 LLM 常识与其硬约束/交互资产结合，说明成熟 simulator schema 是场景 agent 的关键接口。
- **Limitations**：域与资产集合固定；视觉/几何风格与现实仍有差距。
- **可复现性**：官方开源、文档成熟，是 embodied scene generation 的稳定底座。

### 5.3 BlenderProc

- **元数据**：Denninger et al.，2019 起持续维护；[源码](https://github.com/DLR-RM/BlenderProc)。
- **任务**：脚本化 Blender 合成数据生成、资产加载、随机化、物理放置、渲染和标注。
- **表示**：模块化 Python pipeline/config，直接控制 Blender。
- **反馈**：执行错误、物理和渲染输出；无原生 LLM critic。
- **数据**：面向 CV 的 RGB/depth/normal/segmentation/pose 合成数据。
- **评测**：更多是工程可靠性与下游视觉任务，不是语言生成质量。
- **Finding**：适合作为安全执行器、标准 renderer 和 ground-truth 采集层，能缩短构建 Blender agent harness 的工程路径。
- **Limitations**：创作自由度与 Blender API 同样带来版本/上下文问题；需自行增加 agent、sandbox 和 verifier。
- **可复现性**：开源成熟、容器化支持较好。

### 5.4 Kubric

- **元数据**：Greff et al.，CVPR 2022；[源码](https://github.com/google-research/kubric)。
- **任务**：用 Blender + PyBullet 生成带完美标注的复杂视频数据。
- **表示**：Python 场景/物理/相机/灯光程序。
- **反馈**：物理执行和多通道渲染，无 LLM 闭环。
- **数据**：可生成 MOVi 等对象运动、碰撞和分割视频。
- **评测**：下游视频理解/对象分解任务。
- **Finding**：提供“代码 → 物理动态场景 → 视频 + 真值”的清晰范式，是动态代码生成和 4DCodeBench 类工作的先导底座。
- **Limitations**：项目维护节奏与依赖版本需核实；真实感和复杂角色动画不是重点。
- **可复现性**：源码公开，适合受控物理视频任务。

## 6. 开源系统补充清单（论文外工程信号）

这些项目可用于实现 agent harness，但没有与上述论文同等强度的同行评审证据，适合工程参考而非学术结论：

- [BlenderGPT](https://github.com/gd3kr/BlenderGPT)：自然语言生成并执行 Blender 指令/代码；是 SceneCraft 的直接工程基线。
- [BlendHarness](https://github.com/cccky0813/BlendHarness)：headless Blender sandbox、Coder/Critic/Verifier、错误作为 observation、结构 diff、成本与步骤预算。
- [blender-agent-studio](https://github.com/ifBars/blender-agent-studio)：可编辑 `.blend` 与 Python，多视图检查、重新打开文件验证导出持久性。
- [blenderwright](https://github.com/HoldMyBeer-gg/blenderwright)：MCP 工具、快速 viewport feedback、mesh quality report、auto-critique；默认限制 raw Python。
- [better-blender-mcp](https://github.com/marlonka/better-blender-mcp)：强调 build–inspect–repair–rerender 与证据回传。
- [LLM-Blender-Agent](https://github.com/saofund/LLM-Blender-Agent)：function calling 驱动 Blender 自动化。
- [LLMUnity](https://github.com/undreamai/LLMUnity)：Unity 内本地/远程 LLM、RAG 与角色交互；偏 NPC，但可作为 Unity agent 通信层。

工程项目的共同启示是：**长驻无头进程 + watchdog、隔离 sandbox、场景重置、执行超时、保存/重开验证、固定多视图、结构 diff、mesh lint、调用追踪和预算控制**，往往比更复杂的 prompt 更能提高可靠性。

## 7. 建议的统一评测协议

面向 `awesome-code-generated-video`，建议把新系统统一拆成六层，避免只报“看起来不错”的 demo：

1. **代码层**：parse/compile rate、首次执行率、异常类型、危险 API、版本兼容、平均修复轮数。
2. **场景层**：对象/部件召回，层级、命名、transform、空间关系、碰撞、穿插、接触、可达性、非目标编辑。
3. **外观层**：多视图 DINO/SigLIP、材质/灯光/构图、人类偏好；必须包含固定 canonical views，不能只用最佳视角。
4. **动态层**：轨迹、速度/加速度、接触事件、时间顺序、身份持续、物理约束与关节范围。
5. **引擎层**：保存后重开、运行时行为、play-test、帧率、崩溃/超时、随机种子复现。
6. **代理层**：token/API/渲染成本、步骤数、成功率随预算曲线、工具错误恢复、critic 的 precision/recall、人工介入次数。

推荐报告三种 setting：

- **Single-shot**：只生成一次，用于测基础代码能力；
- **Execution-only repair**：仅给 traceback/结构检查，区分代码正确性；
- **Full multimodal loop**：加入多视图/视频 critic，测端到端创作能力。

还应保留以下 artifact：原始 prompt、每轮代码 diff、stdout/stderr、引擎版本、随机种子、场景文件、固定视角渲染、最终视频、结构化评分和完整 tool trace。

## 8. 对新仓库的技术路线建议

### 8.1 最小可行闭环

```text
Prompt / Reference Image / Video
  → Planner（生成 typed scene spec）
  → Coder（生成或 patch Blender Python）
  → Sandboxed Executor（固定 Blender 版本）
  → Structural Verifier（对象、关系、碰撞、动画、相机）
  → Multi-view / Video Renderer
  → VLM Critic（引用 verifier 证据，输出 typed issues）
  → Repairer（最小 diff，而非全量重写）
  → Save + Reopen + Final Render
```

优先把硬约束放入工具/验证器：对象命名唯一、关键帧范围、相机存在、渲染输出非空、接触/穿插阈值、禁止文件/网络/子进程 API、超时重启。VLM 只负责难以形式化的语义、构图和风格，不负责判断可由程序精确测量的事实。

### 8.2 表示选择

- **短期**：typed JSON scene spec + 受限 `bpy` patch API；兼顾表达力和安全。
- **中期**：引入关系算子（align、support、inside、contact、look-at）与 animation primitives，让 solver 处理坐标。
- **长期**：scene program 同时编译到 Blender（高质量离线渲染）和 UE/Unity（实时交互），并保留 USD/glTF/关节元数据作为交换层。

### 8.3 优先研究空白

1. **可验证 procedural animation**：目前资产/静态布局远多于复杂骨骼、接触和群体动作代码生成。
2. **跨镜头持久世界**：镜头之间资产、状态、时间和叙事约束的统一程序表示仍少。
3. **critic 校准**：量化 VLM 对 3D 关系、遮挡、背面错误和动画异常的检出率，而非默认 critic 正确。
4. **修复局部性**：评价修一个问题时破坏多少无关对象/关键帧；Code4Scene 的 artifact integrity 可直接借鉴。
5. **可复现成本曲线**：在固定 token、工具步数、渲染时间下比较成功率，避免无上限重试。
6. **从视频到程序再到视频**：结合 4DCodeBench 的 inverse graphics 与 GS-Agent/GEST 的 forward simulation，形成真正的 render-and-repair 训练数据闭环。

## 9. 参考入口

### 论文与项目

- [SceneCraft](https://arxiv.org/abs/2403.01248)
- [3D-GPT](https://arxiv.org/abs/2310.12945)
- [LL3M](https://arxiv.org/abs/2508.08228)
- [aDSL / Agentic 3D Creation](https://arxiv.org/abs/2608.17975)
- [SceneCode](https://arxiv.org/abs/2605.19587)
- [Nova3D](https://arxiv.org/abs/2607.22738)
- [BlenderLLM](https://arxiv.org/abs/2412.14203)
- [GS-Agent](https://arxiv.org/abs/2607.21522)
- [GPT4Motion](https://arxiv.org/abs/2311.12631)
- [AutoUE](https://arxiv.org/abs/2603.07106)
- [UnrealLLM](https://aclanthology.org/2025.findings-acl.994/)
- [Authoring for Living Worlds](https://arxiv.org/abs/2604.10383v4)
- [Cutscene Agent](https://arxiv.org/abs/2604.25318)
- [3DCodeBench](https://arxiv.org/abs/2606.01057)
- [Code4Scene](https://arxiv.org/abs/2609.36777)
- [4DCodeBench](https://arxiv.org/abs/2610.03715)
- [Holodeck](https://arxiv.org/abs/2312.09067)
- [RoboGen](https://arxiv.org/abs/2311.01455)
- [FilmAgent](https://arxiv.org/abs/2501.12909)
- [Scene Co-pilot](https://arxiv.org/abs/2411.18644)
- [BlenderAlchemy](https://arxiv.org/abs/2404.17672)
- [The Scene Language](https://arxiv.org/abs/2410.16770)

### 边界说明

本清单刻意没有系统性收录 DreamFusion、Magic3D、Text2NeRF、普通 3D diffusion/3DGS world generation 等工作：它们虽然可能产生可渲染内容，但若不输出可执行场景/脚本、引擎原生状态或不能直接支撑结构化视频渲染闭环，就不属于本文核心范围。