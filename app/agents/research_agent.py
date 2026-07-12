import json
import re
from typing import Any

from app.agents.base_agent import BaseAgent
from app.prompts.research import RESEARCH_PROMPT
from app.services.search_service import SearchService


class ResearchAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(RESEARCH_PROMPT)
        self.search_service = SearchService()

    def run(self, goal: str, task: str) -> str:
        query = f"{goal}. {task}"

        try:
            sources = self.search_service.search(query)
        except Exception as error:
            return f"❌ Ошибка интернет-поиска:\n{error}"

        if not sources:
            return "❌ Поиск не нашел источников."

        sources_text = self._build_sources_text(sources)

        prompt = f"""
{self.system_prompt}

Цель пользователя:
{goal}

Текущая задача:
{task}

Найденные источники:

{sources_text}
"""

        response = self.ai_service.ask(prompt)

        if not response:
            return "❌ Модель вернула пустой ответ."

        cleaned_response = self._clean_json(response)

        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError:
            return self._format_fallback(response, sources)

        if not isinstance(data, dict):
            return self._format_fallback(response, sources)

        return self._format_report(data, sources)

    @staticmethod
    def _build_sources_text(
        sources: list[dict[str, str]],
    ) -> str:
        blocks: list[str] = []

        for index, source in enumerate(sources, start=1):
            blocks.append(
                f"""
Источник [{index}]
Название: {source["title"]}
URL: {source["url"]}
Содержание:
{source["content"]}
""".strip()
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _clean_json(response: str) -> str:
        text = response.strip()

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(r"\s*```$", "", text)

        first_brace = text.find("{")
        last_brace = text.rfind("}")

        if first_brace != -1 and last_brace != -1:
            text = text[first_brace:last_brace + 1]

        return text.strip()

    def _format_report(
        self,
        data: dict[str, Any],
        sources: list[dict[str, str]],
    ) -> str:
        sections = [
            ("summary", "📌 Краткое описание"),
            ("market", "📈 Рынок"),
            ("audience", "👥 Целевая аудитория"),
            ("competitors", "🏆 Конкуренты"),
            ("strengths", "✅ Сильные стороны"),
            ("weaknesses", "❌ Слабые стороны"),
            ("opportunities", "🚀 Возможности"),
            ("risks", "⚠️ Риски"),
            ("recommendations", "💡 Рекомендации"),
            ("conclusion", "📋 Итог"),
        ]

        report: list[str] = []

        for key, title in sections:
            value = data.get(key)

            if value in (None, "", []):
                continue

            report.append(title)
            report.append(self._format_value(value))
            report.append("")

        report.append("🔗 Источники")

        for index, source in enumerate(sources, start=1):
            report.append(
                f'[{index}] {source["title"]}\n{source["url"]}'
            )

        return "\n\n".join(report).strip()

    @staticmethod
    def _format_value(value: Any) -> str:
        if isinstance(value, list):
            return "\n".join(f"• {item}" for item in value)

        if isinstance(value, dict):
            return "\n".join(
                f"• {key}: {item}"
                for key, item in value.items()
            )

        return str(value)

    def _format_fallback(
        self,
        response: str,
        sources: list[dict[str, str]],
    ) -> str:
        report = [
            "⚠️ Модель вернула ответ не в формате JSON.",
            "",
            response.strip(),
            "",
            "🔗 Источники",
        ]

        for index, source in enumerate(sources, start=1):
            report.append(
                f'[{index}] {source["title"]}\n{source["url"]}'
            )

        return "\n\n".join(report)
