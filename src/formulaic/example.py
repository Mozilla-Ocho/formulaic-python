import json

# THIS SCRIPT WORKS IF YOU ARE DOWNLOADING formulaic.py 
# and openclient.py directly from repo and running this 
# script from the same directory. 

# importing as module files directly from the same directory
from formulaic import Formula, load_formula
from openclient import OpenClient


model_config = { "llamafile" :  {"url" : "http://localhost:8080/v1",
                                 "key":"sk-no-key-required", 
                                 "name": "LLaMA_CPP"}, 
                  "OpenAI" :    {"url" :  "https://api.openai.com/v1",
                                 "key": "OPENAI_KEY_GOES_HERE", 
                                 "name": "gpt-3.5-turbo"},
                  "mistral7b" : {"url" : "https://api.endpoints.anyscale.com/v1",
                                 "key": "ANYSCALE_KEY_GOES_HERE", 
                                 "name": "mistralai/Mistral-7B-Instruct-v0.1"}  
                   
}

# load our Formula
my_formula = Formula(load_formula("motivator.json")) 

print(f"{my_formula.name}: {my_formula.description}")


# render prompts. 
my_formula.render()
print(f"\nMy starting prompts: {my_formula.prompts}")



#our new variables here. 
data = {"occasion": "I'm scared of heights and climbing a mountain", 'language': 'German'}

# render and print our prompts
my_formula.render(data)
print(f"\nMy new prompts: {my_formula.prompts}")


# get new inputs 
#my_formula= my_formula.inputs()


#my_formula.render(my_formula.inputs())

#print(f"My new prompts: {my_formula.prompts}")


client = OpenClient(my_formula, model_config["llamafile"])
#print(model_config["OpenAI"])

#print(formula.model)





#print(formula.prompts)


exit()

client.chat(True)

print(client.me)