import json
import sys
from string import Template
import requests
from openclient import OpenClient


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
        print(model)
        self.open_client = OpenClient(open_client, self, model)
        if script is not None:
            self.script = script
        self.model = model
        if options is not None:
            self.options = options
        else:
            self.options = {"base_URL": "https://formulaic.app/api/", "api_key": None}

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

    def run(self):
        """Run the Formula"""
        self.open_client.run()

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
            print(i)

            for prompt in i:

                # turn it into a FormulaTemplate and then substitute the values
                prompt_template = FormulaTemplate(prompt["text"])

                try:
                    rendered.append(prompt_template.substitute(simple_data))

                except KeyError:
                    print(
                        "Templating error, the JSON you submitted has incorrect keys."
                    )

        # think about whether we want to return prompts or set a property
        self.script["script"]["sequences"] = rendered
        # return rendered


class FormulaTemplate(Template):
    delimiter = "{{{"
    idpattern = r"\w+"

    pattern = r"""
    \{{3}                           # matches 3 opening braces 
    (?:                             
      (?P<named>\w+)\}{3}           # a-z, A-Z, 0-9 and _ allowed
      |                             # OR
      (?P<invalid>.+?)\}{3}         # invalid 
    )
    """
