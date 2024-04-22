
import json, sys, copy, requests
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
    """Load a JSON Formula from disk"""
    try:
        
        file_name = sys.argv[1] if len(sys.argv) > 1 else file_name
        with open(file_name, "r") as my_file:
            contents = my_file.read()
            return json.loads(contents) # load the JSON Formula into a dict
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


class Formulaic:
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


    def __init__(self, api_key=None, formula_json=None, options=None): 
        # formula_json is actually a dict. CONSIDER RENAMING!
        # Use the default_formula_json template if none is given
        # do we need to deepcopy? 

        if formula_json is None:
           formula_json = copy.deepcopy(Formulaic.default_formula_json)

        if api_key is not None:
            self.api_key = api_key

        # set default options to include base_url
        self.options = {"base_url": "https://formulaic.app/api/"}
        
        # add user options, including overriding base_url. api_key expected
        if options is not None:
            self.options.update(options)

        self.script = formula_json 

     
    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, formula_json):
        if formula_json is not None:
            self._script = formula_json 
            #self.script = formula_json

        # individual properties

        self.name = formula_json.get('name', '')
        self.description = formula_json.get('description', '')
        self.created = formula_json.get('created_at', '')
        self.updated = formula_json.get('updated_at', '')
        self.author = formula_json.get('author', '')  # ['author']
        self.source = formula_json.get ('source') #['source']
        self.license = formula_json.get('license', {}) #['license']['canonical_link']
        self.model = formula_json.get('script', {}).get('model', {}) #['script']['model']
        
        # shortcut because model_id seems useful
        self.model_id = self.model.get('id', '')  #['script']['model']['id']
        self.sequences = formula_json.get('script', {}).get('sequences', []) #['script']['sequences']


        
        # full variables with all attributes
        self.variables = formula_json.get('script', {}).get('variables', {}) #['script']['variables']

        # storedefault variables in simple format. Useful for testing locally
        self.default_values = Formulaic.simple_variables(self.variables)

        # auto-render the default values or fail when they're called before rendering?
        #self.prompts = Formula.render(self.sequences, self.defaults)

    def get_formula(self, formula_id):
        """Get a Formula from the Formulaic API"""
        url = self.options['base_url'] + "recipes/" + formula_id + "/scripts"
        headers = {
            "Accept": "*/*",
            "Authorization": "Bearer " + self.api_key,
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        formula_dict = response.json()
        self.script = formula_dict
        return formula_dict



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
        
        #consider format here -- do we use OpenAI format for messages?
        #think about whether we want to return prompts or set a property
        self.prompts = rendered
  

 

# This allows us to extend templating or replace w/ Jinja2        
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


