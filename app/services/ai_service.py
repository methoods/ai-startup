from openai import OpenAI

from app.config import BASE_URL, OPENAI_API_KEY
from app.services.model_selector import ModelSelector


class AIService:

    def __init__(self):
        self.selector = ModelSelector()

    def ask(self, prompt: str) -> str:

        last_error = None

        for _ in range(4):

            model = self.selector.current()

            print(f"\n🤖 Модель: {model}")

            client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=BASE_URL,
            )

            try:

                response = client.chat.completions.create(
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

                self.selector.reset()

                return response.choices[0].message.content or ""

            except Exception as e:

                last_error = e

                print(f"⚠️ {model} недоступна.")
                print("➡️ Переключаемся на следующую модель...")

                self.selector.next()

        return f"❌ Ошибка:\n\n{last_error}"
