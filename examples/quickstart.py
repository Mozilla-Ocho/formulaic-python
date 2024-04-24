""" 
This example works with any LLM inference API that uses the OpenAI format and
OpenAI Python library

For this demo we've chosen llamafile, which is an LLM that runs on your local 
machine and includes a locally running OpenAI-compatible API endpoint. 

You may substitue in another providersuch as Anyscale or OpenAI by changing 
the values of endpoint_url and inference_api_key.

"""

from formulaic_ai import Formulaic 
import openai


formulaic_api_key = "your_personal_key"
endpoint_url = "http://localhost:8080/v1" # default for llamafile
inference_api_key = "sk-no-key-required"  # substitute if using another service


formula = Formulaic(formulaic_api_key)

formula.get_formula("2968bf58-a231-46ff-99de-923198c3864e")

# print the entire Formula script
print (formula.script)


# new values for the template variables
new_variables = {"occasion": "I'm scared of heights!", 'language': 'German'}

# render prompts by sustituting the new values
formula.render(new_variables)

# print the prompts that contain our new values
print (formula.prompts)

# change values, render, and print the prompts
new_variables = {"occasion": "It's my birthday!", 'language': 'Greek'}
formula.render(new_variables)
print (formula.prompts)


# Send our latest prompts to an OpenAI compatible endpoint

# create an OpenAI client
client = openai.OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)
messages=[]

# iterate over the prompts and send to the model for completions
for p in formula.prompts:
    messages.append({"role": "user", "content": p})
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    # print the user prompt we sent
    print(f"\nUser: {p}")
    # print the Assistant's response
    print(f"\nAssistant: {completion.choices[0].message.content}")