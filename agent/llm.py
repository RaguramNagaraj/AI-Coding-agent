import httpx


class OllamaClient:
    def __init__(
        self,
        model: str = "qwen3.5:4b",
        base_url: str = "http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url

    def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
        temperature: float = 0.7,
        num_predict: int = 12000,
    ) -> dict:

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict,
            },
        }

        if tools:
            payload["tools"] = tools

        response = httpx.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=180.0,
        )

        response.raise_for_status()

        data = response.json()

        return data["message"]