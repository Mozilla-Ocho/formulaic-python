""" OpenClient class for interacting with OpenAI-compatible APIs. """


class OpenClient:
    """OpenClient class for interacting with OpenAI-compatible APIs."""

    def __name__(self):
        return "OpenClient"

    def __init__(self, client, formula, model):
        self.formula = formula
        self.messages = []
        print("model", model)
        self.model = model
        self.client = client

    def send_message(self, message, printable=True):
        """append to messages, print, send it."""
        self.messages.append({"role": "user", "content": message})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )

        # get clean answer, append it to messages, print
        answer = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})

        if printable:
            print(f"Assistant: {answer}\n")

        return completion

    def run(
        self,
        printable=True,
    ):
        """Run the prompts and responses."""
        self.messages = []
        prompts = self.formula.script.get("script").get("sequences")

        for p in prompts:
            self.send_message(p, printable)

        if printable:
            print(self.messages)

        return self.messages

    def chat(self, printable=False):
        """Start an interactable chat session on command line"""
        self.messages = []

        self.run(printable)
        next_message = "a"
        while next_message:
            next_message = input("> ")
            if next_message:
                self.send_message(next_message, printable)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.messages.clear()
        # self.prompts.clear()
        print("Exiting OpenClient, clearing state.")
