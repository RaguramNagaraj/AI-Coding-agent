import pytest

from tools.filesystem import FileSystemTools
from tools.registry import ToolRegistry
from tools.shell import ShellTool


def test_filesystem_blocks_path_traversal(tmp_path):
    tools = FileSystemTools(str(tmp_path))

    with pytest.raises(PermissionError):
        tools.read_file("../outside.txt")


def test_filesystem_can_write_and_read(tmp_path):
    tools = FileSystemTools(str(tmp_path))

    tools.write_file("example.txt", "hello")

    assert tools.read_file("example.txt") == "hello"


def test_edit_file_requires_unique_match(tmp_path):
    tools = FileSystemTools(str(tmp_path))

    tools.write_file(
        "example.txt",
        "hello\nhello\n",
    )

    with pytest.raises(ValueError):
        tools.edit_file(
            "example.txt",
            "hello",
            "world",
        )


def test_shell_blocks_unknown_command(tmp_path):
    shell = ShellTool(str(tmp_path))

    with pytest.raises(PermissionError):
        shell.run_command("powershell -Command Get-Date")


def test_shell_blocks_command_chaining(tmp_path):
    shell = ShellTool(str(tmp_path))

    with pytest.raises(PermissionError):
        shell.run_command("python --version && whoami")


def test_shell_allows_python(tmp_path):
    shell = ShellTool(str(tmp_path))

    result = shell.run_command(
        "python -c \"print('safe')\""
    )

    assert "safe" in result
    assert "PASSED" in result


def test_registry_rejects_duplicate_tools():
    registry = ToolRegistry()

    registry.register(
        name="example",
        function=lambda: "ok",
        description="Example tool",
        parameters={
            "type": "object",
            "properties": {},
        },
    )

    with pytest.raises(ValueError):
        registry.register(
            name="example",
            function=lambda: "again",
            description="Duplicate",
            parameters={
                "type": "object",
                "properties": {},
            },
        )
