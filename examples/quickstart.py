import sys
import json

from formulaic_ai import Formula, load_formula

model_config = {
    "llamafile": {
        "url": "http://localhost:8080/v1",
        "key": "sk-no-key-required",
        "name": "LLaMA_CPP",
    },
    "OpenAI": {
        "url": "https://api.openai.com/v1",
        "key": "OPENAI_KEY_GOES_HERE",
        "name": "gpt-3.5-turbo",
    },
    "mistral7b": {
        "url": "https://api.endpoints.anyscale.com/v1",
        "key": "ANYSCALE_KEY_GOES_HERE",
        "name": "mistralai/Mistral-7B-Instruct-v0.1",
    },
}

# load our Formula, print the Formula name: description
formulaic = Formula()
formulaic.get_formula()  # pass in ID of formula
print(formulaic.script)

# render prompts.
print(f"\nMy starting prompts: {json.dumps(formulaic.script, indent=2)}")


# our new variables here.
data = {
    "value": "What is {{{name}}}?",
    "name": "German",
}


# render and print our prompts
formulaic.render(data)
print(f"\nMy new prompts: {json.dumps(formulaic.script, indent=2)}")


# # Create an OpenClient instance for llamafile
# with OpenClient(my_formula, model_config["llamafile"]) as client:

#     # start our chat. True = print to terminal
#     client.chat(True)

#     # print our message log.
#     print(client.messages)
