import re
from datetime import datetime
from pathlib import Path


class ReportStorage:
    def __init__(self, reports_directory: str = "reports") -> None:
        self.reports_directory = Path(reports_directory)
        self.reports_directory.mkdir(exist_ok=True)

    def save(self, goal: str, task: str, report: str) -> Path:
        safe_goal = self._make_safe_filename(goal)
        safe_task = self._make_safe_filename(task)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{safe_goal}_{safe_task}_{timestamp}.md"
        filepath = self.reports_directory / filename

        content = (
            f"# {goal}\n\n"
            f"## {task}\n\n"
            f"{report}\n"
        )

        filepath.write_text(content, encoding="utf-8")

        return filepath

    @staticmethod
    def _make_safe_filename(value: str) -> str:
        value = value.lower().strip()
        value = re.sub(r"[^\wа-яё-]+", "_", value, flags=re.IGNORECASE)
        return value.strip("_")[:80]
