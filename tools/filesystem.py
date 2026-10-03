from pathlib import Path


class FileSystemTools:
    PROTECTED_NAMES = {
        ".env",
        ".git",
        ".gitignore",
        "credentials.json",
        "secrets.json",
    }

    def __init__(self, workspace: str = "./workspace"):
        self.workspace = Path(workspace).resolve()

    def _resolve_path(self, path: str) -> Path:
        target = (self.workspace / path).resolve()

        if not target.is_relative_to(self.workspace):
            raise PermissionError(
                "Access outside the workspace is not allowed."
            )

        return target

    def _is_protected(self, path: Path) -> bool:
        try:
            relative = path.relative_to(self.workspace)
        except ValueError:
            return True

        return any(
            part in self.PROTECTED_NAMES
            for part in relative.parts
        )

    def list_files(self) -> list[str]:
        files = []

        for path in self.workspace.rglob("*"):
            if path.is_file() and not self._is_protected(path):
                files.append(
                    str(path.relative_to(self.workspace))
                )

        return sorted(files)

    def read_file(self, path: str) -> str:
        file_path = self._resolve_path(path)

        if self._is_protected(file_path):
            raise PermissionError(
                "Access to protected files is not allowed."
            )

        if not file_path.is_file():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        return file_path.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> str:
        file_path = self._resolve_path(path)

        if self._is_protected(file_path):
            raise PermissionError(
                "Writing protected files is not allowed."
            )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return f"Successfully wrote {path}"

    def edit_file(
        self,
        path: str,
        old_text: str,
        new_text: str,
    ) -> str:
        file_path = self._resolve_path(path)

        if self._is_protected(file_path):
            raise PermissionError(
                "Editing protected files is not allowed."
            )

        if not file_path.is_file():
            raise FileNotFoundError(
                f"File not found: {path}"
            )

        content = file_path.read_text(
            encoding="utf-8"
        )

        occurrences = content.count(old_text)

        if occurrences == 0:
            raise ValueError(
                "The specified old_text was not found in the file."
            )

        if occurrences > 1:
            raise ValueError(
                f"The specified old_text appears {occurrences} times. "
                "Edit cancelled because the target is ambiguous."
            )

        file_path.write_text(
            content.replace(old_text, new_text, 1),
            encoding="utf-8",
        )

        return (
            f"Successfully edited {path}. "
            "Exactly one occurrence was replaced."
        )