---
title: "LLM Wiki 与 Ontology 区别"
---

# LLM Wiki 与 Ontology 区别

**一句话**：LLM Wiki 是写给 LLM 读的活笔记，语义靠模型当场理解；Ontology 是写给机器推理的形式化地基，语义写死在结构里。互补，不是替代。

## 核心分野

| 维度 | LLM Wiki | Ontology |
|---|---|---|
| 载体 | Markdown 页 + **wiki链接** | 三元组：类/属性/公理（OWL·RDF·SHACL） |
| 语义在哪 | 模型运行时解释（概率性） | 结构内形式化定义（确定性） |
| 推理方式 | 检索+LLM 理解，可能漏、可能编 | 推理机/SPARQL 演绎，结论可证明 |
| 一致性 | 无保证，靠 lint 巡检兜底 | 一致性检查+SHACL 校验，冲突即报 |
| 建设成本 | 低：写笔记即建设 | 高：需专职建模（AI 辅助可降） |
| 擅长 | 隐性知识、踩坑、口径故事 | 跨系统对齐、机器校验、grounding |

## 两条消费链路

- Wiki：提问 → 检索（相似度+显式链接）→ LLM 读文本 → 答案（语义在模型脑内）
- 本体：提问 → SPARQL/推理机 → 公理演绎 → 结论（语义在结构里）

## 混合趋势（谁也吃不掉谁）

- LLM 建本体：qOntology 四轮对话建模，门槛从本体工程师降到会聊天 → [2026-11-05-三开源项目解读-nomifun-muopt-qOntology](./2026-11-05-三开源项目解读-nomifun-muopt-qOntology.md)
- 本体喂 LLM：形式化模型做 grounding，确定性 37%→98% → [2026-11-05-Agent五问全网解答](./2026-11-05-Agent五问全网解答.md)
- 何明璐比喻：Wiki 是给数据，Ontology 是给地基
- 本体技术栈：Protege 编辑 / RDF4J 存储 / qOntology AI 建模 → [2026-11-05-本体双开源解读-Protege与RDF4J](./2026-11-05-本体双开源解读-Protege与RDF4J.md)

## 自己的轨迹

wiki 范式适合记经验（容忍模糊、找得到就行）；本体走工程项目线（地基、对齐、机器可判）。两条线不冲突：**记经验、容忍模糊 → Wiki；跨系统对齐、要机器可判 → Ontology**。

