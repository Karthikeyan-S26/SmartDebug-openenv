from environment import DebugEnv
from models import Action

def main():
    env = DebugEnv()
    
    print("--- RESET ---")
    obs = env.reset()
    print(obs)
    
    print("\n--- STEP 1: Invalid Edit ---")
    action1 = Action(action_type="edit_line", line_number=10, new_code="junk")
    obs, reward, done = env.step(action1)
    print("Obs:", obs)
    print("Reward:", reward)
    
    print("\n--- STEP 2: Run Tests (Buggy) ---")
    action2 = Action(action_type="run_tests")
    obs, reward, done = env.step(action2)
    print("Obs test_results:", obs.test_results)
    print("Reward:", reward)
    
    print("\n--- STEP 3: Fix Bug ---")
    action3 = Action(action_type="edit_line", line_number=2, new_code="    return a + b")
    obs, reward, done = env.step(action3)
    print("Obs code:", obs.code)
    print("Reward:", reward)
    
    print("\n--- STEP 4: Run Tests (Fixed) ---")
    action4 = Action(action_type="run_tests")
    obs, reward, done = env.step(action4)
    print("Obs test_results:", obs.test_results)
    print("Reward:", reward)
    print("Done:", done)

if __name__ == "__main__":
    main()
