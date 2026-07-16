from app.services.financial_extractor import FinancialExtractor
from app.services.financial_research_agent import FinancialResearchAgent
from app.services.search_service import SearchService


class FinancialContextBuilder:

    MAX_RESULTS_PER_QUERY = 3

    def __init__(self) -> None:
        self.agent = FinancialResearchAgent()
        self.search = SearchService()
        self.extractor = FinancialExtractor()

    def build(self, goal: str) -> str:

        blocks: list[str] = []

        for query in self.agent.build_queries(goal):

            print(f"💰 {query}")

            try:
                results = self.search.search(
                    query=query,
                    goal=goal,
                )
            except Exception as error:
                print(f"⚠️ Финансовый поиск пропущен: {error}")
                continue

            for item in results[: self.MAX_RESULTS_PER_QUERY]:

                content = (
                    item.get("content")
                    or item.get("snippet")
                    or ""
                )

                facts = self.extractor.extract(content)

                if not facts:
                    continue

                title = item.get("title", "").strip()
                url = item.get("url", "").strip()

                blocks.append(f"### Категория поиска: {query}")

                if title:
                    blocks.append(f"Источник: {title}")

                if url:
                    blocks.append(f"URL: {url}")

                blocks.append(facts)
                blocks.append("")

        if not blocks:
            return "Подтвержденные финансовые факты не найдены."

        print("\n✅ Финансовые факты извлечены.\n")

        return "\n".join(blocks)
