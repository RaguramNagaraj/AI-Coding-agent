from agent.core import CodingAgent
from tools.filesystem import FileSystemTools
from tools.registry import ToolRegistry
from tools.shell import ShellTool
from tools.search import SearchTool
from tools.test_runner import TestRunner


def create_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    filesystem = FileSystemTools()
    shell = ShellTool()
    search = SearchTool()
    test_runner = TestRunner()

    registry.register(
        name="list_files",
        function=filesystem.list_files,
        description="List all files inside the workspace.",
        parameters={
            "type": "object",
            "properties": {},
        },
    )

    registry.register(
        name="read_file",
        function=filesystem.read_file,
        description="Read the contents of a text file inside the workspace.",
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file relative to the workspace.",
                }
            },
            "required": ["path"],
        },
    )

    registry.register(
        name="run_command",
        function=shell.run_command,
        description=(
            "Run an allowed development command inside the workspace. "
            "Use this tool to run tests, check syntax, or execute approved "
            "development commands. After modifying code, run the relevant "
            "tests when possible and inspect the result before declaring "
            "the task complete."
        ),
        parameters={
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": (
                        "Command to execute in the workspace."
                    ),
                },
                "timeout": {
                    "type": "integer",
                    "description": (
                        "Maximum execution time in seconds."
                    ),
                    "default": 30,
                },
            },
            "required": ["command"],
        },
    )

    registry.register(
        name="write_file",
        function=filesystem.write_file,
        description=(
            "Create a new file in the workspace or intentionally replace "
            "the complete contents of an existing file. "
            "When making a small or targeted change to an existing file, "
            "prefer edit_file instead."
        ),
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Path of the file relative to the workspace."
                    ),
                },
                "content": {
                    "type": "string",
                    "description": (
                        "Complete text content to write into the file."
                    ),
                },
            },
            "required": ["path", "content"],
        },
    )

    registry.register(
        name="search_files",
        function=search.search_files,
        description=(
            "Search for a text string inside files in the workspace. "
            "USE THIS TOOL whenever the user asks you to find, search, "
            "locate, or check whether a word, phrase, function, class, "
            "variable, import, or code pattern exists in the workspace. "
            "Do NOT list and read files manually to perform a search. "
            "Returns matching file paths, line numbers, and matching lines."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Text to search for inside files."
                    ),
                },
                "path": {
                    "type": "string",
                    "description": (
                        "Optional file or directory to search "
                        "inside. Defaults to the workspace."
                    ),
                    "default": ".",
                },
                "case_sensitive": {
                    "type": "boolean",
                    "description": (
                        "Whether the search should match "
                        "letter case."
                    ),
                    "default": False,
                },
            },
            "required": ["query"],
        },
    )

    registry.register(
        name="edit_file",
        function=filesystem.edit_file,
        description=(
            "Modify an existing file by replacing exactly one specific "
            "piece of existing text. Prefer this tool for targeted code "
            "changes instead of rewriting the entire file with write_file. "
            "Use read_file or search_files first when necessary to inspect "
            "the existing code. The old_text must match exactly once."
        ),
        parameters={
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Path to the existing file inside the workspace."
                    ),
                },
                "old_text": {
                    "type": "string",
                    "description": (
                        "The exact existing text to replace. "
                        "It must occur exactly once."
                    ),
                },
                "new_text": {
                    "type": "string",
                    "description": (
                        "The replacement text."
                    ),
                },
            },
            "required": [
                "path",
                "old_text",
                "new_text",
            ],
        },
    )

    registry.register(
        name="run_tests",
        function=test_runner.run_tests,
        description=(
            "Run pytest tests inside the workspace. "
            "Use this after modifying code to verify the changes."
        ),
        parameters={
            "type": "object",
            "properties": {
                "test_path": {
                    "type": "string",
                    "description": (
                        "Test file or directory relative to the workspace."
                    ),
                    "default": ".",
                },
                "timeout": {
                    "type": "integer",
                    "description": (
                        "Maximum execution time in seconds."
                    ),
                    "default": 60,
                },
            },
        },
    )

    return registry


def main():
    registry = create_tool_registry()

    print()

    agent = CodingAgent(registry)

    print("=" * 60)
    print("                    CODING AGENT")
    print("=" * 60)
    print()
    print("Workspace: ./workspace")
    print("Type 'exit' or 'quit' to stop.")
    print()

    while True:
        try:
            user_input = input("You > ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            response = agent.chat(user_input)

            print()
            print(f"Agent > {response}")
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        except Exception as exc:
            print(
                f"\nError: {type(exc).__name__}: {exc}\n"
            )


if __name__ == "__main__":
    main()