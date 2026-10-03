from agent.llm import OllamaClient
from tools.registry import ToolRegistry


class CodingAgent:
    def __init__(
        self,
        tool_registry: ToolRegistry,
        max_iterations: int = 3,
    ):
        self.llm = OllamaClient()
        self.tools = tool_registry
        self.max_iterations = max_iterations

    def chat(self, message: str) -> str:
        print("\n[frontend] Generating HTML...")

        html = self._generate_html(message)

        if not self._valid_html(html):
            print("[frontend] HTML was incomplete. Regenerating...")
            html = self._generate_html(message)

        if not self._valid_html(html):
            return "HTML generation failed or returned incomplete HTML."

        if not html:
            return "Failed to generate HTML."

        print("[frontend] Generating CSS...")

        css = self._generate_css(message, html)

        if not css:
            return "Failed to generate CSS."

        print("[frontend] Generating JavaScript...")

        js = self._generate_js(message, html)

        if not js:
            return "Failed to generate JavaScript."

        write_file = self.tools.get("write_file")

        if write_file is None:
            return "write_file tool is not available."

        write_file(
            path="index.html",
            content=html,
        )

        write_file(
            path="styles.css",
            content=css,
        )

        write_file(
            path="script.js",
            content=js,
        )

        return (
            "Frontend created successfully.\n\n"
            "Created files:\n"
            "- workspace/index.html\n"
            "- workspace/styles.css\n"
            "- workspace/script.js"
        )

    def _generate_html(self, request: str) -> str:
        prompt = f"""
    Create a complete HTML5 webpage for this request:

    {request}

    IMPORTANT:

    Return ONLY the HTML document.

    The response MUST:
    - Start with <!DOCTYPE html>
    - Contain <html>, <head>, and <body>
    - End with </html>
    - Link to styles.css
    - Load script.js
    - Include all requested sections
    - Include navigation if requested
    - Include buttons, forms, cards, images, and content where appropriate
    - Use semantic HTML
    - Use clear IDs and classes
    - Be responsive through CSS classes
    - Be visually detailed but keep the HTML reasonably compact
    - Use placeholder/public image URLs when images are needed
    - Do NOT include CSS inside <style>
    - Do NOT include JavaScript inside <script>
    - Do NOT use React, Vue, Bootstrap, Tailwind, Node.js, or npm
    - Do NOT use markdown
    - Do NOT explain anything

    The output must be one complete HTML document.
    """

        return self._ask(prompt, "html")



    def _generate_css(self, request: str, html: str) -> str:
        prompt = f"""
You are an expert UI/UX designer and CSS developer.

Create ONLY the complete CSS for this website request:

{request}

Here is the generated HTML:

{html}

Requirements:
- Create a polished, unique visual design matching the user's request.
- Style every important section in the HTML.
- Make it fully responsive for desktop, tablet, and mobile.
- Include hover effects and transitions where appropriate.
- Use modern CSS.
- Do not use frameworks.
- Do not explain anything.
- Return ONLY CSS code.
- Do not use markdown code fences.
"""

        return self._ask(prompt, "css")

    def _generate_js(self, request: str, html: str) -> str:
        prompt = f"""
You are an expert JavaScript frontend developer.

Create ONLY the complete JavaScript for this website:

User request:
{request}

Generated HTML:
{html}

Requirements:
- Add useful interactive behavior appropriate for this website.
- Make navigation work.
- Add mobile menu behavior if a mobile menu exists.
- Add smooth scrolling where appropriate.
- Add form interaction/validation where appropriate.
- Use the actual IDs and classes from the HTML.
- Do not use external JavaScript libraries.
- Do not create backend functionality.
- Do not explain anything.
- Return ONLY JavaScript code.
- Do not use markdown code fences.
"""

        return self._ask(prompt, "javascript")

    def _ask(self, prompt: str, code_type: str) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional frontend code generator. "
                    "Follow the requested output format exactly."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        response = self.llm.chat(messages)

        if not isinstance(response, dict):
            return ""

        content = response.get("content", "")

        if not content:
            return ""

        return self._clean_code(content, code_type)

    def _clean_code(self, content: str, code_type: str) -> str:
        content = content.strip()

        # Remove markdown code fences if the model adds them.
        if content.startswith("```"):
            lines = content.splitlines()

            if lines:
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        # Remove accidental closing fence.
        if content.endswith("```"):
            content = content[:-3].rstrip()

        return content

    def _valid_html(self, html: str) -> bool:
        if not html:
            return False

        required = [
            "<!DOCTYPE html",
            "<html",
            "<head",
            "<body",
            "</body>",
            "</html>",
        ]

        return all(
            item.lower() in html.lower()
            for item in required
        )