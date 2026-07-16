from app.prompts.competitors import COMPETITORS_PROMPT
from app.prompts.finance import FINANCE_PROMPT
from app.prompts.marketing import MARKETING_PROMPT
from app.prompts.research import RESEARCH_PROMPT


class PromptFactory:

    @staticmethod
    def get(task: str) -> str:

        task = task.lower().strip()

        mapping = {
            "финанс": FINANCE_PROMPT,
            "маркет": MARKETING_PROMPT,
            "конкур": COMPETITORS_PROMPT,
            "исслед": RESEARCH_PROMPT,
            "требован": RESEARCH_PROMPT,
            "запуск": RESEARCH_PROMPT,
        }

        for keyword, prompt in mapping.items():
            if keyword in task:
                return prompt

        return RESEARCH_PROMPT
