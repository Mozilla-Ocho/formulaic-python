from formulaic_ai import Formula, load_formula, OpenClient
 


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

# load our Formula, print the Formula name: description
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


# Create an OpenClient instance for llamafile
with OpenClient(my_formula, model_config["llamafile"]) as client:

    # start our chat. True = print to terminal
    client.chat(True)
    
    # print our message log.  
    print(client.messages)