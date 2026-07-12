from app.agents.base_agent import BaseAgent
from app.prompts.finance import FINANCE_PROMPT


class FinanceAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(FINANCE_PROMPT)
