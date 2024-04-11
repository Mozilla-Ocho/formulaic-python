import json
import sys
from copy import deepcopy
from string import Template
import requests


def load_formula(file_name):
    """Load a JSON Formula from disk"""
    try:

        file_name = sys.argv[1] if len(sys.argv) > 1 else file_name
        with open(file_name, "r") as my_file:
            contents = my_file.read()
            return json.loads(contents)  # load the JSON Formula into a dict
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def save_output(output, filename="export.txt"):
    """Save output to disk as JSON"""
    json_str = json.dumps(output, indent=4)

    with open(filename, "w") as f:
        f.write(json_str)


class Formula:
    """Formula Class for enabling the opening, parsing of Formulas"""

    def __name__(self):
        return "Formulaic"

    def __init__(self, open_client, script=None, options=None, model=None):
        self.open_client = open_client
        if script is not None:
            self.script = script
        self.model = model
        if options is not None:
            self.options = options
        else:
            self.options = {"base_URL": "https://formulaic.app/api/", "api_key": None}
        self.rendered = None

        self.messages = []

    def get_formula(self, formula_id):
        """Get a Formula from the Formulaic API"""
        headers = {
            "Accept": "*/*",
            "Authorization": "Bearer " + self.options["api_key"],
        }
        url = self.options["base_URL"] + "recipes/" + formula_id + "/scripts"
        response = requests.get(url, headers=headers, timeout=10)
        value = response.json()
        self.script = value
        return value

    @staticmethod
    def simple_variables(data):
        """reformat our variables into k/v pairs for use in the template"""
        simple_data = {variable["name"]: variable["value"] for variable in data}
        return simple_data

    # renders prompts
    def render(self, simple_data=None):
        """Render the Formula prompts with the new values"""
        # if we don't get new values, use the defaults
        if simple_data is None:
            simple_data = self.script.get("script").get("variables")

        rendered = []

        # render our template, substituting the values
        script = self.script.get("script")
        sequences = script.get("sequences")
        for i in sequences:
            # each prompt in the sequence
            for prompt in i:
                temp_prompt = prompt["text"]
                for var in simple_data:
                    name = var["name"]
                    value = var["value"]
                    temp_prompt = temp_prompt.replace("{{{" + name + "}}}", value)
                rendered.append(temp_prompt)
        # think about whether we want to return prompts or set a property
        rendered_formula = deepcopy(self.script)
        rendered_formula["script"]["sequences"] = rendered
        print(rendered_formula)
        return rendered_formula

    def send_message(self, message, printable=True):
        """append to messages, print, send it."""
        self.messages.append({"role": "user", "content": message})
        print("self.messages " + str(self.messages))
        completion = self.open_client.chat.completions.create(
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
        variables=None,
    ):
        """Run the prompts and responses."""
        self.messages = []
        rendered_formula = self.render(variables)
        for p in rendered_formula["script"]["sequences"]:
            self.send_message(p, printable)

        if printable:
            print(self.messages)

        return self.messages

    def chat(
        self,
        printable=False,
        variables=None,
    ):
        """Start an interactable chat session on command line"""
        self.messages = []

        self.run(variables=variables, printable=printable)
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
