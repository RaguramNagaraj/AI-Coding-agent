from agent.llm import OllamaClient


class Planner:
    def __init__(self):
        self.llm = OllamaClient()

    def create_plan(self, task: str) -> list[str]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are the planning component of a coding agent. "
                    "Create a short practical plan for the user's task. "
                    "For coding tasks, prefer: inspect files, modify code, run tests, "
                    "fix failures if needed, and report the result. "
                    "Return only numbered steps. "
                    "Do not execute tools. "
                    "Do not include explanations. "
                    "Keep the plan between 2 and 7 steps."
                ),
            },
            {
                "role": "user",
                "content": task,
            },
        ]

        response = self.llm.chat(messages)

        content = response.get("content", "").strip()

        return self._parse_plan(content)

    def _parse_plan(self, content: str) -> list[str]:
        steps = []

        for line in content.splitlines():
            line = line.strip()

            if not line:
                continue

            if line[0].isdigit() and "." in line:
                step = line.split(".", 1)[1].strip()

                if step:
                    steps.append(step)

        return steps[:7]