class ToolRegistry:
    def __init__(self):
        self._tools = {}
        self._schemas = {}

    def register(
        self,
        name: str,
        function,
        description: str,
        parameters: dict,
    ):
        if not name.strip():
            raise ValueError("Tool name cannot be empty.")

        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        if not callable(function):
            raise TypeError(
                f"Tool '{name}' must be callable."
            )

        self._tools[name] = function

        self._schemas[name] = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
        }

    def get(self, name: str):
        return self._tools.get(name)

    def get_schemas(self) -> list[dict]:
        return list(self._schemas.values())

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())