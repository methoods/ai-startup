from urllib.parse import urlparse


class SourceRanker:

    TRUSTED_DOMAINS = {
        "wildberries.by": 100,
        "wildberries.ru": 100,
        "wb.ru": 100,

        "ozon.ru": 100,
        "ozon.by": 100,

        "government.by": 95,
        "gov.by": 95,

        "business.gov.by": 90,

        "2gis.ru": 90,
        "yandex.ru": 90,
        "yandex.by": 90,

        "journal.tinkoff.ru": 80,
        "tbank.ru": 80,

        "vc.ru": 70,
        "rb.ru": 70,

        "youtube.com": 40,
        "pikabu.ru": 20,
    }

    def rank(self, sources: list[dict]) -> list[dict]:

        unique = {}

        for source in sources:

            url = source.get("url", "")

            if url not in unique:
                unique[url] = source

        ranked = list(unique.values())

        ranked.sort(
            key=self.score,
            reverse=True,
        )

        return ranked

    def score(self, source: dict) -> int:

        url = source.get("url", "")

        domain = urlparse(url).netloc.lower()

        domain = domain.replace("www.", "")

        return self.TRUSTED_DOMAINS.get(
            domain,
            10,
        )
