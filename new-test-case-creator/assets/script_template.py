"""
测试用例导出脚本
由 test-case-writer 技能生成 —— 下方 TEST_CASES_DATA 和 EXPECTED_TOTAL
由第二阶段撰写好的测试用例内容填充，其余导出/校验逻辑保持不变，不要修改。
"""

import pandas as pd

# ==================== 配置区 ====================
EXPECTED_TOTAL = 0  # 替换为第一阶段锁定的测试点总数 N
OUTPUT_FILE = "test_cases.xlsx"
DEFAULT_OWNER = "宁瑞瑞"
DEFAULT_STATUS = "就绪"
DEFAULT_CASE_TYPE = "功能测试"
DEFAULT_TEST_TYPE = "手动"
DEFAULT_STAGE = "功能测试阶段"

# ==================== 测试用例数据（由第二阶段内容填充） ====================
# 每条为字典，键名固定：id, module, priority, title, steps, expected, precondition(可选，无则留空字符串)
# steps / expected 必须是带编号的多行字符串，例如 "1. 步骤A\n2. 步骤B"，禁止使用 list[str]
TEST_CASES_DATA = []

# ==================== 以下为固定导出逻辑，请勿修改 ====================

COLUMNS = ["模块", "编号", "标题", "状态", "维护人", "用例类型", "重要程度", "测试类型",
           "预估工时", "剩余工时", "关联工作项", "前置条件", "步骤描述", "预期结果",
           "关注人", "备注", "适用阶段", "关联模块"]


def build_rows(data):
    rows = []
    for i, case in enumerate(data, start=1):
        print(f"[{i}/{len(data)}] 生成用例: {case['id']} - {case['title']}")
        rows.append({
            "模块": case["module"],
            "编号": "",
            "标题": case["title"],
            "状态": DEFAULT_STATUS,
            "维护人": DEFAULT_OWNER,
            "用例类型": DEFAULT_CASE_TYPE,
            "重要程度": case["priority"],
            "测试类型": DEFAULT_TEST_TYPE,
            "预估工时": "",
            "剩余工时": "",
            "关联工作项": "",
            "前置条件": case.get("precondition", ""),
            "步骤描述": case["steps"],
            "预期结果": case["expected"],
            "关注人": "",
            "备注": "",
            "适用阶段": DEFAULT_STAGE,
            "关联模块": "",
        })
    return rows


def main():
    rows = build_rows(TEST_CASES_DATA)
    df = pd.DataFrame(rows, columns=COLUMNS)
    df.to_excel(OUTPUT_FILE, index=False)

    total = EXPECTED_TOTAL if EXPECTED_TOTAL else len(TEST_CASES_DATA)
    if len(df) == total == len(TEST_CASES_DATA):
        print("校验通过")
    else:
        print("校验失败")
        print(f"  EXPECTED_TOTAL={EXPECTED_TOTAL}, 实际数据条数={len(TEST_CASES_DATA)}, 写入行数={len(df)}")

    print(f"已生成: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
