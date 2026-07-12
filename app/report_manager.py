from pathlib import Path
from datetime import datetime


class ReportManager:

    def save(self, goal: str, report: str):

        Path("reports").mkdir(exist_ok=True)

        filename = (
            goal.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        filepath = Path("reports") / f"{filename}_{now}.md"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {goal}\n\n")
            f.write(report)

        return filepath