from openai import OpenAI

from app.config import BASE_URL, OPENAI_API_KEY
from app.services.model_selector import MODELS


class AIService:

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=BASE_URL,
        )

    def ask(self, prompt: str) -> str:

        errors: list[str] = []

        for model in MODELS:

            print(f"\n🤖 Модель: {model}")

            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    temperature=0.3,
                    max_tokens=1500,
                )

                if not response.choices:
                    raise RuntimeError(
                        "Провайдер вернул ответ без choices."
                    )

                choice = response.choices[0]

                if choice is None:
                    raise RuntimeError(
                        "Провайдер вернул пустой choice."
                    )

                message = getattr(choice, "message", None)

                if message is None:
                    raise RuntimeError(
                        "Провайдер вернул choice без message."
                    )

                content = getattr(message, "content", None)

                if not isinstance(content, str):
                    raise RuntimeError(
                        "Провайдер вернул message без текстового content."
                    )

                content = content.strip()

                if not content:
                    raise RuntimeError(
                        "Модель вернула пустой текст."
                    )

                print(f"✅ Ответ получен: {model}")

                return content

            except Exception as error:

                error_text = f"{model}: {error}"
                errors.append(error_text)

                print(f"⚠️ {model} недоступна или вернула ошибку.")
                print(f"Причина: {error}")
                print("➡️ Переключаемся на следующую модель...")

        details = "\n".join(errors)

        raise RuntimeError(
            "Все модели недоступны или вернули некорректный ответ.\n\n"
            f"{details}"
        )
