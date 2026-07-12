import time

from openai import (
    APIConnectionError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)

from app.config import BASE_URL, MODEL, OPENAI_API_KEY


class AIService:
    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise ValueError(
                "В файле .env отсутствует OPENAI_API_KEY"
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=BASE_URL,
            timeout=60,
            max_retries=0,
        )

    def ask(self, prompt: str) -> str:
        print(f"\n🤖 Используется модель: {MODEL}")
        print("📡 Отправляем запрос...\n")

        attempts = 3

        for attempt in range(1, attempts + 1):
            try:
                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    response_format={
                        "type": "json_object",
                    },
                    temperature=0.1,
                    max_tokens=2200,
                )

                content = response.choices[0].message.content

                if not content:
                    if attempt < attempts:
                        time.sleep(2)
                        continue

                    return "❌ Модель вернула пустой ответ."

                text = str(content).strip()

                service_answers = {
                    "user safety: safe",
                    "safe",
                    "unsafe",
                }

                if text.lower() in service_answers:
                    if attempt < attempts:
                        print(
                            "⚠️ Получен служебный ответ. "
                            "Повторяю запрос..."
                        )
                        time.sleep(2)
                        continue

                    return (
                        "❌ Бесплатная модель вернула "
                        "служебный ответ вместо исследования."
                    )

                return text

            except APIConnectionError:
                if attempt < attempts:
                    print(
                        f"⚠️ Ошибка соединения. "
                        f"Попытка {attempt + 1}/{attempts}..."
                    )
                    time.sleep(3)
                    continue

                return (
                    "❌ Не удалось соединиться с OpenRouter "
                    "после трех попыток."
                )

            except APITimeoutError:
                if attempt < attempts:
                    print(
                        f"⚠️ Превышено время ожидания. "
                        f"Попытка {attempt + 1}/{attempts}..."
                    )
                    time.sleep(3)
                    continue

                return "❌ Сервер не ответил после трех попыток."

            except RateLimitError:
                return (
                    "❌ Бесплатный лимит OpenRouter временно "
                    "исчерпан. Повтори запрос позже."
                )

            except Exception as error:
                return f"❌ Ошибка OpenRouter:\n{error}"

        return "❌ Не удалось получить ответ."