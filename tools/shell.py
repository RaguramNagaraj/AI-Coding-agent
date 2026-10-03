import shlex
import subprocess
import sys
from pathlib import Path


class ShellTool:
    ALLOWED_COMMANDS = {
        "python",
        "python3",
        "pytest",
    }

    BLOCKED_ARGUMENTS = {
        "&&",
        "||",
        ";",
        "|",
        ">",
        ">>",
        "<",
        "$(",
        "`",
    }

    def __init__(self, workspace: str = "./workspace"):
        self.workspace = Path(workspace).resolve()

    def _parse_command(self, command: str) -> list[str]:
        if not command or not command.strip():
            raise ValueError("Command cannot be empty.")

        try:
            parts = shlex.split(command, posix=False)
        except ValueError as exc:
            raise ValueError(
                f"Invalid command syntax: {exc}"
            ) from exc

        if not parts:
            raise ValueError("Command cannot be empty.")

        return parts

    def _validate_command(self, parts: list[str]):
        command_name = Path(parts[0]).name.lower()

        if command_name.endswith(".exe"):
            command_name = command_name[:-4]

        if command_name not in self.ALLOWED_COMMANDS:
            raise PermissionError(
                f"Command '{command_name}' is not allowed."
            )

        for argument in parts[1:]:
            if argument in self.BLOCKED_ARGUMENTS:
                raise PermissionError(
                    f"Unsafe shell operator '{argument}' is not allowed."
                )

        if command_name in {"python", "python3"}:
            if "-c" in parts or "-m" in parts:
                raise PermissionError(
                    "Python -c and Python -m execution are not allowed."
                )

    def run_command(
        self,
        command: str,
        timeout: int = 30,
    ) -> str:
        parts = self._parse_command(command)
        self._validate_command(parts)

        if parts[0].lower() in {"python", "python3"}:
            parts[0] = sys.executable

        result = subprocess.run(
            parts,
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
            f"Command: {command}",
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