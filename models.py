from pydantic import BaseModel

class Action(BaseModel):
    action_type: str  # e.g., "edit_line", "run_tests"
    line_number: int = 0
    new_code: str = ""

class Observation(BaseModel):
    code: str
    test_results: str = ""
    error: str = ""
    done: bool = False