class MemoryModule:
    def __init__(self):
        self.context = []

    def add_context(self, text: str):
        self.context.append(text)

    def get_context(self) -> str:
        return " ".join(self.context)
