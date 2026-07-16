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

        finance_rules = ""
        finance_context = ""

        if "финанс" in task.lower():

            finance_rules = self.financial_context.build(goal)

            print("\n💰 Поиск финансовых данных...\n")

            finance_context = self.financial_search.get_context(goal)

        prompt = self._build_prompt(
            goal=goal,
            task=task,
            context=context,
            finance_rules=finance_rules,
            finance_context=finance_context,
        )

        response = self._request(prompt)
        response = self.financial_validator.validate(response)

        data = self.validator.parse(response)

        if not isinstance(data, dict):
            raise RuntimeError(
                "Модель вернула JSON, который не является объектом."
            )

        return self._report(data, sources)

    def _request(self, prompt: str) -> str:

        current_prompt = prompt
        last_response = ""

        for attempt in range(2):

            response = self.ai_service.ask(current_prompt)
            last_response = response

            if self.validator.is_valid(response):
                return response

            print(f"⚠️ Попытка {attempt + 1}: невалидный JSON.")

            current_prompt = f"""
Исправь следующий ответ.

Верни только один корректный JSON-объект.
Не используй Markdown.
Не добавляй пояснения до или после JSON.
Не меняй факты и значения.
Закрой все строки, массивы и фигурные скобки.

Ответ для исправления:

{response}
"""

        raise RuntimeError(
            "Модель дважды вернула невалидный JSON.\n\n"
            f"{last_response}"
        )

    def _build_prompt(
        self,
        goal: str,
        task: str,
        context: str,
        finance_rules: str,
        finance_context: str,
    ) -> str:

        prompt = PromptFactory.get(task)

        sections = [
            prompt,
            f"""
Цель проекта:

{goal}

Задача:

{task}

Контекст исследования:

{context}
""",
        ]

        if finance_rules:
            sections.append(
                f"""
Финансовые ограничения:

{finance_rules}
"""
            )

        if finance_context:
            sections.append(
                f"""
Подтвержденные финансовые факты:

{finance_context}

Правила использования финансовых фактов:

- Не смешивай BYN, RUB, USD, EUR и другие валюты.
- Используй число только вместе с его исходным контекстом.
- Не превращай прибыль в ежемесячный расход.
- Не превращай инвестиции готового бизнеса или франшизы в стоимость оборудования.
- Не используй данные другой страны для проекта в Беларуси.
- При противоречии укажи, что данные противоречивы.
- Если значение нельзя надежно классифицировать, напиши:
  "Недостаточно данных (оценка требуется)".
"""
            )

        return "\n".join(sections)

    def _report(
        self,
        data: dict[str, Any],
        sources: list[dict],
    ) -> str:

        report: list[str] = []

        for key, value in data.items():

            report.append(
                f"## {key.replace('_', ' ').title()}"
            )

            self._format_value(
                value=value,
                report=report,
                level=3,
            )

            report.append("")

        report.append("## Источники")
        report.append("")

        for index, source in enumerate(sources, start=1):

            if not isinstance(source, dict):
                continue

            title = source.get("title", "Без названия")
            url = source.get("url", "")

            report.append(f"[{index}] {title}")

            if url:
                report.append(url)

            report.append("")

        return "\n".join(report)

    def _format_value(
        self,
        value: Any,
        report: list[str],
        level: int,
    ) -> None:

        if isinstance(value, dict):

            for key, nested_value in value.items():

                heading = key.replace("_", " ").title()
                heading_level = min(level, 6)

                report.append(
                    f"{'#' * heading_level} {heading}"
                )

                self._format_value(
                    value=nested_value,
                    report=report,
                    level=heading_level + 1,
                )

            return

        if isinstance(value, list):

            for item in value:

                if isinstance(item, (dict, list)):
                    self._format_value(
                        value=item,
                        report=report,
                        level=level,
                    )
                else:
                    report.append(f"• {item}")

            return

        report.append(str(value))
