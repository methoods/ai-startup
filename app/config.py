import os

from dotenv import load_dotenv


load_dotenv()


def get_env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)

    if not value:
        return ""

    return value.strip().strip('"').strip("'")


OPENAI_API_KEY = get_env("OPENAI_API_KEY")
BASE_URL = get_env(
    "BASE_URL",
    "https://openrouter.ai/api/v1",
)
MODEL = get_env(
    "MODEL",
    "openrouter/free",
)
TAVILY_API_KEY = get_env("TAVILY_API_KEY")


if OPENAI_API_KEY and not OPENAI_API_KEY.isascii():
    raise ValueError(
        "OPENAI_API_KEY содержит русские или другие "
        "недопустимые символы. Проверь файл .env."
    )

if TAVILY_API_KEY and not TAVILY_API_KEY.isascii():
    raise ValueError(
        "TAVILY_API_KEY содержит русские или другие "
        "недопустимые символы. Проверь файл .env."
    )