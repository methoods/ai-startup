from app.services.country_filter import CountryFilter
from app.services.financial_assumptions import FinancialAssumptions


class FinancialContext:

    def __init__(self):

        self.country_filter = CountryFilter()
        self.assumptions = FinancialAssumptions()

    def build(
        self,
        goal: str,
    ) -> str:

        country = self.country_filter.detect(goal)

        data = self.assumptions.get(country)

        return f"""
Используй только следующие финансовые допущения.

Страна: {country}

Валюта: {data['currency']}

Средний чек:
{data['avg_check'][0]}–{data['avg_check'][1]} {data['currency']}

Аренда:
{data['rent_per_m2'][0]}–{data['rent_per_m2'][1]} {data['currency']} за м²

Средняя зарплата сотрудника:
{data['salary'][0]}–{data['salary'][1]} {data['currency']}

Если точных данных нет —
обязательно пиши "(оценка)".

Запрещено придумывать другую валюту.

Запрещено использовать RUB или ₽ для Беларуси.

Запрещено писать суммы,
не соответствующие указанному диапазону.
"""
