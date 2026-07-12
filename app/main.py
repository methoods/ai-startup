from app.core.executor import Executor
from app.core.planner import Planner
from app.storage.project_storage import ProjectStorage
from app.storage.report_storage import ReportStorage


planner = Planner()
executor = Executor()

project_storage = ProjectStorage()
report_storage = ReportStorage()


print("=" * 50)
print("🚀 AI STARTUP")
print("=" * 50)

projects = project_storage.list_projects()

if projects:

    print("\nВаши проекты:\n")

    for i, project in enumerate(projects, start=1):
        print(f"{i}. {project['goal']}")

print("\nN - Новый проект")

choice = input("\nВыбор: ").strip().lower()

if choice == "n" or not projects:

    goal = input("\n🎯 Новая цель:\n> ")

else:

    goal = projects[int(choice) - 1]["goal"]

project_storage.create_project(goal)

tasks = planner.create_plan(goal)

print("\n📋 План:\n")

for i, task in enumerate(tasks, start=1):
    print(f"{i}. {task}")

while True:

    choice = input(f"\nВведите номер задачи (1-{len(tasks)}) или q: ")

    if choice.lower() == "q":
        break

    if not choice.isdigit():
        continue

    number = int(choice)

    if number < 1 or number > len(tasks):
        continue

    task = tasks[number - 1]

    print(f"\n⏳ {task}...\n")

    result = executor.execute(goal, task)

    print(result)

    report_storage.save(
        goal=goal,
        task=task,
        report=result
    )

    project_storage.save_report(
        goal,
        task,
        result
    )