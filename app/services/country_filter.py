class CountryFilter:

    COUNTRIES = {
        "belarus": [
            "беларус",
            "минск",
            "брест",
            "гомель",
            "гродно",
            "витебск",
            "могилев",
            "могилёв",
            "баранович",
            ".by",
        ],
        "russia": [
            "росси",
            "москва",
            "санкт",
            "петербург",
            ".ru",
        ],
        "kazakhstan": [
            "казахстан",
            "алматы",
            "астана",
            ".kz",
        ],
    }

    def detect(self, text: str) -> str:

        text = text.lower()

        for country, keywords in self.COUNTRIES.items():

            for keyword in keywords:

                if keyword in text:
                    return country

        return "unknown"
