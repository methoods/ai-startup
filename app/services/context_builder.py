class ContextBuilder:

    MAX_CONTENT_LENGTH = 1200

    def build(
        self,
        sources: list[dict],
    ) -> str:

        blocks = []

        for index, source in enumerate(sources, start=1):

            title = source.get("title", "").strip()
            url = source.get("url", "").strip()
            content = source.get("content", "").strip()

            if len(content) > self.MAX_CONTENT_LENGTH:
                content = content[: self.MAX_CONTENT_LENGTH] + "..."

            blocks.append(
                f"""Источник {index}

Название:
{title}

URL:
{url}

Факты:
{content}
"""
            )

        return "\n\n".join(blocks)
