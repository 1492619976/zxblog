---
title: "Data Agent 落地方法论六议题解读（ThinkingAI Summit 2026）"
---

# Data Agent 落地方法论六议题解读（ThinkingAI Summit 2026）

> 2026-10-21 用户贴来六条议题标题 + 结论句"Data Agent落地方法论：Harness工程+记忆管理+取数Skill！"。出处已锁定：**ThinkingAI Summit China 2026** 峰会议题推介版（邀请函把议程改写成带钩子的标题），**2026-10-28（周三）13:30 北京·瑞吉酒店**，线下。

## 一、六条标题 ↔ 实际议程对照

| 推介标题 | 实际议程/来源 | 讲者 |
|---|---|---|
| Agentic Engine：让 Agent 能感知、能理解、能行动 | "Agentic Engine：开箱即用的企业级 Agent——从发现业务问题，到持续验证的增长" | 周津（ThinkingAI CTO） |
| Creator Harness + Soul Agent 的仿生世界架构 | "Livo：从'生成内容'走向'仿生世界'" | 吴庶宸（快看世界 Livo AI 算法负责人） |
| 基于知识库+取数Skill的归因分析实践 | "携程酒店的数据智能 Agent 实践" | 俞恺（携程数据总监） |
| 基于 Harness+记忆+Skill 的 Data Agent 实践 | 同上（携程场的内容概括） | 同上 |
| 如何基于语义层+Skill+知识库让 Agent 更懂业务？ | 推介文概括句，贯穿携程/平台场 | — |
| 企业级 Agent 如何跑进每个业务部门？ | 圆桌"从产品到组织，企业级 Agent 如何跑进每个业务部门" | 王博（甲子光年）主持，钱瀚（理想汽车大数据）等 |

峰会另有：卓动科技多Agent客服、星云AI短剧、货拉拉增长闭环。主办方 ThinkingAI（思考家）：数据智能领域十年、1500+ 企业客户，2026-04 发布 Agentic Engine（与华为云 MaaS 共建，信通院可信 AI 评测 4+ 级）。

## 二、三篇公开锚点（干货现在就能读，不必等会后纪要）

1. **快看 Livo 专访**（搜狐时间线 2026-09-07，InfoQ 陈姚戈 × 杨超）——本场"仿生世界"讲题的底料：World Agent（日程/事件/天气/运势）+ Soul Agent（聊天/"活着"/"照见"/执笔者子Agent）+ 每角色独立 Agent（一个故事 20+ NPC）；**Creator Harness = 创作者只写人物小传/剧本，系统抽出六层人格**（意识、需求、信念、思考方式=稳态；状态、情绪=动态）注入角色 Agent；200+ 节点，心智模型 128 维激活 32（类 MoE）；评测先行 60%→SFT 80%→98% 目标；数据飞轮 + Bad Case 收集。
2. **Agentic Engine 发布**（36氪 2026-04-20）——"能感知、能理解、能行动"话术源头；1500+ 客户、华为云共建、信通院 4+ 级；BI/分析厂商集体转 Agent 的又一例证。
3. **取数→归因的 Data Agent 演进**（InfoQ《从AI取数到智能分析》）——"知识库+取数Skill归因"的公开同款内容：OLAP 真实场景 Text-to-SQL 准确率从纸面 90% 骤降；五步归因 Skill（指标下钻拉时间序列→按国家/品类/渠道多维拆解→…）；五次跃迁（单链路RAG→Multi-Agent+渐进披露→个性化画像/记忆→语义模型+Text-to-DSL→Sandbox/文件系统+Skill）；Skill 三大价值=可复用/可信赖（流程不可跳过、中间步骤可追溯）/可扩展；元数据治理 ROI：AI生成描述70%直接采纳、单表治理30→10分钟、人工治理2000张核心表血缘扩散覆盖15万+张、找表准确率+15pp。

## 三、与库内已有笔记的关系

**同源不重讲**：
- Harness 工程定实际水平 → **小米DataAgent生产落地实践-解读**（拉开差距的不是模型而是 Harness）、**DataAgent从入门到精通手册-解读**
- Skill 机制：快手电商 DataAgent 实践（研发包 Skill 化）与 Skill 三级渐进披露（Q7）互为印证
- 语义层是地基 → [2026-10-21-DataAgent落地七问题与语义稿方案解读](./2026-10-21-DataAgent落地七问题与语义稿方案解读.md)、[2026-10-20-DataAgent深度调研报告2026版解读](./2026-10-20-DataAgent深度调研报告2026版解读.md)
- 评测驱动 → 小米评测 Loop

**真增量三块**：
1. **记忆管理**——三件套里库内最薄一环。快看记忆系统设计可作方案参考骨架：记忆=推荐系统（"该想起什么"类 MoE 激活）、VDB 存事实 + GDB 存长程因果（呼应/因果/回响三类边）、重要性衰减+遗忘；对照 AWS《Agent记忆系统的工程实践与演进》（Data for AI 系列第三篇）。B 端 Data Agent 记忆（口径确认/常用表/用户画像，InfoQ Shopee 版）与 C 端陪伴记忆（心智模型分层）分两层记。
2. **Harness 概念跨域泛化**——快看把 Harness 用到内容/角色域（Creator Harness），"Harness=模型外的一切工程壳"最生动的第二例证（第一例=LangGraph≈Kettle .kjb 锚定，见尚硅谷费曼解读 campaign）。
3. **厂商/市场情报**——ThinkingAI（十年数据智能、1500+ 客户）转 Agent 平台 + 快看（内容公司）用同一套 Harness/Skill/记忆词汇——跨行业共识形成中，售前"数据消费主体从人变 Agent"（**本体驱动的AI数据管理-解读**）再添两例。

## 四、结论句判读

"落地方法论=Harness工程+记忆管理+取数Skill"没有新东西，是已有实证的压缩版：Harness 管确定性（执行/权限/上下文/评测），记忆管长期一致与个性化，取数 Skill 管专家流程资产化——三层全在"模型外工程"，与库内结论"模型定上限、工程定实际水平"同构。价值在"记忆管理"被提到与 Harness/Skill 并列的第一公民位置，正好暴露库内空白。

## 来源

- 峰会议程：thinkingai.cn/event/thinkingai-summit-china-2026
- 快看 Livo：timeline.sohu.com/news/o4vkOJDqRl
- Agentic Engine：36kr.com/p/3774850764030472
- 取数→归因：infoq.cn/article/LfO7mzdhxMWTtICFuTNb
- AWS 记忆系列：aws.amazon.com/cn/blogs/china/agent-system-engineering-practice
