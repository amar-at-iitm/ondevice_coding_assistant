# ondevice_coding_assistant

An intelligent, local-first coding assistant that understands natural language, writes code, and autonomously debugs it within a secure, sandboxed environment. Powered by the 20-billion parameter model, `GPT-OSS-20B`, this tool runs entirely on your machine, ensuring your code and data remain private.

---

##  Problem Statement

The goal is to create a local coding assistant powered by `GPT-OSS-20B` that can:
1.  Accept natural-language coding tasks (e.g., “*Write a Python function to…*”).
2.  Generate the corresponding code.
3.  Execute it locally in a secure sandbox.
4.  Detect errors, debug, and retry until the code runs successfully or the attempt limit is reached.
5.  Run entirely on-device for complete privacy and offline capability.

---

## Features

* **Natural Language Interface**: Give instructions in plain English.
* **Automated Code Generation & Debugging**: The assistant not only writes code but also fixes its own mistakes based on execution errors.
* **Safe & Sandboxed Execution**: All generated code is run in an isolated environment (like a Docker container) to prevent any potential harm to your system.
* **100% Local & Private**: No internet connection is needed after setup. Your prompts and code never leave your machine.
* **Detailed Logging**: Keeps a history of prompts, generated code, execution results, and debugging attempts for full transparency.
* **Configurable**: Easily set parameters like the maximum number of debugging attempts.

---

##  How It Works

The assistant follows a simple yet powerful loop:

1.  **Input**: You provide a coding task via the command line or a web interface.
2.  **Generate**: The `GPT-OSS-20B` model generates the code based on your request.
3.  **Execute**: The generated code is saved to a file and run inside a secure sandbox.
4.  **Analyze**:
    * **Success**: If the code runs without errors, the output, logs, and final code are presented to you.
    * **Error**: If the code fails, the error message and traceback are captured.
5.  **Debug (if error)**: The error message, original prompt, and the faulty code are fed back into the `GPT-OSS-20B` model with an instruction to "fix the bug." The process repeats from Step 3 with the new code.
6.  **Exit**: The loop terminates upon successful execution or after a configurable number of failed attempts (`N`).



---

##  Tech Stack

* **Language Model**: `GPT-OSS-20B` for code generation and debugging logic.
* **Execution Sandbox**: **Docker** (recommended) or **Firejail** / **sandboxed subprocesses** for safe code execution.
* **Backend**: **Python** for the main application logic, model inference, and sandbox management.
* **Interface**: Interactive **CLI** or a simple **Web UI**.

---

## Project Structure
```
ondevice_coding_assistant/
├── config.py           # Configuration (like max attempts)
├── llm_interface.py    # Handles interaction with GPT-OSS-20B
├── sandbox.py          # Manages safe code execution in Docker
├── main.py             # The main application logic and CLI
├── Dockerfile          # Defines the environment for running user code
└── requirements.txt    # Python dependencies
```

### Prerequisites

* Python 3.8+
* Git
* Docker installed and running.
* Sufficient hardware to run the `GPT-OSS-20B` model (e.g., a modern GPU with at least 24GB of VRAM is recommended).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amar-at-iitm/ondevice_coding_assistant
    cd ondevice_coding_assistant
    ```

2.  **Set up the Language Model:**
    Download the `GPT-OSS-20B` model weights and place them in a `model/` directory. Follow the instructions from the model provider for setup.
    *(Note: This is a large model, and the download/setup process may be resource-intensive.)*

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    Edit the `config.yaml` file to set your preferences, such as the maximum number of debug attempts.
    ```yaml
    # config.yaml
    max_debug_attempts: 5
    sandbox_type: 'docker' # or 'subprocess'
    ```

---

##  Usage

### Command-Line Interface (CLI)

Use the `assistant.py` script to interact with the assistant.

**Basic Example:**
```bash
python assistant.py "Create a Python script that prints the first 20 numbers of the Fibonacci sequence."
````

**Example with Language Constraint:**

```bash
python assistant.py --lang "Rust" "Write a function that takes two integers and returns their sum."
```

### Outputs

Upon completion, the assistant will create an `output/` directory for your task, structured as follows:

```
output/
└── task_20250812_183005/
    ├── final_code.py
    ├── execution_log.txt
    └── debug_history.json
```

  * `final_code.py`: The final, working version of the code.
  * `execution_log.txt`: The full console output from the final successful run.
  * `debug_history.json`: A structured log of each generation and debug attempt.

-----

## Project Milestones

  - [x] Set up `GPT-OSS-20B` inference locally.
  - [x] Implement safe execution sandbox (Docker-based).
  - [ ] Create initial “generate code” → “run” → “error handling” loop.
  - [ ] Add debugging mode (error trace → fix code → re-run).
  - [ ] Test on at least 20 varied programming tasks.
  - [ ] Develop an interactive CLI.
  - [ ] (Optional) Build a simple web UI.


-----
