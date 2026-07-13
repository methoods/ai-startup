from app.prompts.research import RESEARCH_PROMPT
from app.prompts.finance import FINANCE_PROMPT
from app.prompts.marketing import MARKETING_PROMPT
from app.prompts.competitors import COMPETITORS_PROMPT


class PromptFactory:

    @staticmethod
    def get(task: str) -> str:

        task = task.lower()

        if "исследование" in task:
            return RESEARCH_PROMPT

        if "конкурент" in task:
            return COMPETITORS_PROMPT

        if "финанс" in task:
            return FINANCE_PROMPT

        if "требован" in task:
            return RESEARCH_PROMPT

        if "запуск" in task:
            return RESEARCH_PROMPT

        return RESEARCH_PROMPT
