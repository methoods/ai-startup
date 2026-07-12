from app.agents.finance_agent import FinanceAgent
from app.agents.marketing_agent import MarketingAgent
from app.agents.research_agent import ResearchAgent


class Router:
    def __init__(self) -> None:
        self.research_agent = ResearchAgent()
        self.finance_agent = FinanceAgent()
        self.marketing_agent = MarketingAgent()

    def get_agent(self, task: str):
        normalized_task = task.lower()

        if "финанс" in normalized_task:
            return self.finance_agent

        if "маркет" in normalized_task:
            return self.marketing_agent

        return self.research_agent
