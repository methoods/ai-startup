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

        prompt = self._build_prompt(
            goal,
            task,
            sources,
        )

        response = self._request(prompt)

        data = self.validator.parse(response)

        return self._report(
            data,
            sources,
        )

    def _request(
        self,
        prompt: str,
    ) -> str:

        for attempt in range(2):

            response = self.ai_service.ask(prompt)

            if self.validator.is_valid(response):
                return response

            print(
                f"⚠️ Попытка {attempt+1}: невалидный JSON."
            )

            prompt = f"""
Верни только JSON.

Без markdown.

Без пояснений.

{prompt}
"""

        return response

    def _build_prompt(
        self,
        goal: str,
        task: str,
        sources: list[dict],
    ) -> str:

        prompt = PromptFactory.get(task)

        text = ""

        for i, source in enumerate(
            sources,
            start=1,
        ):

            text += f"""

Источник {i}

Название:
{source['title']}

URL:
{source['url']}

Текст:
{source['content']}
"""

        return f"""
{prompt}

Цель:

{goal}

Задача:

{task}

Источники:

{text}
"""

    def _report(
        self,
        data: dict[str, Any],
        sources: list[dict],
    ) -> str:

        report = []

        for key, value in data.items():

            report.append(
                f"## {key.replace('_',' ').title()}"
            )

            if isinstance(value, list):

                if value and isinstance(
                    value[0],
                    dict,
                ):

                    for item in value:

                        report.append("")

                        for k, v in item.items():

                            report.append(
                                f"{k}: {v}"
                            )

                else:

                    for item in value:

                        report.append(
                            f"• {item}"
                        )

            else:

                report.append(str(value))

            report.append("")

        report.append("## Источники")
        report.append("")

        for i, source in enumerate(
            sources,
            start=1,
        ):

            report.append(
                f"[{i}] {source['title']}"
            )

            report.append(
                source["url"]
            )

            report.append("")

        return "\n".join(report)
