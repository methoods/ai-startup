from app.core.router import Router


class Executor:
    def __init__(self) -> None:
        self.router = Router()

    def execute(self, goal: str, task: str) -> str:
        agent = self.router.get_agent(task)
        return agent.run(goal, task)
