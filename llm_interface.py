# llm_interface.py
import time

def generate_code(prompt: str) -> str:
    """
    Simulates a call to the GPT-OSS-20B model.
    Replace this with your actual model inference code.
    """
    print("\n[LLM] Received prompt...")
    print(f"[LLM] Prompt: \"{prompt[:80]}...\"")
    time.sleep(1) # Simulate processing time

    # --- SIMULATED RESPONSE ---
    # This is where you would get the real model output.
    # We'll hardcode responses for a sample task: "calculate fibonacci up to 10"

    if "Initial prompt" in prompt:
        print("[LLM] Generating initial code...")
        # Intentionally buggy code (prints one too many)
        return """
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n + 1): # Bug is here
        print(a, end=' ')
        a, b = b, a + b

fibonacci(10)
"""
    elif "Fix the code" in prompt:
        print("[LLM] Received error, attempting to debug...")
        # Corrected code
        return """
def fibonacci(n):
    a, b = 0, 1
    # Corrected the loop to range(n)
    for _ in range(n):
        print(a, end=' ')
        a, b = b, a + b

fibonacci(10)
"""
    return "print('Error: Could not understand the prompt.')"