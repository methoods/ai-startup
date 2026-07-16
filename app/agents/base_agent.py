from app.core.research_engine import ResearchEngine


class BaseAgent:

    def __init__(self, system_prompt: str) -> None:
        self.engine = ResearchEngine()

    def run(
        self,
        goal: str,
        task: str,
    ) -> str:

        return self.engine.run(
            goal=goal,
            task=task,
        )
