#!/usr/bin/env python3
"""Validate daily plan lines for length and required evidence."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MAX_CHARS = 75
HOURS_RE = re.compile(r"(?:工时|总计).{0,8}(?:\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?h)", re.I)
EVIDENCE_RE = re.compile(r"(?:依据|模块|流程|功能点|用例|接口|缺陷|平台|服务|组件|场景|数据|角色|检查点|议题).{0,20}\d|\d.{0,8}(?:模块|流程|功能点|例|接口|缺陷|平台|服务|组件|场景|数据|角色|检查点|议题)")
PREFIX_RE = re.compile(r"^\s*(?:[-*]\s+|\d+[.、]\s*)")


def validate_line(raw: str, line_no: int) -> list[str]:
    line = PREFIX_RE.sub("", raw.strip())
    if not line:
        return []

    errors: list[str] = []
    if len(line) > MAX_CHARS:
        errors.append(f"第{line_no}行超过{MAX_CHARS}字符：{len(line)}字符")
    if not HOURS_RE.search(line):
        errors.append(f"第{line_no}行缺少工时（如：工时1.5h）")
    if "总计" not in line and not EVIDENCE_RE.search(line):
        errors.append(f"第{line_no}行缺少可量化依据")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验每日测试计划的长度、工时和量化依据")
    parser.add_argument("plan", type=Path, help="UTF-8计划文本文件")
    args = parser.parse_args()

    text = args.plan.read_text(encoding="utf-8-sig")
    errors = [error for no, line in enumerate(text.splitlines(), 1) for error in validate_line(line, no)]
    if errors:
        print("校验失败：")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print("校验通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
