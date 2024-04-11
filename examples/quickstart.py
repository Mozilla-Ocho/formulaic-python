""" Get started very quickly, create a .env file in this directory with the following contents:
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
FORMULAIC_API_KEY=your_formulaic_api_key

Or use any OpenAI compatiable service that can use the openai python client.
Formulaic does not depend on any specific inference provider, for example you can also use 
anyscale, llamafile, or any other provider with minor code tweaks.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from formulaic_ai import Formula, load_formula


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

FORMULAIC_API_KEY = os.getenv("FORMULAIC_API_KEY")


client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)

formulaic = Formula(
    open_client=client,
    model="gpt-3.5-turbo",
    options={"api_key": FORMULAIC_API_KEY},
)

# grab a public formula as an example
formulaic.get_formula("899e3cbb-2887-4646-8e83-b2d319a52441")

# add new values for the variables here.
data = [{"name": "topic", "value": "Turtles"}, {"name": "count", "value": "20"}]


# render and send prompts to LLM
formulaic.run(data)

# create an interactive chat session with the formula (this is a blocking call)
with formulaic.open_client as client:
    formulaic.chat(True, data)
    print(client.messages)
