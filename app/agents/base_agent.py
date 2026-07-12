from app.services.ai_service import AIService


class BaseAgent:
    def __init__(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt
        self.ai_service = AIService()

    def run(self, goal: str, task: str) -> str:
        prompt = f"""
{self.system_prompt}

Цель пользователя:
{goal}

Текущая задача:
{task}
"""

        return self.ai_service.ask(prompt)
