import json
import re
from pathlib import Path


class ProjectStorage:
    def __init__(self) -> None:
        self.projects_dir = Path("projects")
        self.projects_dir.mkdir(exist_ok=True)

    def list_projects(self) -> list[dict]:
        projects: list[dict] = []

        for project_dir in sorted(self.projects_dir.iterdir()):
            if not project_dir.is_dir():
                continue

            project_file = project_dir / "project.json"

            if not project_file.exists():
                continue

            try:
                data = json.loads(
                    project_file.read_text(encoding="utf-8")
                )
            except (json.JSONDecodeError, OSError):
                continue

            data["slug"] = project_dir.name
            projects.append(data)

        return projects

    def get_project(self, slug: str) -> dict | None:
        project_file = self.projects_dir / slug / "project.json"

        if not project_file.exists():
            return None

        try:
            data = json.loads(
                project_file.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            return None

        data["slug"] = slug
        return data

    def create_project(self, goal: str) -> Path:
        project_dir = self.projects_dir / self._slug(goal)
        reports_dir = project_dir / "reports"

        reports_dir.mkdir(parents=True, exist_ok=True)

        project_file = project_dir / "project.json"

        if not project_file.exists():
            data = {
                "goal": goal,
                "status": "active",
                "reports": [],
            }

            project_file.write_text(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=4,
                ),
                encoding="utf-8",
            )

        return project_dir

    def save_report(
        self,
        goal: str,
        task: str,
        report: str,
    ) -> Path:
        project_dir = self.create_project(goal)
        reports_dir = project_dir / "reports"

        report_file = reports_dir / f"{self._slug(task)}.md"

        report_file.write_text(
            report,
            encoding="utf-8",
        )

        project_file = project_dir / "project.json"

        data = json.loads(
            project_file.read_text(encoding="utf-8")
        )

        if task not in data["reports"]:
            data["reports"].append(task)

        project_file.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )

        return report_file

    def read_report(
        self,
        slug: str,
        task: str,
    ) -> str | None:
        report_file = (
            self.projects_dir
            / slug
            / "reports"
            / f"{self._slug(task)}.md"
        )

        if not report_file.exists():
            return None

        return report_file.read_text(encoding="utf-8")

    def get_slug(self, goal: str) -> str:
        return self._slug(goal)

    @staticmethod
    def _slug(text: str) -> str:
        normalized = text.lower().strip()

        normalized = re.sub(
            r"[^a-zA-Zа-яА-ЯёЁ0-9]+",
            "_",
            normalized,
        )

        return normalized.strip("_")