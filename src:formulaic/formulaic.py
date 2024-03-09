
import json, sys
from string import Template


''' 
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



'''


# Helpers
# open and read JSON file passed by CLI, return dict
def load_formula(file_name):
    try:
        
        file_name = sys.argv[1] if len(sys.argv) > 1 else file_name
        with open(file_name, "r") as my_file:
            contents = my_file.read()
            return json.loads(contents) # load the JSON Formula into a dict
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# saves our output file to disk 
# filename is the full file path to disk plus extension
def save_output(output, filename='export.txt'):
    # convert dict to json string
    json_str = json.dumps(output, indent=4)

    with open(filename, 'w') as f:
        f.write(json_str)
    


class Formula:
    # blank Formula for embedded publishing in apps
    default_formula_json = {
        'name': '',
        'description': '',
        'created_at': '',
        'updated_at': '',
        'author': '',
        'source': '',
        'license': {'name': '','canonical_link': ''},
        'script': {
            'model': {'id': '', 'name': '', 'vendor': '', 'provider': ''},
            'sequences': [],
            'variables': {}
        }
    }

    
    def __init__(self, formula_json=None): 
        # formula_json is actually a dict. CONSIDER RENAMING!
        # Use the default_formula_json template if none is given
        if formula_json is None:
            formula_json = Formula.default_formula_json        
        
        # store the json as a hack for republishing, to be implemented later
        self.formula_json = formula_json

        # individual properties
        self.name = formula_json.get('name', '')
        self.description = formula_json.get('description', '')  
        self.author = formula_json.get('author', '')  # ['author']
        self.source = formula_json.get ('source') #['source']
        self.license = formula_json.get('license', {}).get('canonical_link', '') #['license']['canonical_link']
        self.model = formula_json.get('script', {}).get('model', {}) #['script']['model']
        self.model_id = self.model.get('id', '') #['script']['model']['id']
        self.sequences = formula_json.get('script', {}).get('sequences', []) #['script']['sequences']

        
        # full variables with all attributes
        self.variables = formula_json.get('script', {}).get('variables', {}) #['script']['variables']

        # storedefault variables in simple format. Useful for testing locally
        self.default_values = Formula.simple_variables(self.variables)

        # auto-render the default values or fail when they're called before rendering?
        #self.prompts = Formula.render(self.sequences, self.defaults)


    @staticmethod 
    def simple_variables(data):
        # reformat our variables into k/v pairs for use in the template
        simple_data = {variable['name']: variable['value'] for variable in data}
        return simple_data
    
    #renders prompts
    def render(self, simple_data=None):    
        
        # if we don't get new values, use the defaults
        if simple_data is None:
            simple_data = self.default_values

        rendered = []

        # render our template, substituting the values  

        for i in self.sequences:
            # each prompt in the sequence
            for prompt in i:
        
                # turn it into a FormulaTemplate and then substitute the values
                prompt_template = FormulaTemplate(prompt["text"])

                try:
                    rendered.append(prompt_template.substitute(simple_data))

                except:
                    print(f"Templating error, the JSON you submitted has incorrect keys.")
        
        #think about whether we want to return prompts or set a property
        self.prompts = rendered
        #return rendered

    # Convenient for testing user variable inputs in CLI
    # Loops over Formula.variables simple object
    # creates a new

    def inputs(self, variables=None):

        if variables is None:
            variables = self.variables 

        new_inputs = variables

        for i in variables:
            answer = input(i['description'] + "\n> ")

            # no validation here...
            i['value'] = answer

        new_inputs = Formula.simple_variables(new_inputs)

        return new_inputs



        
class FormulaTemplate(Template):
    delimiter = '{{{'
    idpattern = r'\w+'
    
    pattern = r'''
    \{{3}                           # matches 3 opening braces 
    (?:                             
      (?P<named>\w+)\}{3}           # a-z, A-Z, 0-9 and _ allowed
      |                             # OR
      (?P<invalid>.+?)\}{3}         # invalid 
    )
    '''


