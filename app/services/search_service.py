from tavily import TavilyClient

from app.config import TAVILY_API_KEY


class SearchService:
    def __init__(self) -> None:
        if not TAVILY_API_KEY:
            raise ValueError("В файле .env отсутствует TAVILY_API_KEY")

        self.client = TavilyClient(api_key=TAVILY_API_KEY)

    def search(self, query: str) -> list[dict[str, str]]:
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
        )

        sources: list[dict[str, str]] = []

        for item in response.get("results", []):
            sources.append(
                {
                    "title": item.get("title", "Без названия"),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                }
            )

        return sources
