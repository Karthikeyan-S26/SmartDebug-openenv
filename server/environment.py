from models import Action, Observation

class DebugEnv:

    def __init__(self):
        self.max_steps = 20
        self.reset()

    def reset(self):
        self.code = [
            "def add(a, b):",
            "    return a - b"   # BUG
        ]
        self.step_count = 0
        self.test_results = [False, False]

        return self._get_obs()

    def step(self, action: Action):
        self.step_count += 1
        reward = 0
        done = False

        if action.action_type == "edit_line":
            if 0 <= action.line_number < len(self.code):
                self.code[action.line_number] = action.new_code
            else:
                reward -= 0.05

        elif action.action_type == "run_tests":
            self.test_results = self._run_tests()
            reward += sum(self.test_results) * 0.2

            if all(self.test_results):
                reward += 1.0
                done = True

        if self.step_count >= self.max_steps:
            done = True

        return self._get_obs(), reward, done, {}

    def state(self):
        return self._get_obs()

    def _get_obs(self):
        return Observation(
            current_code="\n".join(self.code),
            stdout="",
            stderr="",
            test_results=self.test_results,
            step_count=self.step_count
        )

    def _run_tests(self):
        try:
            namespace = {}
            exec("\n".join(self.code), namespace)
            return [
                namespace["add"](2, 3) == 5,
                namespace["add"](5, 2) == 7
            ]
        except:
            return [False, False]