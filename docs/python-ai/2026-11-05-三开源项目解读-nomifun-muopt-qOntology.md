---
title: "三开源项目解读：nomifun-desktop / muopt / qOntology"
---

# 三开源项目解读：nomifun-desktop / muopt / qOntology

> 2026-11-05 源码解读，三个仓库已 clone 到本地同名目录，三个并行探索 agent 深挖后汇总。

## nomifun-desktop — 本地优先 AI 工作站（抄架构）

> 配套图解：nomifun-desktop 架构解读（HTML，含五场景应用映射与可抄清单）

- Tauri 2 + Rust 2024 + React 19；**Rust 110 万行/65 crate + TS 37 万行**，中文开源 Agent 桌面工程化天花板
- 架构：一份 `nomifun-app` 组合根（axum ~400 路由）双宿主复用——Tauri 壳进程内嵌（随机端口+本地信任 token+fetch 拦截器注入）与 Web 宿主（JWT+CSRF）零分叉
- 分层：`nomi-*`（Agent 引擎原语，不依赖业务）与 `nomifun-*`（业务域）隔离；chat-model-broker=唯一模型重试/故障转移权威；AgentExecution=Planner→DAG→Scheduler（16模型/64参与者/128步硬上限）
- MCP：完整 OAuth PKCE + 8 个第三方 Agent CLI 适配器（Claude/Codex/Gemini/Qwen…）；17 内置技能 `include_dir!` 编译进二进制启动物化
- **能力总线**：工具调用走带作用域/签名/租约的 capability claim，签名根不落子进程
- 伙伴成长：SQLite+FTS5 记忆（-bm25+importance*0.5+strength*0.5 排名）+ 事件流 JSONL + EvolutionEngine 60s tick 自动挖模式起草 SKILL.md（挖矿→起草→评审→人工采纳）
- 质量：13370 Rust 测试+910 前端测试；20+ `check:*` 脚本强制架构边界防旧代码回流
- 不足：nomifun-app 19.7 万行巨型组合根、wave1~5 按施工波次命名、pre-1.0 破坏性升级退役数据集
- 对我：DataAgent 平台工程参考——能力总线签名/技能物化/模型路由合同/双宿主

## muopt（沐优）— 内网 SQL 优化+信创转换（抄细节）

> 配套图解：`BaiduSyncdisk/解读文档/muopt沐优胜品图解-源码解读与工作结合.html`（含结合工作四档拆解：直接用/借机制/作品集叙事/边界警示 + 5 题自测）

- Spring Boot 3.2 单体 59 类 1.1 万行，单 jar 进内网；MIT；18 方言
- 索引建议（`IndexAnalyzerService`）：JSqlParser AST；OR 两侧只作独立范围候选、LIKE 前缀才算；等值前+范围后拼组合索引；连库后 `DatabaseMetaData.getIndexInfo` 最左前缀匹配分橙（待建）/灰（已有）
- **SqlConverter(1658行) 刻意不用 AST**（toString 重排毁格式/含 `#{}` 必挂/无字符偏移无法按位写回）→ 保形转换三步：字面量掩码（字符串/注释/MyBatis 占位符遮住）→ 函数映射 → **类型槽位白名单**（只换 CREATE TABLE/CAST/`::`/ALTER 位置的类型词，防列名 text 被改 CLOB）；日期格式串 `%Y↔YYYY` 逆表按长度降序防 HH24 抢匹配；"宁可漏改不猜"
- 写回安全五重闸：路径规范化防穿越+占位符丢失即终止+`.bak` 字节级备份+GBK 严格写回（写不进抛错不毁文件）
- AI 降级链：失败/超时/截断（finish_reason=length）→ 本地规则（逗号连接→JOIN、HAVING 下移）；AI 输出 sanitize 白名单（非 ASCII 只允许原文已有中文、长度≤3x+200）
- 不足：45 测试全在安全/工具类，**SqlConverter 零测试**；默认口令弱（内网取舍）
- 对我：与生产环境 Oracle 方言转换经验直接对口，"槽位白名单+字面量掩码+宁可漏改"三原则可搬进信创 SQL 改造工具化

## qOntology — 开源本体工程平台（抄思路+避坑）

- Spring Boot 3.5+Vue3，Java 13 万行；**本质=RuoYi 脚手架+芋道风格+本体业务层**；85 表（om_*/app_*/basic_*）
- 已实现：CQ 建模目标（om_target+两张关联表，"覆盖率"=SQL 计数非语义匹配）、术语/别名、对象类型树（parentId+ancestors）、约束=自研 om_model_axiom+om_data_rule（**非标准 SHACL**）
- **版本管理=整库快照克隆**：`IProjectRepeatable` 按 copyOrder 串行复制，ProjectCopyContext 维护新旧 ID 映射；无增量 diff（"版本比对"只是 count 统计）
- Turtle/RDF-XML 导出=手写字符串序列化（无 Jena/OWL API），枚举约束不生成
- **AI 建模流水线（3061 行，最有设计感）**：POI/PDFBox 解析→证据分块→**四轮 LLM**（round-1 CQ术语→round-2 对象→round-3 属性关系→round-4 公理规则，提示词 resources/prompts/ai-modeling/）→ 候选表（置信度+evidenceBlockNos 溯源+candidateKey 去重）→ **人工采纳落正式表**
- 图谱：自研 graphis 抽象（Neo4j/ArangoDB 双后端 MP 风格 wrapper）；结构化抽取 Redis 队列+Quartz 按映射灌图；非结构化=**导出 TTL 压缩成 JSON 塞提示词**抽三元组（建模→TTL→抽取闭环）
- **占位未实现**（showDeveloping 壳）：质量检查（循环继承/悬空关系零算法）、SHACL 导出（全源码无痕）、本体问答（setTimeout 模拟回复）、属性基数/默认值；业务模块零测试
- 对我：本体项目参照——AI 四轮流水线与快照克隆版本两条路可直接引用；"README 宣传 vs 源码实现"落差=讲差异化方案的对照素材

## 一句话

nomifun 抄架构（Agent 平台工程天花板）、muopt 抄细节（防御式小工具教科书）、qOntology 抄思路+避坑（本体平台宣传与实现落差活案例）。
