# 部署上线指引（GitHub Pages）

全程免费，不需要服务器。首次约 10 分钟。

## 0. 前置

- GitHub 账号（没有就去 github.com 注册）
- 本机 git 已配置（`git config --global user.name` / `user.email` 有值）

## 1. 在 GitHub 上建仓库

- 仓库名建议 `blog`（网址会是 `https://<用户名>.github.io/blog/`）
- 想让博客直接挂在 `https://<用户名>.github.io/` 根路径，仓库名就用 `<用户名>.github.io`
- 其余选项默认（Public、不加 README）即可

## 2. 本地推送

```bash
cd /d/blog
git init
git add .
git commit -m "init: 学习博客上线"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

> package-lock.json 必须一起提交——线上部署用 `npm ci`，没有锁文件会失败。

## 3. 开启 Pages

1. 打开仓库页面 → **Settings** → 左侧 **Pages**
2. **Build and deployment** → **Source** 选 **GitHub Actions**
3. 回到 **Actions** 标签页，能看到 "Deploy VitePress site to Pages" 在跑，等它变绿

## 4. 访问

- 仓库名 `blog` → `https://<用户名>.github.io/blog/`
- 仓库名 `<用户名>.github.io` → `https://<用户名>.github.io/`

> 本项目仓库名已定为 `blog`，`docs/.vitepress/config.mts` 已配置 `base: '/blog/'`（2026-10-09 提交 4de48fc）。
> 若日后改用根路径仓库名，需删除该 `base` 行，本地 dev 地址也会从 `/blog/` 变回 `/`。

## 5. 以后的日常更新

```bash
# 写/改 docs 下的 md，或跑 tools/import_notes.py 导入新笔记之后：
git add .
git commit -m "更新：xxx"
git push
```

推送即自动发布，什么都不用再做。

## 6.（可选）自定义域名

1. 买域名（.icu / .dev 首年 10~30 元）
2. DNS 加 CNAME 记录指向 `<用户名>.github.io`
3. 仓库 Settings → Pages → Custom domain 填域名，勾选 Enforce HTTPS

## 常见问题

| 现象 | 处理 |
|------|------|
| Actions 红叉 | 点进失败的那次运行看日志，最常见是 md 里有死链（build 会报 dead link） |
| 页面 404 / 无样式 | 子路径部署没配 `base`，见第 4 节提示 |
| 图片不显示 | 图片必须在 `docs/public/` 下，引用路径以 `/` 开头（导入脚本已自动处理） |
