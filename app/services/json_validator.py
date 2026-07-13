import json
import re


class JSONValidator:

    @staticmethod
    def clean(text: str) -> str:

        text = text.strip()

        text = re.sub(
            r"^```json",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = text.replace("```", "")

        first = text.find("{")
        last = text.rfind("}")

        if first != -1 and last != -1:
            text = text[first:last + 1]

        return text.strip()

    @staticmethod
    def is_valid(text: str) -> bool:

        try:
            json.loads(JSONValidator.clean(text))
            return True

        except Exception:
            return False

    @staticmethod
    def parse(text: str) -> dict:

        return json.loads(
            JSONValidator.clean(text)
        )
