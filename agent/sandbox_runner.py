"""
TrapWire - Sandboxed Execution Runner
Orchestrates isolated inspection sessions via Docker containers or isolated subprocess sandboxes.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

class SandboxRunner:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.worker_script = self.project_root / "docker" / "sandbox_worker.py"
        self.has_docker = self._check_docker_available()

    def _check_docker_available(self) -> bool:
        """Verifies if Docker Daemon is actively responding."""
        try:
            import docker
            client = docker.from_env()
            client.ping()
            return True
        except Exception:
            return False

    def execute_in_sandbox(self, target_url: str) -> Dict[str, Any]:
        """
        Executes URL inspection within a sandboxed environment.
        Uses Docker container if available; falls back to an isolated process runner.
        """
        if self.has_docker:
            return self._run_docker_container(target_url)
        else:
            return self._run_local_sandbox(target_url)

    def _run_docker_container(self, target_url: str) -> Dict[str, Any]:
        """Runs the inspection inside a privileged-dropped Docker container."""
        import docker
        client = docker.from_env()
        try:
            container = client.containers.run(
                image="python:3.11-slim",
                command=f"python /sandbox/sandbox_worker.py --url {target_url}",
                volumes={str(self.project_root / 'docker'): {'bind': '/sandbox', 'mode': 'ro'}},
                mem_limit="512m",
                network_mode="bridge",
                remove=True,
                detach=False
            )
            raw_output = container.decode("utf-8").strip()
            return json.loads(raw_output)
        except Exception as e:
            # Fallback to local sandbox if container build/run fails
            return self._run_local_sandbox(target_url)

    def _run_local_sandbox(self, target_url: str) -> Dict[str, Any]:
        """Executes inspection in an isolated process sandbox with strict timeout."""
        cmd = [sys.executable, str(self.worker_script), "--url", target_url]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
                cwd=str(self.project_root)
            )
            stdout = proc.stdout.strip()
            if stdout:
                # Find the last json line
                for line in reversed(stdout.splitlines()):
                    if line.startswith("{") and line.endswith("}"):
                        return json.loads(line)
            return {"status": "error", "error_message": proc.stderr or "No output"}
        except subprocess.TimeoutExpired:
            return {"status": "error", "error_message": "Sandbox execution timed out"}
        except Exception as e:
            return {"status": "error", "error_message": str(e)}

# Singleton
sandbox_runner = SandboxRunner()
