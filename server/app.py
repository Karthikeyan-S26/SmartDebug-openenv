import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel

from server.environment import DebugEnv
from models import Action

app = FastAPI()
env = DebugEnv()


class ResetRequest(BaseModel):
    task_name: Optional[str] = "easy"


@app.post("/reset")
def reset(request: Optional[ResetRequest] = None, task_name: str = Query("easy")):
    if request and request.task_name:
        task_name = request.task_name
    obs = env.reset(task_name)
    return {"observation": obs}


@app.get("/reset")
def reset_get(task_name: str = "easy"):
    obs = env.reset(task_name)
    return {"observation": obs}


@app.post("/step")
def step_env(action: Action):
    result = env.step(action)
    obs, reward, done = result
    return {
        "observation": obs,
        "reward": reward,
        "done": done
    }


@app.get("/state")
def get_state():
    return {"state": env.state()}


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
