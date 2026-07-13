from app.core.research_engine import ResearchEngine


class ResearchAgent:
    def __init__(self) -> None:
        self.engine = ResearchEngine()

    def run(self, goal: str, task: str) -> str:
        return self.engine.run(goal, task)
