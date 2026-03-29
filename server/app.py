import os
import sys

# Ensure root directory is in path just in case
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from environment import DebugEnv
from models import Action

app = FastAPI()
env = DebugEnv()

@app.get("/reset")
def reset_env(task_name: str = "easy"):
    obs = env.reset(task_name)
    return {"observation": obs}

@app.post("/step")
def step_env(action: Action):
    obs, reward, done = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def get_state():
    return {"state": env.state()}
