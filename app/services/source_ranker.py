from app.services.country_filter import CountryFilter


class SourceRanker:

    PRIORITY = [
        ".gov.by",
        ".gov",
        ".edu",
        ".org",
        ".by",
        ".ru",
        ".kz",
    ]

    BLOCKED = [
        "wiktionary.org",
        "wikipedia.org",
        "cooljugator.com",
        "youtube.com",
        "youtu.be",
        "tiktok.com",
        "instagram.com",
        "facebook.com",
        "vk.com",
        "ok.ru",
        "mail.ru",
        "otvet.mail.ru",
    ]

    BLOCKED_WORDS = [
        "викисловар",
        "wiktionary",
        "википед",
        "wikipedia",
        "conjugation",
        "спряжение",
        "склонение",
        "открыть —",
    ]

    def __init__(self) -> None:
        self.country_filter = CountryFilter()

    def rank(
        self,
        sources: list[dict],
        goal: str = "",
    ) -> list[dict]:

        country = self.country_filter.detect(goal)

        unique = []
        seen = set()

        for source in sources:

            url = source.get("url", "").strip().lower()
            title = source.get("title", "").strip().lower()

            if not url:
                continue

            if any(domain in url for domain in self.BLOCKED):
                continue

            if any(word in title for word in self.BLOCKED_WORDS):
                continue

            if url in seen:
                continue

            seen.add(url)
            unique.append(source)

        def score(source: dict) -> tuple[int, int]:

            url = source.get("url", "").lower()

            local_bonus = 1

            if country == "belarus" and ".by" in url:
                local_bonus = 0

            elif country == "russia" and ".ru" in url:
                local_bonus = 0

            elif country == "kazakhstan" and ".kz" in url:
                local_bonus = 0

            priority = 999

            for index, domain in enumerate(self.PRIORITY):
                if domain in url:
                    priority = index
                    break

            return (local_bonus, priority)

        return sorted(
            unique,
            key=score,
        )
