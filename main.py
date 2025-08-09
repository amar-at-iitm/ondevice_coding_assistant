# main.py
import argparse
import json
import os
from datetime import datetime

from config import MAX_DEBUG_ATTEMPTS
from llm_interface import generate_code
from sandbox import run_in_sandbox

def solve_task(task: str):
    """
    Main logic loop to generate, run, and debug code.
    """
    print(f"--- Starting Task: {task} ---")
    debug_history = []
    
    # Initial code generation
    prompt = f"Initial prompt: Write Python code to {task}. Do not add any explanation, just the code."
    current_code = generate_code(prompt)

    for attempt in range(MAX_DEBUG_ATTEMPTS):
        print(f"\n--- Attempt {attempt + 1}/{MAX_DEBUG_ATTEMPTS} ---")
        print("Generated Code:\n" + "-"*20 + f"\n{current_code}\n" + "-"*20)

        print("[Sandbox] Executing code...")
        output, error = run_in_sandbox(current_code)

        history_entry = {
            "attempt": attempt + 1,
            "code": current_code,
            "output": output,
            "error": error
        }
        debug_history.append(history_entry)

        if error:
            print(f"[Sandbox] Execution failed.")
            print(f"Error: {error}")
            
            if attempt < MAX_DEBUG_ATTEMPTS - 1:
                # Prepare debug prompt
                debug_prompt = f"""The code failed.
Original task: '{task}'.
---
Faulty Code:
{current_code}
---
Error Message:
{error}
---
Fix the code. Provide only the complete, corrected Python code."""
                current_code = generate_code(debug_prompt)
            else:
                print("\n--- Task Failed: Max debug attempts reached. ---")
                break
        else:
            print("[Sandbox] Execution successful!")
            print(f"Output: {output}")
            print("\n--- Task Complete! ---")
            save_results(task, debug_history)
            return

    # If the loop finishes without success
    save_results(task, debug_history)


def save_results(task: str, history: list):
    """Saves the final code and debug history to files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/task_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # Save final code
    final_code = history[-1].get("code")
    if final_code:
        with open(os.path.join(output_dir, "final_code.py"), "w") as f:
            f.write(final_code)

    # Save debug history
    with open(os.path.join(output_dir, "debug_history.json"), "w") as f:
        json.dump(history, f, indent=2)

    # Save execution log
    final_output = history[-1].get("output", "") or history[-1].get("error", "")
    with open(os.path.join(output_dir, "execution_log.txt"), "w") as f:
        f.write(final_output)

    print(f"\nResults saved in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="On-Device Coding Assistant")
    parser.add_argument("task", type=str, help="The coding task to perform, in natural language.")
    args = parser.parse_args()
    solve_task(args.task)