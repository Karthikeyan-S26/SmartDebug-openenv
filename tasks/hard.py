TASK = {
    "name": "hard",
    "buggy_code": [
        "def fibonacci(n):",
        "    if n <= 1:",
        "        return 1   # bug: return n",
        "    return fibonacci(n-1) + fibonacci(n-3)   # bug: fibonacci(n-2)"
    ],
    "tests": [
        {"input": "(1)", "expected": 1},
        {"input": "(5)", "expected": 5},
        {"input": "(10)", "expected": 55}
    ],
    "entry_point": "fibonacci"
}
