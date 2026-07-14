MODELS = [
    "qwen/qwen3-coder:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
]


class ModelSelector:

    def __init__(self):
        self.index = 0

    def current(self) -> str:
        return MODELS[self.index]

    def next(self) -> str:
        if self.index < len(MODELS) - 1:
            self.index += 1
        return MODELS[self.index]

    def reset(self):
        self.index = 0
