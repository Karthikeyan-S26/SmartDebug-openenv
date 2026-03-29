from environment import DebugEnv
from models import Action

def main():
    env = DebugEnv(task_name="easy")
    
    tasks = ["easy", "medium", "hard"]
    for t in tasks:
        print(f"\n=== Testing Task: {t} ===")
        obs = env.reset(task_name=t)
        print(f"Loaded length of code: {len(obs.code.splitlines())} lines.")
        
        # Test original buggy code scoring
        obs, reward, done = env.step(Action(action_type="run_tests"))
        print(f"Initial test_results: {obs.test_results}")
        print(f"Initial reward/score: {reward}")
        print(f"Done: {done}")

if __name__ == "__main__":
    main()
