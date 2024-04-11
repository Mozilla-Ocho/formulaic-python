""" OpenClient class for interacting with OpenAI-compatible APIs. """


class OpenClient:
    """OpenClient class for interacting with OpenAI-compatible APIs."""

    def __name__(self):
        return "OpenClient"

    def __init__(self, client, formula, model):
        self.formula = formula
        self.responses = []
        self.messages = []
        print("model", model)
        self.model = model
        self.client = client

    def send_message(self, message, printable=True, direct=False):
        """append to messages, print, send it."""
        self.messages.append({"role": "user", "content": message})
        print(f"Messages: {self.messages}\n")
        print("Model: ", self.model)
        print(type(self.messages))
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        print(f"completion: {completion}\n")
        # get clean answer, append it to messages, print
        answer = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        self.responses.append(answer)

        if printable:
            print(f"Assistant: {answer}\n")

    def run(
        self,
        printable=True,
    ):
        """Run the prompts and responses."""
        prompts = self.formula.script.get("script").get("sequences")
        for p in prompts:
            self.send_message(p, printable)

    def chat(self, printable=False):
        """Start a chat session."""
        self.run(printable)
        next_message = "a"
        while next_message:
            next_message = input("> ")
            if next_message:
                self.send_message(next_message, printable, direct=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.responses.clear()
        self.messages.clear()
        # self.prompts.clear()
        print("Exiting OpenClient, clearing state.")
