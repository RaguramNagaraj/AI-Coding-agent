import subprocess
import sys
from pathlib import Path


class TestRunner:
    __test__ = False

    def __init__(self, workspace: str = "./workspace"):
        self.workspace = Path(workspace).resolve()

    def run_tests(
        self,
        test_path: str = ".",
        timeout: int = 60,
    ) -> str:
        target = (self.workspace / test_path).resolve()

        if not target.is_relative_to(self.workspace):
            raise PermissionError(
                "Test path outside the workspace is not allowed."
            )

        if not target.exists():
            raise FileNotFoundError(
                f"Test path not found: {test_path}"
            )

        command = [
            sys.executable,
            "-m",
            "pytest",
            test_path,
            "-v",
        ]

        result = subprocess.run(
            command,
            cwd=self.workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )

        status = (
            "PASSED"
            if result.returncode == 0
            else "FAILED"
        )

        output = [
            f"Test path: {test_path}",
            f"Exit code: {result.returncode}",
            f"Status: {status}",
        ]

        if result.stdout:
            output.append(
                f"STDOUT:\n{result.stdout}"
            )

        if result.stderr:
            output.append(
                f"STDERR:\n{result.stderr}"
            )

        return "\n\n".join(output)