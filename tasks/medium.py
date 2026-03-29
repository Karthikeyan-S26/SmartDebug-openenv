TASK = {
    "name": "medium",
    "buggy_code": [
        "def multiply(a, b):",
        "    result = 0",
        "    for i in range(b):",
        "        result += a - 1   # bug",
        "    return result"
    ],
    "tests": [
        {"input": "(3, 4)", "expected": 12},
        {"input": "(5, 0)", "expected": 0},
        {"input": "(2, 10)", "expected": 20}
    ],
    "entry_point": "multiply"
}
