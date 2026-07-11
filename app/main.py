from core.planner import Planner
from core.executor import Executor

planner = Planner()
executor = Executor()

goal = input("🎯 Какая ваша цель?\n> ")

print("\n📋 План:\n")

tasks = planner.create_plan(goal)

for i, task in enumerate(tasks, start=1):
    print(f"{i}. {task}")

while True:
    choice = input(f"\nВведите номер задачи (1-{len(tasks)}) или q для выхода: ")

    if choice.lower() == "q":
        print("👋 До встречи!")
        break

    if not choice.isdigit():
        print("❌ Введите номер задачи.")
        continue

    number = int(choice)

    if number < 1 or number > len(tasks):
        print("❌ Такой задачи нет.")
        continue

    print(f"\n⏳ Выполняю: {tasks[number - 1]}...\n")

    result = executor.execute(
        f"""
Цель пользователя:
{goal}

Текущая задача:
{tasks[number - 1]}

Выполни ее максимально подробно.
"""
    )

    print("=" * 60)
    print(result)
    print("=" * 60)