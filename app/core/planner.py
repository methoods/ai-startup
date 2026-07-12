class Planner:

    def create_plan(self, goal: str) -> list[str]:

        intent = self.detect_intent(goal)

        if intent == "MARKETPLACE":
            return [
                "Исследование спроса",
                "Анализ конкурентов",
                "Финансовая модель",
                "Требования площадки",
                "План запуска"
            ]

        if intent == "BUSINESS":
            return [
                "Исследование рынка",
                "Анализ конкурентов",
                "Финансовая модель",
                "Маркетинговая стратегия",
                "План запуска"
            ]

        if intent == "SAAS":
            return [
                "Исследование рынка",
                "Анализ конкурентов",
                "Проблема пользователей",
                "MVP",
                "Монетизация",
                "План запуска"
            ]

        return [
            "Анализ задачи",
            "Практические рекомендации",
            "План дальнейших действий"
        ]

    def detect_intent(self, goal: str) -> str:

        goal = goal.lower()

        marketplace = [
            "ozon",
            "озон",
            "wildberries",
            "вайлдберриз",
            "wb",
            "маркетплейс",
            "пункт выдачи",
            "пвз"
        ]

        saas = [
            "saas",
            "сервис",
            "ai",
            "ии",
            "стартап",
            "startup",
            "платформа"
        ]

        business = [
            "открыть",
            "открытие",
            "магазин",
            "кофейня",
            "детейлинг",
            "салон",
            "кафе",
            "бизнес"
        ]

        if any(word in goal for word in marketplace):
            return "MARKETPLACE"

        if any(word in goal for word in saas):
            return "SAAS"

        if any(word in goal for word in business):
            return "BUSINESS"

        return "GENERAL"