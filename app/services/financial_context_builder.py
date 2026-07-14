from app.services.financial_research_agent import FinancialResearchAgent
from app.services.search_service import SearchService


class FinancialContextBuilder:

    def __init__(self):
        self.agent = FinancialResearchAgent()
        self.search = SearchService()

    def build(self, goal: str) -> str:

        context = []

        for query in self.agent.build_queries(goal):

            print(f"💰 {query}")

            try:
                results = self.search.search(
                    query=query,
                    goal=goal,
                )

            except Exception:
                continue

            if not results:
                continue

            context.append(f"\n### {query}\n")

            for item in results[:3]:

                title = item.get("title", "")
                snippet = item.get("snippet", "")
                url = item.get("url", "")

                context.append(f"• {title}")
                context.append(snippet)
                context.append(url)
                context.append("")

        return "\n".join(context)
