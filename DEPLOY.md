# 部署上线指引

## 当前托管现状（2026-10-09 定）

- **代码主仓**：Gitee https://gitee.com/paul-sun/zxblog （remote `origin`）
- **日常更新**：`git add . && git commit -m "..." && git push` 即可
- **站点发布**：⚠️ Gitee Pages 已于 2024 年停止服务，推送到 Gitee **不会**自动发布站点；
  `.github/workflows/deploy.yml` 仅在推送到 GitHub 时生效，对 Gitee 无效
- 发布渠道二选一（详见下文）：Cloudflare Pages（CLI 手动发布）或 GitHub 双推（全自动发布）

## 方案 A：Cloudflare Pages（不依赖 GitHub）

1. 注册 https://dash.cloudflare.com （免费）
2. `npx wrangler login` 浏览器授权一次
3. 发布 = 构建 + 上传：`npm run docs:build && npx wrangler pages deploy docs/.vitepress/dist --project-name zxblog`
4. 之后每次更新重跑第 3 步（可包成 npm script）

## 方案 B：GitHub 双推（全自动，推荐）

1. 注册 GitHub → 建空仓 `zxblog`（Public，不勾初始化文件）
2. `git remote add github https://github.com/<用户名>/zxblog.git && git push -u github main`
3. GitHub 仓库 Settings → Pages → Source 选 **GitHub Actions**
4. `docs/.vitepress/config.mts` 的 `base: '/zxblog/'` 已与仓库名一致，无需改
5. 之后日常：`git push` 推 Gitee + `git push github main` 推 GitHub，GitHub 侧自动发布
   （可设 `git remote set-url --add --push origin <github-url>` 让一次 push 同时推两边）

---

以下为原 GitHub Pages 全自动流程（方案 B 的展开说明）：

## 0. 前置

- GitHub 账号（没有就去 github.com 注册）
- 本机 git 已配置（`git config --global user.name` / `user.email` 有值）

## 1. 在 GitHub 上建仓库

- 仓库名已定 `zxblog`（网址会是 `https://<用户名>.github.io/zxblog/`）
- 想让博客直接挂在 `https://<用户名>.github.io/` 根路径，仓库名就用 `<用户名>.github.io`（不推荐：根域名留给个人主站）
- 其余选项默认（Public、不加 README）即可

## 2. 本地推送

```bash
cd /d/selfFiles_warehouse/blog
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

- 仓库名 `zxblog` → `https://<用户名>.github.io/zxblog/`
- 仓库名 `<用户名>.github.io` → `https://<用户名>.github.io/`

> 本项目仓库名已定为 `zxblog`，`docs/.vitepress/config.mts` 已配置 `base: '/zxblog/'`。
> 若日后改用根路径仓库名，需删除该 `base` 行，本地 dev 地址也会从 `/zxblog/` 变回 `/`。

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
