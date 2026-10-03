from pathlib import Path


class SearchTool:
    IGNORE_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        ".pytest_cache",
    }

    MAX_RESULTS = 100
    MAX_FILE_SIZE = 1_000_000

    def __init__(self, workspace: str = "./workspace"):
        self.workspace = Path(workspace).resolve()

    def _resolve_path(self, path: str) -> Path:
        target = (self.workspace / path).resolve()

        if not target.is_relative_to(self.workspace):
            raise PermissionError(
                "Access outside the workspace is not allowed."
            )

        return target

    def search_files(
        self,
        query: str,
        path: str = ".",
        case_sensitive: bool = False,
    ) -> str:
        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        search_root = self._resolve_path(path)

        if not search_root.exists():
            raise FileNotFoundError(
                f"Search path not found: {path}"
            )

        if not search_root.is_dir() and not search_root.is_file():
            raise ValueError(
                f"Search path is not a valid file or directory: {path}"
            )

        if not case_sensitive:
            query = query.lower()

        results = []

        if search_root.is_file():
            files = [search_root]
        else:
            files = search_root.rglob("*")

        for file_path in files:
            if not file_path.is_file():
                continue

            if self._should_ignore(file_path):
                continue

            try:
                if file_path.stat().st_size > self.MAX_FILE_SIZE:
                    continue

                content = file_path.read_text(
                    encoding="utf-8"
                )
            except (UnicodeDecodeError, OSError):
                continue

            lines = content.splitlines()

            for line_number, line in enumerate(lines, start=1):
                searchable_line = (
                    line if case_sensitive else line.lower()
                )

                if query in searchable_line:
                    relative_path = file_path.relative_to(
                        self.workspace
                    )

                    results.append(
                        f"{relative_path}:{line_number}:{line.strip()}"
                    )

                    if len(results) >= self.MAX_RESULTS:
                        return self._format_results(
                            results,
                            truncated=True,
                        )

        return self._format_results(results)

    def _should_ignore(self, path: Path) -> bool:
        try:
            relative_path = path.relative_to(self.workspace)
        except ValueError:
            return True

        return any(
            part in self.IGNORE_DIRECTORIES
            for part in relative_path.parts
        )

    def _format_results(
        self,
        results: list[str],
        truncated: bool = False,
    ) -> str:
        if not results:
            return "No matches found."

        output = [
            f"Found {len(results)} match(es):"
        ]

        output.extend(results)

        if truncated:
            output.append(
                f"\nResults truncated at {self.MAX_RESULTS} matches."
            )

        return "\n".join(output)