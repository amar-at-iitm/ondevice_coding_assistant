# sandbox.py
import docker
import os
import tempfile
from docker.errors import ContainerError, ImageNotFound
from config import DOCKER_IMAGE, TIMEOUT_SECONDS

def run_in_sandbox(code_string: str) -> tuple[str | None, str | None]:
    """
    Runs a string of Python code in a secure Docker container.

    Args:
        code_string: The Python code to execute.

    Returns:
        A tuple of (output, error). If successful, error is None.
        If it fails, output is None.
    """
    try:
        client = docker.from_env()
        # Ensure the image is available
        try:
            client.images.get(DOCKER_IMAGE)
        except ImageNotFound:
            print(f"Pulling Docker image: {DOCKER_IMAGE}...")
            client.images.pull(DOCKER_IMAGE)

        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = os.path.join(temp_dir, "main.py")
            with open(script_path, "w") as f:
                f.write(code_string)

            container = client.containers.run(
                image=DOCKER_IMAGE,
                command=f"python main.py",
                volumes={os.path.abspath(temp_dir): {'bind': '/app', 'mode': 'ro'}}, # Read-only
                working_dir="/app",
                remove=True,  # Automatically remove the container when done
                detach=True,
                mem_limit="256m",
                network_disabled=True # Crucial for security
            )

            # Wait for the container to finish, with a timeout
            try:
                result = container.wait(timeout=TIMEOUT_SECONDS)
                stdout = container.logs(stdout=True, stderr=False).decode('utf-8').strip()
                stderr = container.logs(stdout=False, stderr=True).decode('utf-8').strip()

                if result['StatusCode'] == 0:
                    return stdout, None
                else:
                    return None, stderr
            except Exception as e:
                container.kill()
                return None, f"Execution timed out after {TIMEOUT_SECONDS} seconds."


    except ContainerError as e:
        return None, e.stderr.decode('utf-8')
    except Exception as e:
        return None, str(e)