# zxblog

> 个人学习博客：边学边记，公开复盘。

🚧 线上地址部署中（GitHub Pages）

## 为什么公开写

1. 公开输出是最好的复习——写不清楚就是没学明白
2. 公开承诺是对抗拖延的杠杆
3. 希望同样在学习路上的朋友少走一点弯路

## 内容栏目

| 栏目 | 内容 |
|------|------|
| 📝 每日笔记 | 每个学习日一篇：今日所学 / 卡点与解决 / 明日计划 |
| ☕ Java | 从基础语法到并发与 JVM，逐层学习笔记 |
| 🌊 大数据 | Hadoop / Spark / Flink 生态与数仓建模 |
| 🐍 Python 与 AI | Python、LLM 应用、RAG 与 Agent 项目——本站主线 |
| 🧹 数据治理 | 数据标准、数据质量、元数据、指标体系 |
| 🧠 学习方法论 | 主动回忆、间隔重复、费曼技巧的实践验证 |
| 📅 学习周记 | 每周一篇：目标 / 进展 / 卡点 / 复盘，半年不断更 |

## 技术栈

- 站点：[VitePress](https://vitepress.dev/)（默认主题 + 中文本地全文搜索）
- 部署：GitHub Actions 自动构建发布
- 写作：笔记在 Obsidian 中管理，`tools/import_notes.py` 批量导入（wiki 链接、图片、frontmatter 自动转换）

## 本地预览

```bash
git clone https://gitee.com/paul-sun/zxblog.git
cd zxblog
npm install
npm run docs:dev     # http://localhost:5173/zxblog/
```

## 笔记导入（个人工作流）

```bash
# 内容源通过环境变量注入，脚本会拒绝源目录之外的任何路径
set BLOG_SOURCE_ROOT=<你的Obsidian库>/02-学习
py -3 tools/import_notes.py scan      # 扫描生成候选清单
py -3 tools/import_notes.py import    # 勾选后转换导入
```

## 更新节奏

- 每日笔记：每个学习日一篇当日所学
- 学习周记：每周一篇总结，汇总本周每日笔记
- 主题笔记：随学习进度沉淀到各栏目

## 许可

本站内容如无特别说明，均采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)（署名-非商业性-相同方式共享）。
