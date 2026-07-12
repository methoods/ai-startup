from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.executor import Executor
from app.core.planner import Planner
from app.storage.project_storage import ProjectStorage


app = FastAPI(title="AI STARTUP")

templates = Jinja2Templates(directory="web/templates")

planner = Planner()
executor = Executor()
storage = ProjectStorage()


def build_context(
    request: Request,
    goal: str = "",
    tasks: list[str] | None = None,
    report: str | None = None,
    selected_task: str | None = None,
) -> dict:
    completed_reports: list[str] = []

    if goal:
        slug = storage.get_slug(goal)
        project = storage.get_project(slug)

        if project:
            completed_reports = project.get("reports", [])

    return {
        "request": request,
        "goal": goal,
        "tasks": tasks,
        "report": report,
        "selected_task": selected_task,
        "projects": storage.list_projects(),
        "completed_reports": completed_reports,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=build_context(request),
    )


@app.post("/projects", response_class=HTMLResponse)
async def create_project(
    request: Request,
    goal: str = Form(...),
):
    clean_goal = goal.strip()

    if not clean_goal:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context=build_context(request),
        )

    storage.create_project(clean_goal)
    tasks = planner.create_plan(clean_goal)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=build_context(
            request=request,
            goal=clean_goal,
            tasks=tasks,
        ),
    )


@app.get("/projects/{slug}", response_class=HTMLResponse)
async def open_project(
    request: Request,
    slug: str,
):
    project = storage.get_project(slug)

    if not project:
        return RedirectResponse(
            url="/",
            status_code=303,
        )

    goal = project["goal"]
    tasks = planner.create_plan(goal)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=build_context(
            request=request,
            goal=goal,
            tasks=tasks,
        ),
    )


@app.post("/execute", response_class=HTMLResponse)
async def execute_task(
    request: Request,
    goal: str = Form(...),
    task: str = Form(...),
):
    clean_goal = goal.strip()
    clean_task = task.strip()

    tasks = planner.create_plan(clean_goal)

    try:
        report = executor.execute(
            clean_goal,
            clean_task,
        )

        if not report:
            report = "❌ Модель вернула пустой ответ."

        storage.save_report(
            goal=clean_goal,
            task=clean_task,
            report=report,
        )

    except Exception as error:
        report = f"❌ Ошибка:\n\n{error}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=build_context(
            request=request,
            goal=clean_goal,
            tasks=tasks,
            report=report,
            selected_task=clean_task,
        ),
    )


@app.get(
    "/projects/{slug}/reports/{task}",
    response_class=HTMLResponse,
)
async def open_report(
    request: Request,
    slug: str,
    task: str,
):
    project = storage.get_project(slug)

    if not project:
        return RedirectResponse(
            url="/",
            status_code=303,
        )

    goal = project["goal"]
    tasks = planner.create_plan(goal)
    report = storage.read_report(slug, task)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=build_context(
            request=request,
            goal=goal,
            tasks=tasks,
            report=report or "Отчет не найден.",
            selected_task=task,
        ),
    )