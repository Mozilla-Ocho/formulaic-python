import json, sys
from string import Template
import requests


""" 
Formula Class for enabling the opening, parsing of Formulas
Gets them ready to send to various LLMs

This will grow to support system prompts, few shot 
examples, etc. 

Formula Class works with OpenClient, which is a wrapper on top of 
OpenAI and can send our Formula prompts to many LLMs

:render(): Formula method for rendering usable prompts by substituting variable values
into the template placeholders

:inputs(): Helpful CLI tool for testing only. Prompts user for new variables on command line

FormulaTemplate Class - extends Template for basic template rendering of curly
brace tenplates. Consider changing format to support either mustache or 
jinja formats

Helper functions Also contains helper functions for opening json Formula files from disc
And saving processed outputs back to disc
:load_formula(): top-level function to load a Formula from disk.
arg is path+filename (or just filename if in same directory)
:save_output(): saves message output to disk. Expects 2 args
- output: a dictionary reprenting the message thread. This is natively what 
Formula.messages generates
- filepath+filename (or just filename if saving to same directory)



"""


# Helpers
# open and read JSON file passed by CLI, return dict
def load_formula(file_name):
    try:

        file_name = sys.argv[1] if len(sys.argv) > 1 else file_name
        with open(file_name, "r") as my_file:
            contents = my_file.read()
            return json.loads(contents)  # load the JSON Formula into a dict
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# saves our output file to disk
# filename is the full file path to disk plus extension
def save_output(output, filename="export.txt"):
    # convert dict to json string
    json_str = json.dumps(output, indent=4)

    with open(filename, "w") as f:
        f.write(json_str)


class Formula:

    def __init__(self, openClient, script=None, options=None):
        self.openClient = openClient
        if script is not None:
            self._script = script
        if options is not None:
            self.options = options
        else:
            self.options = {baseURL: "https://formulaic.app/api/", apiKey: None}

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, value):
        if value is not None:
            self._script = value

    def get_formula(self, id):
        headers = {"Accept": "*/*", "Authorization": "Bearer " + self.options["apiKey"]}
        url = self.options["baseURL"] + "recipes/" + id + "/scripts"
        response = requests.get(url, headers=headers)
        value = response.json()
        print(value)
        self._script = value
        return value

    @staticmethod
    def simple_variables(data):
        # reformat our variables into k/v pairs for use in the template
        simple_data = {variable["name"]: variable["value"] for variable in data}
        return simple_data

    # renders prompts
    def render(self, simple_data=None):
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

                except:
                    print(
                        f"Templating error, the JSON you submitted has incorrect keys."
                    )

        # think about whether we want to return prompts or set a property
        self.script["script"]["sequences"] = rendered
        # return rendered

    # Convenient for testing user variable inputs in CLI
    # Loops over Formula.variables simple object
    # creates a new

    def inputs(self, variables=None):

        if variables is None:
            variables = self.variables

        new_inputs = variables

        for i in variables:
            answer = input(i["description"] + "\n> ")

            # no validation here...
            i["value"] = answer

        new_inputs = Formula.simple_variables(new_inputs)

        return new_inputs


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
