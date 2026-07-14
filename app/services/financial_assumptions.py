class FinancialAssumptions:

    DATA = {
        "belarus": {
            "currency": "BYN",
            "avg_check": (20, 35),
            "rent_per_m2": (15, 35),
            "salary": (1200, 1800),
        },
        "russia": {
            "currency": "RUB",
            "avg_check": (400, 900),
            "rent_per_m2": (800, 2500),
            "salary": (50000, 90000),
        },
        "kazakhstan": {
            "currency": "KZT",
            "avg_check": (3500, 7000),
            "rent_per_m2": (5000, 12000),
            "salary": (250000, 450000),
        },
    }

    def get(
        self,
        country: str,
    ) -> dict:

        return self.DATA.get(
            country,
            self.DATA["belarus"],
        )
