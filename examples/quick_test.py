""" Get started very quickly, create a .env file in this directory with the following contents:
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
FORMULAIC_API_KEY=your_formulaic_api_key

Or use any OpenAI compatiable service that can use the openai python client.
Formulaic does not depend on any specific inference provider, for example you can also use 
anyscale, llamafile, or any other provider with minor code tweaks.
"""

#import os
#from dotenv import load_dotenv
from formulaic_ai import Formulaic 
import openai


#load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
#FORMULAIC_API_KEY = os.getenv("FORMULAIC_API_KEY")


FORMULAIC_API_KEY = "your_personal_key"




my_formula = Formulaic()

my_formula.get("2968bf58-a231-46ff-99de-923198c3864e", FORMULAIC_API_KEY)




 
# add new values for the variables here.
print (my_formula.script)



new_variables = {"occasion": "I'm scared of heights and climbing a mountain", 'language': 'German'}
my_formula.render(new_variables)

print (my_formula.prompts)


new_variables = {"occasion": "new haircut", 'language': 'Japanese'}
my_formula.render(new_variables)

print (my_formula.prompts)


new_variables = {"occasion": "My birthday", 'language': 'Greek'}
my_formula.render(new_variables)

print (my_formula.prompts)

print (my_formula.script)

exit()



import openai

client = openai.OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)

completion = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
    
    {"role": "user", "content": my_formula.prompts[0]},
]
)

print(completion.choices[0].message.content)