from app.agents.base_agent import BaseAgent
from app.prompts.marketing import MARKETING_PROMPT


class MarketingAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(MARKETING_PROMPT)
