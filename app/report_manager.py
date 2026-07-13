from pathlib import Path
import json


class ReportManager:

    def __init__(self):

        self.projects = Path("projects")

    def build_business_plan(self, goal: str) -> str:

        project_name = (
            goal.lower()
            .replace(" ", "_")
        )

        project_dir = self.projects / project_name

        project_file = project_dir / "project.json"

        if not project_file.exists():

            return "❌ Проект не найден."

        project = json.loads(
            project_file.read_text(
                encoding="utf-8"
            )
        )

        report = []

        report.append("# БИЗНЕС-ПЛАН")
        report.append("")
        report.append(project["goal"])
        report.append("")
        report.append("---")
        report.append("")

        reports_dir = project_dir / "reports"

        for task in project.get(
            "reports",
            []
        ):

            filename = (
                task.lower()
                .replace(" ", "_")
                + ".md"
            )

            file = reports_dir / filename

            if not file.exists():
                continue

            report.append(f"# {task}")
            report.append("")
            report.append(
                file.read_text(
                    encoding="utf-8"
                )
            )
            report.append("")
            report.append("---")
            report.append("")

        output = (
            project_dir
            / "business_plan.md"
        )

        output.write_text(
            "\n".join(report),
            encoding="utf-8",
        )

        return str(output)
