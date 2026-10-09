# my-learning-blog

个人学习博客（VitePress + GitHub Pages）：记录 2026-10 → 2027-03 转职 AI+大数据方向的学习全过程。

## 常用命令

```bash
npm run docs:dev      # 本地开发预览 http://localhost:5173
npm run docs:build    # 构建（死链会让构建失败，是好事）
npm run docs:preview  # 构建产物本地预览 http://localhost:4173
```

## 从 Obsidian 导入笔记

```bash
py -3 tools/import_notes.py scan     # 扫描 02-学习，生成 tools/candidates.txt
# 编辑 candidates.txt，取消注释想发布的行
py -3 tools/import_notes.py import   # 转换导入 + 自动更新侧边栏
```

- 转换：`[[wiki链接]]`→相对链接（解析不到转纯文本）、图片自动复制到 `public/images/`、剥离个人 frontmatter
- 内容源硬编码为 Obsidian 库的 `02-学习\`，脚本会拒绝该目录之外的任何路径（工作内容不上公网的红线兜底）
- 明细见 `tools/import_report.txt`

## 目录结构

```
blog/
├─ docs/               # 站点内容
│  ├─ .vitepress/
│  │  ├─ config.mts    # 站点配置（站名/导航/搜索）
│  │  └─ sidebar.gen.ts# 侧边栏（导入脚本自动生成）
│  ├─ java/ bigdata/ python-ai/ governance/ methodology/
│  ├─ weekly/          # 学习周记（手写，每周一篇）
│  ├─ about/           # 关于我
│  └─ public/          # 静态资源（图片自动落 public/images/）
├─ tools/import_notes.py
├─ .github/workflows/deploy.yml   # push 到 main 自动发布
└─ DEPLOY.md           # 上线操作指引
```

上线/更新步骤见 [DEPLOY.md](./DEPLOY.md)。
