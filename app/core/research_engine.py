from typing import Any

from app.prompts.prompt_factory import PromptFactory
from app.services.ai_service import AIService
from app.services.context_builder import ContextBuilder
from app.services.financial_context import FinancialContext
from app.services.financial_search_service import FinancialSearchService
from app.services.financial_validator import FinancialValidator
from app.services.json_validator import JSONValidator
from app.services.search_service import SearchService


class ResearchEngine:

    def __init__(self) -> None:
        self.search_service = SearchService()
        self.ai_service = AIService()
        self.validator = JSONValidator()
        self.context_builder = ContextBuilder()
        self.financial_context = FinancialContext()
        self.financial_search = FinancialSearchService()
        self.financial_validator = FinancialValidator()

    def run(
        self,
        goal: str,
        task: str,
    ) -> str:

        print("\n🌍 Поиск актуальных источников...\n")

        sources = self.search_service.search(
            query=f"{goal}. {task}",
            goal=goal,
        )

        context = self.context_builder.build(sources)
        finance_rules = self.financial_context.build(goal)

        finance_context = ""

        if "финанс" in task.lower():
            print("\n💰 Поиск финансовых данных...\n")
            finance_context = self.financial_search.get_context(goal)

        prompt = self._build_prompt(
            goal,
            task,
            context,
            finance_rules,
            finance_context,
        )

        response = self._request(prompt)
        response = self.financial_validator.validate(response)

        data = self.validator.parse(response)

        return self._report(data, sources)

    def _request(self, prompt: str) -> str:

        current_prompt = prompt

        for attempt in range(2):

            response = self.ai_service.ask(current_prompt)

            if self.validator.is_valid(response):
                return response

            print(f"⚠️ Попытка {attempt + 1}: невалидный JSON.")

            current_prompt = f"""
Верни только корректный JSON.

Не меняй содержание.

Исправь только формат.

{response}
"""

        return response

    def _build_prompt(
        self,
        goal: str,
        task: str,
        context: str,
        finance_rules: str,
        finance_context: str,
    ) -> str:

        prompt = PromptFactory.get(task)

        return f"""
{prompt}

Цель проекта:

{goal}

Задача:

{task}

Контекст исследования:

{context}

Финансовые ограничения:

{finance_rules}

Дополнительные финансовые данные:

{finance_context}
"""

    def _report(
        self,
        data: dict[str, Any],
        sources: list[dict],
    ) -> str:

        report = []

        for key, value in data.items():

            report.append(f"## {key.replace('_', ' ').title()}")

            if isinstance(value, list):

                if value and isinstance(value[0], dict):

                    for item in value:
                        report.append("")

                        for k, v in item.items():
                            report.append(f"{k}: {v}")

                else:

                    for item in value:
                        report.append(f"• {item}")

            else:
                report.append(str(value))

            report.append("")

        report.append("## Источники")
        report.append("")

        for i, source in enumerate(sources, start=1):
            report.append(f"[{i}] {source['title']}")
            report.append(source["url"])
            report.append("")

        return "\n".join(report)
