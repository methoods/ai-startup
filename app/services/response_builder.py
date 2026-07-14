class ResponseBuilder:

    def is_truncated(
        self,
        text: str,
    ) -> bool:

        if not text:
            return True

        markers = [
            "</",
            "...",
            "```",
        ]

        if any(text.rstrip().endswith(m) for m in markers):
            return True

        if len(text) > 100 and not text.rstrip().endswith(("}", "]")):
            return True

        return False

    def build_continue_prompt(
        self,
        response: str,
    ) -> str:

        return f"""
Ответ оборвался.

Продолжи с места остановки.

Не повторяй начало.

Верни только продолжение.

{response}
"""
