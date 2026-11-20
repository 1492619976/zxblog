---
title: "NomiFun 工作台 vs DSH（装了插件的）对比"
---

# NomiFun 工作台 vs DSH（装了插件的）对比

> 2026-11-05 应问整理。DSH 架构细节引用 **Agent-Harness架构模式**（五模式，2026-08 提炼）不重讲；NomiFun 细节见 [2026-11-05-三开源项目解读-nomifun-muopt-qOntology](./2026-11-05-三开源项目解读-nomifun-muopt-qOntology.md) 与配套 HTML。

## 一句话

NomiFun = 垂直整合"整机产品"（65 crate 全家桶，能力长在产品里）；DSH 装插件 = 微内核"插件树"拼出的工作站（agent loop/模型适配器/会话日志本身都是插件皆可替换）。能力面能拼得像，哲学/扩展点/安全流派完全不同。

## 对照

| 维度 | NomiFun | DSH 装插件 |
|---|---|---|
| 内核 | 特权组合根 nomifun-app(19.7万行)+唯一官方 runtime，核心不可换 | 无特权内核，一切插件可配置替换 |
| 扩展 | 外挂协议层（MCP/技能/渠道），核心不动 | 插件树+patch（bundle→profile→用户 patch 后写胜），可换循环本身 |
| 能力来源 | 第一方内置（17 技能编译进二进制/gateway 15+ 能力域/CDP/伙伴/机器人） | 生态插件按需挂（dsh-base+web-app 或 headless） |
| 工具安全 | **能力票据流派**：scope+TTL+签名 claim+四级权限（事前授权） | **流程管线流派**：pre-execute→guard 单调否决→execute→post-execute（事中监督） |
| 会话真源 | canonical Session/Turn/Event/Effect 存储 | 日志即真源（append-only 流+deriveMessages 投影+运行时断言） |
| 多 Agent | DAG 引擎+硬上限(16/64/128)+preset 不可变 Revision | subagent 缝（可委派他产品）+实验 Agent Teams |
| 形态 | Tauri 桌面+Web 双宿主，免费模型目录 | npx 起 3080 Web UI / headless；开发者预览 |
| 面向 | 终端用户开箱即用 | 开发者二次组合 |

## 三个关键区别

1. **互补而非替代**：dsh 装齐插件能力面接近 NomiFun，但拼不出桌面整合（伙伴窗/computer use/实体机器人/IM 渠道）、产品化（免费模型目录/AutoWork boot-resume/backup）与 Rust 单机性能；NomiFun 给不了 dsh 的可替换性（fs+subprocess 指向远程沙箱则 Bash/PTY/LSP 整体迁移；换 agent loop 不可能）。
2. **工具安全两流派可合并**：票据定权（capability）+管线把关（pre/guard/post）= 自研轻量中台工具层的满分结构，也是"Agent 工具安全"的答题骨架。
3. **分工价值**：dsh 抄框架设计（五模式 Python 降维复刻成本低，正好用作自研中台 agent 层骨架）；NomiFun 抄工程化（1.3万测试/check边界脚本/能力总线/双宿主/boot-resume）。dsh 教做可组合框架，NomiFun 教做敢交付的产品，作品集两样都要。

## 关联

- **Agent-Harness架构模式**（dsh 五模式 + pi 交叉验证）
- [2026-11-05-三开源项目解读-nomifun-muopt-qOntology](./2026-11-05-三开源项目解读-nomifun-muopt-qOntology.md)
- **2026-11-05-nomifun-desktop架构解读**（HTML，五场景映射）
