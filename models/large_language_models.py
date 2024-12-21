from huggingface_hub import InferenceClient
import os
from helpers.utils import read_file

class Agent:
    def __init__(self, model_name=None, temperature=0.2, max_tokens=500, top_p=0.7, extra_parameters = None):
        self.model_name = model_name or os.getenv('MODEL_NAME') or "meta-llama/Llama-3.2-3B-Instruct"
        self.client = InferenceClient(token=os.getenv("HUGGINGFACE_TOKEN"))
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.extra_parameters = extra_parameters
        self.instruct = ""

    def set_parameters(self, temperature=None, max_tokens=None, top_p=None):
        if temperature is not None:
            self.temperature = temperature
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if top_p is not None:
            self.top_p = top_p
    
    def set_instruct(self, model_instruct):
        self.instruct = model_instruct

    def _reverse_message_roles(self, msgs):
        for msg in msgs:
            if (msg['role'] == "user"):
                msg['role'] = "assistant"
            else:
                msg['role'] = "user"

    def ask_model_reversed(self,all_messages):
        self._reverse_message_roles(all_messages)
        res = ''.join(self.ask_model(all_messages))
        self._reverse_message_roles(all_messages)
        return res

    def ask_model(self, all_messages):
        params = {
            "model": self.model_name,
            "messages": [{"role": "system", "content": self.instruct}] + all_messages,
            "stream": True,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p
        }
        
        if (self.extra_parameters):
            params.update(self.extra_parameters)

        try:
            chat_completion = self.client.chat.completions.create(**params)
            for message in chat_completion:
                yield message.choices[0].delta.content
        except Exception as e:
            print("Error:", e)
            return None

    def __repr__(self):
        return (f"{self.__class__.__name__}(model_name={self.model_name}, temperature={self.temperature}, "
                f"max_tokens={self.max_tokens}, top_p={self.top_p})")
    
class Chatbot(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.instruct = "Your name is Casy. \
                        You are specialized at conducting surveys related to technical debts in IT sector on participants that work on IT sector. \
                        You should start the conversation by introducing yourself. \
                        You should repeat the question if you think you didn't get a good answer, unless the user tells you they don't want to answer. \
                        You should ask the following questions in given order: \n"
        self.instruct += read_file("models/chatbot_questions.txt") 
        self.instruct += "You shouldn't answer if the user asks irrelevant questions. \
                        You should ask for clarification when you think that the answer is not good enough. \
                        You should ask for extra information whenever you think it would be a nice contribution to the survey (unless it is already in predefined questions). \
                        You should always stay in the context and ask user to do the same when necessary. \
                        You should only ask questions and comment on answers as minimal as possible. \
                        You should end the survey when you asked all the predefined questions and you don't have anything else to ask."
                        