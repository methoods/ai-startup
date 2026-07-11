from ai import ask_ai


class Executor:

    def execute(self, task: str) -> str:

        prompt = f"""
Выполни следующую задачу максимально подробно.

Задача:
{task}
"""

        return ask_ai(prompt)