from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

 
'''
OpenClient extends OpenAI

Allows us to pass in base endpoint url, key, and  model name
So that Formulaic can use the OpenAI client to send/receive messages
from all OpenAI compliant REST endpoints

send_message() allows us to send a single message, this is called
recursively by both run() and chat()

run() method loops through each prompt in a Formula, awaits server response,
then sends next prompt until complete. It tops once Formula prompts are all sent



chat() method loops through all Formula prompts and then continues with a simple 
CLI chat to continue the chat. If you hit "enter" without inputing data the chat ends

run(), and chat() have a single "printable" argument that defaults to False
Setting it True prints user prompts and assistant responses to command line

'''
 
class OpenClient(OpenAI):
    def __init__(self, formula, model): 
     
        self.base_url = model["url"]
        self.api_key = model["key"]
        self.model = model['name']
        self.prompts = formula.prompts
        self.messages = []
        self.client =  OpenAI(
                        base_url= self.base_url,  
                        api_key = self.api_key
                        )
        

    def send_message(self, message, printable, direct=False):
         # append to messages, print, send it. 
        self.messages.append({"role": "user", "content": message })
        if printable and direct==False:
            print(f"User: {message}\n")

        completion = self.client.chat.completions.create(
        model=self.model,
        messages=self.messages
    )   
        # get clean answer, append it to messages, print 
        answer = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer })

        if printable:
            print(f"Assistant: {answer}\n")



    def run(self, printable=False):
 
        for p in self.prompts:
            self.send_message(p, printable)
            

    def chat(self, printable=False):
        self.run(printable)
        next_message = "a"
        while next_message: 
            next_message = input("> ")
            if next_message:
                self.send_message(next_message, printable, direct=True)
        
