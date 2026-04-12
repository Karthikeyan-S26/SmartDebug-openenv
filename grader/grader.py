import traceback

class Grader:
    @staticmethod
    def compute_score(code_str: str, entry_point: str, tests: list):
        local_vars = {}
        passed = 0
        total = len(tests)
        error = ""
        
        if total == 0:
            return 0, 0, 0.0, "No tests provided."
            
        try:
            exec(code_str, {}, local_vars)
            if entry_point not in local_vars:
                return 0, total, 0.0, f"Function '{entry_point}' not found."
                
            for test in tests:
                try:
                    expr = f"{entry_point}{test['input']}"
                    result = eval(expr, {}, local_vars)
                    if result == test["expected"]:
                        passed += 1
                except Exception as e:
                    pass
                    
        except Exception as e:
            error = traceback.format_exc()
            
        score = float(passed / total)
        # Ensure score falls strictly between 0 and 1
        score = max(0.01, min(0.99, score))
        return passed, total, score, error
