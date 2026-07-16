import re


class FinancialExtractor:

    MAX_LINES = 30

    KEYWORDS = (
        "аренд",
        "зарплат",
        "средний чек",
        "чек",
        "оборуд",
        "касс",
        "витрин",
        "холодиль",
        "налог",
        "пошлин",
        "регистрац",
        "лиценз",
        "выруч",
        "прибыл",
        "окуп",
        "расход",
        "capex",
        "opex",
        "клиент",
        "трафик",
    )

    def extract(self, text: str) -> str:

        result = []
        seen = set()

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            low = line.lower()

            if not any(word in low for word in self.KEYWORDS):
                continue

            line = re.sub(r"\s+", " ", line)

            if line in seen:
                continue

            seen.add(line)
            result.append(line)

            if len(result) >= self.MAX_LINES:
                break

        return "\n".join(result)
