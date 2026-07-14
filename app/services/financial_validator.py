import re


class FinancialValidator:

    def validate(self, text: str) -> str:

        replacements = {
            r"250–350 BYN за одну покупку": "25–35 BYN (оценка)",
            r"250-350 BYN за одну покупку": "25–35 BYN (оценка)",
            r"≈\s*\$95.?130": "",
            r"≈\s*\$95–130": "",
        }

        for pattern, value in replacements.items():
            text = re.sub(
                pattern,
                value,
                text,
                flags=re.IGNORECASE,
            )

        return text
