from tavily import TavilyClient

from app.config import TAVILY_API_KEY
from app.services.source_ranker import SourceRanker


class SearchService:

    def __init__(self):
        self.client = TavilyClient(api_key=TAVILY_API_KEY)
        self.ranker = SourceRanker()

    def search(
        self,
        query: str,
        goal: str = "",
    ) -> list[dict]:

        print("\n==============================")
        print("🔍 Поисковый запрос:")
        print(query)
        print("==============================\n")

        result = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=10,
        )

        sources = []

        for item in result.get("results", []):

            sources.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                }
            )

        sources = self.ranker.rank(
            sources=sources,
            goal=goal,
        )

        print("✅ После фильтрации:\n")

        for item in sources:
            print(f"• {item['title']}")
            print(item["url"])
            print()

        return sources
