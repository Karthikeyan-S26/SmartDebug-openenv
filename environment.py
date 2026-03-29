from models import Action, Observation
import traceback
import importlib
from grader.grader import Grader

class DebugEnv:
    def __init__(self, task_name="easy"):
        self.load_task(task_name)
        
    def load_task(self, task_name: str):
        try:
            task_module = importlib.import_module(f"tasks.{task_name}")
            self.task_data = task_module.TASK
        except ImportError:
            self.task_data = {
                "name": task_name,
                "buggy_code": ["print('Task not found')"],
                "tests": [],
                "entry_point": "fake"
            }
        
        self.original_code = self.task_data["buggy_code"]
        self.code_lines = self.original_code.copy()
        
    def reset(self, task_name=None) -> Observation:
        if task_name is not None:
            self.load_task(task_name)
        self.code_lines = self.original_code.copy()
        return self._get_obs()
        
    def step(self, action: Action):
        reward = 0.0
        done = False
        
        if action.action_type == "edit_line":
            if action.line_number is not None and 1 <= action.line_number <= len(self.code_lines):
                self.code_lines[action.line_number - 1] = action.new_code
            else:
                reward -= 0.05  # invalid edit
                
        elif action.action_type == "run_tests":
            tests_passed, tests_total, score, error = self._run_tests()
            
            reward += score
            
            if score >= 1.0 and tests_total > 0:
                reward += 1.0  # Bonus for completing safely
                done = True
                
            obs = self._get_obs()
            obs.test_results = f"{tests_passed}/{tests_total} tests passed. Score: {score}"
            obs.error = error
            obs.done = done
            return obs, reward, done
            
        return self._get_obs(), reward, done

    def state(self) -> str:
        return "\n".join(self.code_lines)

    def _get_obs(self) -> Observation:
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

