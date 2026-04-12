import sys
import os
import importlib
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models import Action, Observation


class Grader:
    @staticmethod
    def compute_score(code_str: str, entry_point: str, tests: list):
        local_vars = {}
        passed = 0
        total = len(tests)
        error = ""

        if total == 0:
            return 0, 0, 0.5, "No tests provided."

        try:
            exec(code_str, {}, local_vars)
            if entry_point not in local_vars:
                return 0, total, 0.3, f"Function '{entry_point}' not found."

            for test in tests:
                try:
                    expr = f"{entry_point}{test['input']}"
                    result = eval(expr, {}, local_vars)
                    if result == test["expected"]:
                        passed += 1
                except Exception:
                    pass

        except Exception:
            error = traceback.format_exc()

        if total == 0:
            score = 0.5
        else:
            score = passed / total

        # Force strictly into (0, 1)
        if score <= 0.0:
            score = 0.3
        elif score >= 1.0:
            score = 0.7

        return passed, total, score, error


class DebugEnv:

    TASKS = {
        "easy": {
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
        },
        "medium": {
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
        },
        "hard": {
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
    }

    def __init__(self, task_name="easy"):
        self.load_task(task_name)

    def load_task(self, task_name: str):
        task = self.TASKS.get(task_name, self.TASKS["easy"])
        self.task_data = task
        self.original_code = task["buggy_code"].copy()
        self.code_lines = self.original_code.copy()

    def reset(self, task_name=None):
        if task_name and task_name in self.TASKS:
            self.load_task(task_name)
        else:
            self.code_lines = self.original_code.copy()
        self.code_lines = self.original_code.copy()
        return self._get_obs()

    def step(self, action: Action):
        reward = 0.5
        done = False

        if action.action_type == "edit_line":
            if action.line_number is not None and 1 <= action.line_number <= len(self.code_lines):
                self.code_lines[action.line_number - 1] = action.new_code

        elif action.action_type == "run_tests":
            tests_passed, tests_total, score, error = self._run_tests()

            # Force strictly into (0, 1)
            if score <= 0.0:
                reward = 0.3
            elif score >= 1.0:
                reward = 0.7
            else:
                reward = score

            if tests_passed == tests_total and tests_total > 0:
                done = True

            obs = self._get_obs()
            obs.test_results = f"{tests_passed}/{tests_total} tests passed. Score: {score:.4f}"
            obs.error = error
            obs.done = done
            return obs, reward, done

        return self._get_obs(), reward, done

    def state(self):
        return "\n".join(self.code_lines)

    def _get_obs(self):
        return Observation(
            code=self.state(),
            test_results="",
            error="",
            done=False
        )

    def _run_tests(self):
        code_str = self.state()
        entry = self.task_data.get("entry_point", "")
        tests = self.task_data.get("tests", [])
        return Grader.compute_score(code_str, entry, tests)