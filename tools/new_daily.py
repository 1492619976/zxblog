#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""new_daily.py — 一键创建当天的每日笔记（文件 + 索引 + 侧边栏）

用法：
  py -3 tools/new_daily.py              # 创建今天
  py -3 tools/new_daily.py 2026-10-11   # 补某天

幂等：目标日期已存在则什么都不改。
创建后：在 Obsidian 里打开生成的文件填三段，然后
  git add . && git commit -m "daily: <日期>" && git push
"""

import re
import sys
from datetime import date
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent
DAILY = BLOG / "docs" / "daily"
INDEX = DAILY / "index.md"
SIDEBAR = BLOG / "docs" / ".vitepress" / "sidebar.gen.ts"

TEMPLATE = """# {d}

## TIL

### （知识点标题）

（问题背景 → 学到的内容 → 代码示例）

## 卡点

-

## 参考

-
"""


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
        sys.exit(f"日期格式应为 YYYY-MM-DD，收到：{d}")
    target = DAILY / f"{d}.md"
    if target.exists():
        print(f"文件已存在，检查索引与侧边栏是否需要补齐：{target}")
    else:
        target.write_text(TEMPLATE.format(d=d, placeholder="（一句话主题）"), encoding="utf-8")

    # 索引表加行（幂等）：追加到表格最后一行之后
    idx = INDEX.read_text(encoding="utf-8")
    row = f"| [{d}](/daily/{d}) | （一句话主题） |"
    if f"(/daily/{d})" not in idx:
        lines = idx.splitlines()
        last = max(i for i, ln in enumerate(lines) if ln.startswith("| "))
        lines.insert(last + 1, row)
        INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 侧边栏 daily 节加条目（幂等），插在"总览"之后（key 兼容带引号/不带引号两种写法）
    sb = SIDEBAR.read_text(encoding="utf-8")
    if f'"/daily/{d}"' not in sb:
        entry = f'      {{ text: \'{d}\', link: "/daily/{d}" }},'
        m = re.search(r'((?:"daily"|daily): \[\n.*?link: [\'"]?/daily/[\'"]?.*?\n)', sb)
        if m:
            sb = sb[:m.end(1)] + entry + "\n" + sb[m.end(1):]
            SIDEBAR.write_text(sb, encoding="utf-8")

    print(f"就绪：{target}")
    print(f"已更新：{INDEX.name}、sidebar.gen.ts")
    print(f'发布：git add . && git commit -m "daily: {d}" && git push')


if __name__ == "__main__":
    main()
