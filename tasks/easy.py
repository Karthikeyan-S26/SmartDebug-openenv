TASK = {
    "name": "easy",
    "buggy_code": [
        "def add(a, b):",
        "    return a - b   # bug"
    ],
    "tests": [
        {"input": "(2, 3)", "expected": 5},
        {"input": "(5, 2)", "expected": 7},
        {"input": "(0, 0)", "expected": 0}
    ],
    "entry_point": "add"
}
