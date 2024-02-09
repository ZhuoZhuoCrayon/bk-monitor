# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云 - 监控平台 (BlueKing - Monitor) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import re
import sys
import typing

# ============== 30 failed, 492 passed, 2 errors in 219.92s (0:03:39) ===========
# ================= 1 failed, 30 passed in 103.26s (0:01:43) ===============
# ========================== 31 passed in 103.18s (0:01:43) =================


# Ran 191 tests in 1.725s
#
# FAILED (failures=34, errors=24)


# Ran 20 tests in 0.398s
#
# OK


# Ran 20 tests in 0.405s
#
# FAILED (failures=1)


def handle_pytest(output: str) -> typing.Dict[str, int]:
    pattern = re.compile(r"={3,}\s*(?:\d+\s*(?:failed|passed|errors),?\s*)+?in\s*[\d\.s]+\s*\(\d+:\d+:\d+\)\s*={3,}")
    matched_line: str = pattern.findall(output)[-1]

    test_result: typing.Dict[str, int] = {}
    for num_str, category in re.findall(r"(\d+)\s*(failed|passed|errors)", matched_line):
        test_result[category] = int(num_str)
    return test_result


def handle_testcase(output: str) -> typing.Dict[str, int]:
    pattern = re.compile(r"Ran\s(\d+)\stests\sin\s[\d\.s]+\s+(OK|FAILED\s\((?:failures|errors)=\d+,?\s?\))")
    total_str, matched_line = pattern.findall(output)[-1]

    category_mapping: typing.Dict[str, str] = {"failures": "failed"}
    test_result: typing.Dict[str, int] = {}
    for category, num_str in re.findall(r"(failures|errors)=(\d+)", matched_line):
        test_result[category_mapping.get(category, category)] = int(num_str)

    test_result["passed"] = int(total_str) - category_mapping.get("failed", 0) - category_mapping.get("errors", 0)


def parse_test_output(file_name):
    with open(file_name, "r") as file:
        content = file.read()

    if "pytest" in file_name:
        test_result = handle_pytest(content)
    else:
        test_result = handle_testcase(content)

    print(f"{test_result.get('passed', 0)}, {test_result.get('failed', 0)}, {test_result.get('errors', 0)}")


if __name__ == "__main__":
    parse_test_output(sys.argv[1])
