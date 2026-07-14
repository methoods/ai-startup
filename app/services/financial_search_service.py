from app.services.financial_context_builder import FinancialContextBuilder


class FinancialSearchService:

    def __init__(self):
        self.builder = FinancialContextBuilder()

    def get_context(
        self,
        goal: str,
    ) -> str:

        print("\n==============================")
        print("💰 Финансовый поиск")
        print("==============================")

        context = self.builder.build(goal)

        print("\n✅ Финансовый контекст собран.\n")

        return context
