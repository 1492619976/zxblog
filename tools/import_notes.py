#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""import_notes.py — 从 Obsidian 知识库（02-学习）批量导入笔记到本博客

前置：设置环境变量 BLOG_SOURCE_ROOT=<你的Obsidian库>\02-学习（内容源，脚本只读该目录）

用法：
  py -3 tools/import_notes.py scan
      扫描候选笔记，打印分组统计，生成 tools/candidates.txt（全部注释状态）
  py -3 tools/import_notes.py import [--selection tools/candidates.txt] [--out docs]
      按选择清单导入（取消注释的行生效），重写 sidebar.gen.ts，
      输出 tools/import_report.txt

选择清单格式（每行一条，路径相对 02-学习，带不带 02-学习/ 前缀均可）：
  java学习/笔记A.md                 ← 用默认栏目映射
  数据智能学习/笔记B.md -> python-ai  ← 行尾覆盖栏目

转换规则：
  - [[链接]] / [[链接|别名]]：批次内可解析 → 相对 md 链接；解析不到 → **加粗纯文本**
  - ![[图片.png]] 嵌入 / ![](相对路径) 图片：找到就复制到 public/images/ 并改写；
    找不到 → 🖼️（图片未随迁：xxx），并记入报告
  - 原始 frontmatter 全部剥离，只保留 title（frontmatter title > 首个 H1 > 文件名）
  - 代码块（``` / ~~~）内的内容不动

安全红线（代码级兜底）：内容源硬编码为 02-学习 目录；
清单中任何指向该目录之外的路径一律拒绝导入。
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath

# 内容源通过环境变量 BLOG_SOURCE_ROOT 注入（不硬编码个人路径，脚本可公开分发）；
# 脚本只读取该目录，清单中任何指向目录之外的路径一律拒绝导入。
SOURCE_ROOT = Path(os.environ["BLOG_SOURCE_ROOT"]).resolve()
BLOG_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = BLOG_ROOT / "docs"

# 源目录名 → 栏目 key（与 docs/ 下目录、sidebar 对应）
SECTION_MAP = {
    "java学习": "java",
    "大数据学习": "bigdata",
    "PythonAI学习": "python-ai",
    "Python学习": "python-ai",
    "个人学习知识库": "python-ai",
    "数据智能学习": "python-ai",
    "数据库学习": "governance",
    "数据治理学习": "governance",
    "编程通用学习": "methodology",
    "学习方法论": "methodology",
    "学习工坊": "methodology",
    "学习工具": "methodology",
}

# 默认排除的目录名（可被清单显式选择覆盖——排除只是不进候选，不影响导入合法性）
EXCLUDE_DIRS = {
    "00-收件箱", "思维导图", "java课程包", "99_资料", "00-学习规划",
    "05-面试与岗位", "repo", "raw", ".git", ".obsidian", "node_modules",
    "__pycache__", ".trash",
}
IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}
WEEKLY_SECTIONS = {"java", "bigdata", "python-ai", "governance", "methodology"}

WIKI_EMBED = re.compile(r"!\[\[([^\[\]]+?)\]\]")
WIKI_LINK = re.compile(r"\[\[([^\[\]]+?)\]\]")
MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def iter_md_files():
    """遍历 02-学习 下的候选 md（应用默认排除规则）。"""
    for dirpath, dirnames, filenames in os.walk(SOURCE_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn.lower().endswith(".md") and not fn.startswith((".", "~")) and fn != "README.md":
                yield Path(dirpath) / fn


def section_for(rel: Path):
    top = rel.parts[0] if rel.parts else ""
    return SECTION_MAP.get(top)


def make_slug(stem: str) -> str:
    """文件名 → URL 友好 slug：空格和易冲突字符替换为 -，中文保留。"""
    s = re.sub(r"[\s()（）\[\]【】#]+", "-", stem).strip("-.")
    return s or "untitled"


def read_text(p: Path) -> str:
    for enc in ("utf-8", "gbk"):
        try:
            return p.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return p.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str):
    """返回 (title_or_None, body)。只取 title，其余个人元数据全部丢弃。"""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    for i in range(1, min(len(lines), 60)):
        if lines[i].strip() == "---":
            fm_block = lines[1:i]
            body = "\n".join(lines[i + 1:])
            title = None
            for ln in fm_block:
                m = re.match(r'^title:\s*(.+)$', ln.strip())
                if m:
                    title = m.group(1).strip().strip('"').strip("'")
                    break
            return title, body
    return None, text


def extract_title(stem: str, body: str, fm_title):
    if fm_title:
        return fm_title
    for ln in body.splitlines():
        if ln.startswith("# "):
            return ln[2:].strip()
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)


def yaml_safe(s: str) -> str:
    # JSON 字符串是合法 YAML 双引号标量，省去手工转义
    return json.dumps(s, ensure_ascii=False)


class Transformer:
    def __init__(self, out_root: Path, batch_stem2path: dict, report: list):
        self.out_root = out_root
        self.batch = batch_stem2path  # stem -> 目标 md 绝对路径
        self.report = report

    def find_image(self, name: str, src_md: Path):
        """在笔记所在目录及其上级（限 02-学习 内）就近找图。"""
        for base in [src_md.parent, src_md.parent.parent]:
            hits = list(base.rglob(name))
            if hits:
                return hits[0]
        return None

    def copy_image(self, src_img: Path, note_slug: str) -> str:
        dest_dir = self.out_root / "public" / "images" / note_slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src_img.name
        if not dest.exists() or dest.read_bytes() != src_img.read_bytes():
            shutil.copy2(src_img, dest)
        return f"/images/{note_slug}/{src_img.name}"

    def convert_line(self, line: str, src_md: Path, note_slug: str):
        # 1) 嵌入 ![[]]
        def embed_repl(m):
            inner = m.group(1).strip()
            target = inner.split("|")[0].split("#")[0].strip()
            ext = Path(target).suffix.lower()
            if ext in IMG_EXTS:
                img = self.find_image(target, src_md)
                if img:
                    url = self.copy_image(img, note_slug)
                    return f"![{Path(target).stem}]({url})"
                self.report.append(("缺图片", f"{src_md.name} → {target}"))
                return f"🖼️（图片未随迁：{target}）"
            if ext == ".md" or not ext:
                link = self.resolve_wiki(inner, src_md)
                return link if link else f"📎（嵌入未随迁：{target}）"
            return f"📎（嵌入未随迁：{target}）"

        line = WIKI_EMBED.sub(embed_repl, line)

        # 2) 普通链接 [[]]
        def link_repl(m):
            inner = m.group(1).strip()
            res = self.resolve_wiki(inner, src_md)
            if res is None:
                target = inner.split("|")[0].split("#")[0].strip()
                self.report.append(("降级链接", f"{src_md.name} → {target}"))
                return f"**{inner.split('|')[-1].split('#')[0].strip()}**"
            return res

        line = WIKI_LINK.sub(link_repl, line)

        # 3) 标准 md 图片 ![alt](path)——只处理相对本地路径
        def img_repl(m):
            alt, path = m.group(1), m.group(2)
            if path.startswith(("http://", "https://", "data:", "/", "#")):
                return m.group(0)
            img = src_md.parent / path
            if img.exists():
                url = self.copy_image(img, note_slug)
                return f"![{alt}]({url})"
            self.report.append(("缺图片", f"{src_md.name} → {path}"))
            return f"🖼️（图片未随迁：{path}）"

        line = MD_IMAGE.sub(img_repl, line)
        return line

    def resolve_wiki(self, inner: str, src_md: Path):
        """把 [[target|alias#h]] 解析成相对链接；失败返回 None。"""
        parts = inner.split("|")
        target = parts[0].split("#")[0].strip()
        alias = parts[1].strip() if len(parts) > 1 else ""
        stem = Path(target).stem if target.endswith(".md") else target
        dest = self.batch.get(stem)
        if not dest:
            return None
        text = alias or stem
        return f"[{text}]({_rel_link(src_md, dest)})"


def _rel_link(from_md: Path, to_md: Path):
    """跨栏目（兄弟目录）也要能算，所以用 os.path.relpath 而不是 relative_to。"""
    rel = os.path.relpath(to_md.parent, from_md.parent).replace("\\", "/")
    parts = PurePosixPath(rel).parts
    return "/".join(parts + (to_md.name,)) if parts != ("",) else f"./{to_md.name}"


def cmd_scan(args):
    groups = {}
    total = 0
    rows = []
    for f in iter_md_files():
        rel = f.relative_to(SOURCE_ROOT)
        sec = section_for(rel)
        top = rel.parts[0]
        lines = read_text(f).count("\n") + 1
        g = groups.setdefault(top, {"n": 0, "lines": 0, "sec": sec})
        g["n"] += 1
        g["lines"] += lines
        total += 1
        rows.append((rel.as_posix(), lines, sec))

    print(f"内容源：{SOURCE_ROOT}")
    print(f"候选 md 共 {total} 个（已默认排除：{'、'.join(sorted(EXCLUDE_DIRS))}；README.md 不计）\n")
    print(f"{'源目录':<20}{'默认栏目':<12}{'文件数':>6}{'总行数':>8}")
    for top in sorted(groups):
        g = groups[top]
        sec = g["sec"] or "⚠️未映射(需在清单行尾指定)"
        print(f"{top:<20}{sec:<12}{g['n']:>6}{g['lines']:>8}")

    sel = BLOG_ROOT / "tools" / "candidates.txt"
    sel.parent.mkdir(parents=True, exist_ok=True)
    with sel.open("w", encoding="utf-8") as fh:
        fh.write("# 导入选择清单 —— 想导入哪篇就取消那一行的注释（删掉行首的 # 和空格）\n")
        fh.write("# 默认栏目不合适时，在行尾加 -> 栏目key（可选：java bigdata python-ai governance methodology）\n")
        fh.write(f"# 由 scan 生成于 {datetime.now():%Y-%m-%d %H:%M}\n\n")
        cur = None
        for rel, lines, sec in sorted(rows):
            if rel.split("/")[0] != cur:
                cur = rel.split("/")[0]
                fh.write(f"\n# ===== {cur} → 默认栏目：{sec or '未映射'} =====\n")
            fh.write(f"# {rel}\n")
    print(f"\n完整清单已写入 {sel}（全部注释状态）——取消注释后再跑 import")


def parse_selection(path: Path):
    picked = []
    for raw in read_text(path).splitlines():
        ln = raw.strip()
        if not ln or ln.startswith("#"):
            continue
        m = re.match(r"^(.+?)(?:\s*->\s*(\S+))?$", ln)
        rel, sec = m.group(1).strip(), m.group(2)
        picked.append((Path(rel), sec))
    return picked


def cmd_import(args):
    out_root = Path(args.out).resolve()
    if not out_root.exists():
        sys.exit(f"输出目录不存在：{out_root}")
    sel_path = Path(args.selection).resolve()
    if not sel_path.exists():
        sys.exit(f"选择清单不存在：{sel_path}（先跑 scan）")

    picked = parse_selection(sel_path)
    # 红线兜底：逐条校验必须在 02-学习 之内
    legal = []
    for rel, sec in picked:
        rel_s = re.sub(r"^02-学习[/\\]", "", rel.as_posix())
        p = (SOURCE_ROOT / rel_s).resolve()
        if SOURCE_ROOT not in p.parents:
            sys.exit(f"红线拒绝：{rel} 不在 {SOURCE_ROOT} 内")
        if not p.exists():
            print(f"⚠️ 跳过（不存在）：{rel_s}")
            continue
        sec = sec or section_for(Path(rel_s))
        if sec not in WEEKLY_SECTIONS:
            print(f"⚠️ 跳过（栏目未映射，需行尾 -> 栏目key）：{rel.as_posix()}")
            continue
        legal.append((p, sec))
    if not legal:
        sys.exit("清单为空：编辑 candidates.txt，取消注释要导入的行")

    # 目标路径分配（同栏目重名加父目录前缀）
    used = {}
    plan = []
    for p, sec in legal:
        stem = make_slug(p.stem)
        if stem == "index":
            stem = make_slug(p.parent.name)
        key = (sec, stem.lower())
        if key in used:
            stem = make_slug(p.parent.name + "-" + p.stem)
        used[(sec, stem.lower())] = True
        plan.append({"src": p, "sec": sec, "stem": stem,
                     "dst": out_root / sec / f"{stem}.md"})
    batch = {item["src"].stem: item["dst"] for item in plan}

    report = []
    tf = Transformer(out_root, batch, report)
    for item in plan:
        text = read_text(item["src"])
        fm_title, body = split_frontmatter(text)
        title = extract_title(item["src"].stem, body, fm_title)

        out_lines = []
        in_fence = False
        for ln in body.splitlines():
            stripped = ln.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                out_lines.append(ln)
                continue
            out_lines.append(ln if in_fence else tf.convert_line(ln, item["src"], item["stem"]))

        item["dst"].parent.mkdir(parents=True, exist_ok=True)
        content = "---\ntitle: " + yaml_safe(title) + "\n---\n\n" + "\n".join(out_lines).strip() + "\n"
        item["dst"].write_text(content, encoding="utf-8")

        residue = sum(1 for l in out_lines if "[[" in l)
        print(f"✅ {item['sec']:<12}{item['dst'].name}"
              + (f"（残留[[×{residue}，见报告）" if residue else ""))

    gen_sidebar(out_root, plan)

    rep = BLOG_ROOT / "tools" / "import_report.txt"
    with rep.open("w", encoding="utf-8") as fh:
        fh.write(f"导入时间：{datetime.now():%Y-%m-%d %H:%M}\n")
        fh.write(f"导入文件：{len(plan)} 篇\n\n")
        fh.write("[降级/缺失明细]\n" + ("\n".join(f"{a}: {b}" for a, b in report) or "无") + "\n")
        fh.write("\n[未解析 wiki 链接→已转纯文本的，若目标笔记后续也导入，重跑一次 import 即自动变成链接]\n")
    print(f"\n报告：{rep}")
    print(f"下一步：npm run docs:build 验证 → git push 自动发布")


def gen_sidebar(out_root: Path, plan):
    by_sec = {}
    for item in plan:
        by_sec.setdefault(item["sec"], []).append(item)
    labels = {"daily": "每日笔记", "java": "Java", "bigdata": "大数据", "python-ai": "Python 与 AI",
              "governance": "数据治理", "methodology": "学习方法论", "weekly": "学习周记"}
    # daily / weekly 是手写栏目：重写时从现有文件原样保留其条目（总览除外）
    manual = {"daily": [], "weekly": []}
    gen_path = out_root / ".vitepress" / "sidebar.gen.ts"
    if gen_path.exists():
        old = gen_path.read_text(encoding="utf-8")
        for m in re.finditer(r"""\{ text: ([^\n]+?), link: ['"](/(?:daily|weekly)/[^'"]+)['"] \}""", old):
            sec = "daily" if m.group(2).startswith("/daily") else "weekly"
            if m.group(2) != f"/{sec}/":
                manual[sec].append((m.group(1), m.group(2)))
    lines = ["// 本文件由 tools/import_notes.py 自动生成，请勿手改", "export default {"]
    for sec, label in labels.items():
        items = [f'{{ text: {json.dumps("总览", ensure_ascii=False)}, link: "/{sec}/" }}']
        if sec in manual:
            items.extend(f'{{ text: {t}, link: "{l}" }}' for t, l in manual[sec])
        else:
            for it in sorted(by_sec.get(sec, []), key=lambda x: x["stem"]):
                first = [l for l in it["dst"].read_text(encoding="utf-8").splitlines()[:3] if l.startswith("title:")][0]
                title = json.loads(first.split(":", 1)[1].strip())
                items.append(f'{{ text: {json.dumps(title, ensure_ascii=False)}, link: "/{sec}/{it["stem"]}" }}')
        lines.append(f'  {json.dumps(sec)}: [')
        lines.append(f'    {{ text: {json.dumps(label, ensure_ascii=False)}, collapsed: false, items: [')
        lines.extend(f'      {it},' for it in items)
        lines.append('    ] },')
        lines.append('  ],')
    lines.append("}")
    (out_root / ".vitepress").mkdir(parents=True, exist_ok=True)
    (out_root / ".vitepress" / "sidebar.gen.ts").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Obsidian(02-学习) → VitePress 笔记导入")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("scan", help="扫描候选并生成 candidates.txt")
    imp = sub.add_parser("import", help="按清单导入")
    imp.add_argument("--selection", default=str(BLOG_ROOT / "tools" / "candidates.txt"))
    imp.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录（测试时指向临时目录）")
    args = ap.parse_args()
    {"scan": cmd_scan, "import": cmd_import}[args.cmd](args)


if __name__ == "__main__":
    main()
