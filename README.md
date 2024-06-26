# Formulaic Python Library 
_**NOTE: This is a project in active development and changes frequently. It is not yet intended for production use.**_

The [Formulaic Python library](https://github.com/Mozilla-Ocho/formulaic-python) makes it easy to use Formulas inside your generative AI applications. Formulas are open-licensed JSON scripts that contain AI prompts, template variables, and model configuration.  You can browse the library of existing Formulas for many popular language models at [Formulaic.app](https://formulaic.app). 

## Installation

Install the Formulaic Python library

```python
pip install formulaic-ai
```

## Quick Start
We're going to build [this script](https://github.com/Mozilla-Ocho/formulaic-python/blob/main/examples/quickstart.py) step-by-step below, using a [Formula JSON file](https://github.com/Mozilla-Ocho/formulaic-python/blob/main/examples/motivator.json) we downloaded from [Formulaic.app](http://formulaic.app). If you download both this script and the JSON file to your working directory, you can run them right away. You will need a  llamafile server running at `localhost:8080`. You can also substitute in an  OpenAI key and get going that way. We're going to break the entire thing down step-by-step in a moment. 

```python
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
```

## Step-by-step

### Do our imports

Import `Formula` which is what we'll use to work with our Formulas, `OpenClient` a wrapper on the OpenAI library to make it seamless to send Formula prompts to any OpenAI compatible API, and a helper function `load_formula` to open Formula files. 

```python
from formulaic_ai import Formula, OpenClient, load_formula
```

### Load and create our Formula instance
All Formulas on [Formulaic.app](https://formulaic.app) are JSON files that you can download to your local machine. We're providing one called `motivator.json` for you to use for this tutorial, which you can [download here](https://github.com/Mozilla-Ocho/formulaic-python/blob/main/examples/motivator.json). 

- Run `load_formula()` with a single argument of the the filepath+filename to `motivator.json`. That opens the Formula's JSON file and loads it into a Python dictionary
- Create an instance of the `Formula` class by passing it the dictionary we just created. I combined these two steps and saved my `Formula` instance as `my_formula`
- Now let's print the Formula name and description.
  
```python
# load our Formula
my_formula = Formula(load_formula("motivator.json")) 

print(f"{my_formula.name}: {my_formula.description}")

```
We see:

```
Daily Motivator: Generates a motivational slogan based on your occasion.
```

### Render prompts
Our Formula is loaded correctly. Now let's call the `.render()` method. Downloaded Formula prompts often contain templating variables. When we render, we replace the template variables with values and generate prompts that are stored in the `.prompts` property. If we don't pass new values to `.render()`, it will render prompts using the Formula's default values. Render and then print again. 

```python
# render prompts. 
my_formula.render()
print(f"\nMy starting prompts: {my_formula.prompts}")
```
Printed in the terminal we see we see: 

```
My starting prompts: ['You are a personal motivator assistant who is direct and 
believes that everyone can be their best. Generate a motivating slogan for the 
occasion of first day of a new job', 'Now translate that slogan into French ']
```
Our prompts are in a Python list. The occasion is "first day of a new job" and the "French". 

Now let's pass in new data, re-render our prompts, and print again.
```python
#our new variables here. 
data = {"occasion": "I'm scared of heights and climbing a mountain", 'language': 'German'}

# render and print our prompts
my_formula.render(data)
print(f"\nMy new prompts: {my_formula.prompts}")
```
Now we see our prompt list, available at `.prompts` contains the new occasion and new translation language.

```
My new prompts: ["You are a personal motivator assistant who is direct and 
believes that everyone can be their best. Generate a motivating slogan for 
the occasion of I'm scared of heights and climbing a mountain", 'Now 
translate that slogan into German']
```

### Setup our model endpoint configuration
We have prompts that are ready to be sent off to a language model. I'm going to use llamafile for this tutorial. [llamafile](https://github.com/Mozilla-Ocho/llamafile) is free, runs on your local machine, and makes it easy to deploy a local API endpoint. I chose the [mistral 7B instruct llamafile](https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile). To get it running, download the file (5GB) and run it from the command line to start the local HTTP server. Please see the full [llamafile documentation](https://github.com/Mozilla-Ocho/llamafile) for instructions on how to download and get started. 


I went ahead and created a `model_config` dictionary to hold my model config variables to make it simpler. We can use the Formulaic Library to send our prompts to any language model API that supports the OpenAI format, so I included OpenAI and Anyscale. Anyscale provides hosting for many open source language models with an OpenAI compatible endpoint. You would have to create keys for OpenAI and Anyscale and substitute them in below. 

```python

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
```

### Create our OpenClient and start our chat
Now we're ready to create our `OpenClient` instance, which is a class that extends `OpenAI`. 

* We call `OpenClass` and pass two arguments:
    - The first is our Formula, `my_formula`.
    -  The second is a dictionary that contains valid values for the `url`, `key`, and `name` of the model endpoing we're going to use. In this case, we pass it the `llamafile` dictionary from our `model_config`.

We're going to call it using a `with` statement so that OpenClient's context manager will clean up for us:

```python
with OpenClient(my_formula, model_config["llamafile"]) as client:

```

We now have two options. We can just iterate over the 2 prompts we have in our Formula and await their responses. We do that by calling `.run()`. Instead, we are going to have an ongoing chat by calling `.chat()`. Both `.run` and `.chat` have a single optional argument to print out all user propmts and assistant responses to terminal. The default is `False` but we are using the command line to iteract, so we pass `True`

```python
client.chat(True)
```

And we're also going to add `print(client.messages)` so that we can see the full list of all messages we sent to the model and the model sent back. Our whole block looks like this:

```python
# Create an OpenClient instance for llamafile
with OpenClient(my_formula, model_config["llamafile"]) as client:

    # start our chat. True = print to terminal
    client.chat(True)
    
    # print our message log.  
    print(client.messages)

```

## Save and run the script

We save it as `quickstart.py` and run it in the terminal

```
python quickstart.py

```



It takes a moment because we're running on our local hardware using llamafile. Here's what we see:

```
User: You are a personal motivator assistant who is direct and believes that 
everyone can be their best. Generate a motivating slogan for the occasion of 
I'm scared of heights and climbing a mountain

Assistant: Absolutely, I understand that fear of heights can be a significant 
challenge. But remember, every mountain peak is within your reach if you believe 
in yourself and take it one step at a time. Here's a motivating slogan for you:

"Conquer the Mountain Within: Your Fear is Just a Stepping Stone to New Heights!"

User: Now translate that slogan into German

Assistant: Of course! The German translation of "Conquer the Mountain Within: 
Your Fear is Just a Stepping Stone to New Heights!" would be:

"Berge Innerhalb von Dir besiegen: Deine Angst ist nur ein Stufenstein zu 
neuen Gipfeln!"

> 
```

Notice that we have iterated over both of our two prompts and received two answers from the llamafile model. The cursor is awaiting our input. Let's tell it to translate to Latin and hit Return. 

```
> Now translate to Latin
Assistant: In Latin, the phrase could be:

"Montes Intus Vincere: Timor Tuum Nec Nisi Gradus Ad Novos Culmines!"

> 
```
We see the Latin translation from the local llamafile model, and the cursor aways our next chat input. To stop the chat, just hit Return without entering any input and the loop exits. 


### See the message log printed
Our Formula instance saved every message we sent to the model and every message the assistant sent back. This is what we accessed above by printing `client.messages`


and now we see:
```
[{'role': 'user', 'content': "You are a personal motivator assistant who is 
direct and believes that everyone can be their best. Generate a motivating 
slogan for the occasion of I'm scared of heights and climbing a mountain"}, 
{'role': 'assistant', 'content': 'Absolutely, I understand that fear of heights 
can be a significant challenge. But remember, every mountain peak is within your 
reach if you believe in yourself and take it one step at a time. Here\'s a 
motivating slogan for you:\n\n"Conquer the Mountain Within: Your Fear is 
Just a Stepping Stone to New Heights!"'}, {'role': 'user', 'content': 'Now 
translate that slogan into German'}, {'role': 'assistant', 'content': 'Of course! 
The German translation of "Conquer the Mountain Within: Your Fear is Just a Stepping 
Stone to New Heights!" would be:\n\n"Berge Innerhalb von Dir besiegen: Deine Angst 
\ist nur ein Stufenstein zu neuen Gipfeln!"'}, {'role': 'user', 'content': 'Now 
translate to Latin'}, {'role': 'assistant', 'content': 'In Latin, the phrase could 
be:\n\n"Montes Intus Vincere: Timor Tuum Nec Nisi Gradus Ad Novos Culmines!"'}]

```

That's the gist! You've parsed your first Formula and sent it off to a local language model. You can send it off to other model endpoints just as easily.  

You can see [the entire script](https://github.com/Mozilla-Ocho/formulaic-python/blob/main/examples/quickstart.py) we just produced here. 

