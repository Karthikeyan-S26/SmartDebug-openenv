import requests
import os

BASE_URL = "https://karthisenthil-smartdebug-env.hf.space"

API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

print("[START]")

tasks = ["easy", "medium", "hard"]

for task in tasks:
    try:
        print(f"task: {task}")

        requests.post(f"{BASE_URL}/reset", params={"task_name": task})

        done = False
        step_count = 0
        final_reward = 0

        while not done and step_count < 10:
            step_count += 1

            action = {"action_type": "run_tests"}
            response = requests.post(f"{BASE_URL}/step", json=action)

            if response.status_code != 200:
                break

            data = response.json()
            reward = data.get("reward", 0)
            done = data.get("done", False)
            final_reward = reward

            print("\n[STEP]")
            print("action: run_tests")
            print(f"reward: {reward}")

        print("\n[END]")
        print(f"final_score: {final_reward}")

    except Exception:
        print("\n[STEP]")
        print("action: error")
        print("reward: 0")

        print("\n[END]")
        print("final_score: 0")
