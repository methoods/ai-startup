from typing import Any

from app.prompts.prompt_factory import PromptFactory
from app.services.ai_service import AIService
from app.services.json_validator import JSONValidator
from app.services.search_service import SearchService


class ResearchEngine:
    def __init__(self) -> None:
        self.search_service = SearchService()
        self.ai_service = AIService()
        self.validator = JSONValidator()

    def run(self, goal: str, task: str) -> str:
        print("\n🌍 Поиск актуальных источников...\n")

        try:
            sources = self.search_service.search(
                f"{goal}. {task}"
            )
        except Exception as error:
            return f"❌ Ошибка поиска:\n{error}"

        if not sources:
            return "❌ Источники не найдены."

        prompt = self._build_prompt(
            goal=goal,
            task=task,
            sources=sources,
        )

        response = self._request_valid_json(prompt)

        if response is None:
            return self._build_error_report(sources)

        data = self.validator.parse(response)

        return self._build_report(
            data=data,
            sources=sources,
        )

    def _request_valid_json(
        self,
        prompt: str,
    ) -> str | None:
        current_prompt = prompt

        for attempt in range(1, 3):
            response = self.ai_service.ask(current_prompt)

            if self.validator.is_valid(response):
                return response

            print(
                f"⚠️ Попытка {attempt}: модель вернула невалидный JSON."
            )

            current_prompt = f"""
Исправь предыдущий ответ.

Верни ТОЛЬКО корректный JSON.
Без пояснений.
Без Markdown.

Исходная задача:

{prompt}
"""

        return None

    def _build_prompt(
        self,
        goal: str,
        task: str,
        sources: list[dict[str, str]],
    ) -> str:

        prompt_template = PromptFactory.get(task)

        source_blocks = []

        for index, source in enumerate(sources, start=1):
            source_blocks.append(
                f"""
Источник [{index}]

Название:
{source.get("title","")}

URL:
{source.get("url","")}

Содержание:
{source.get("content","")}
""".strip()
            )

        sources_text = "\n\n".join(source_blocks)

        return f"""
{prompt_template}

Цель пользователя:
{goal}

Текущая задача:
{task}

Источники:
{sources_text}
"""

    def _build_report(
        self,
        data: dict[str, Any],
        sources: list[dict[str, str]],
    ) -> str:

        report = []

        for key, value in data.items():

            title = key.replace("_", " ").title()

            report.append(f"## {title}")

            if isinstance(value, list):

                if value and isinstance(value[0], dict):

                    for i, item in enumerate(value, start=1):

                        report.append(f"\n### {i}")

                        for k, v in item.items():
                            report.append(f"{k}: {v}")

                else:

                    for item in value:
                        report.append(f"• {item}")

            else:

                report.append(str(value))

            report.append("")

        report.append("## Источники\n")

        for i, source in enumerate(sources, start=1):

            report.append(
                f"[{i}] {source['title']}"
            )

            report.append(source["url"])

            report.append("")

        return "\n".join(report)

    @staticmethod
    def _build_error_report(
        sources: list[dict[str, str]],
    ) -> str:

        report = [
            "❌ После двух попыток модель не вернула корректный JSON.",
            "",
            "Источники:",
            "",
        ]

        for i, source in enumerate(sources, start=1):

            report.append(
                f"[{i}] {source['title']}"
            )

            report.append(source["url"])

            report.append("")

        return "\n".join(report)
