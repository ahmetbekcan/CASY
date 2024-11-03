from huggingface_hub import InferenceClient
import os

class Chatbot:
    def __init__(self, temperature=0.2, max_tokens=1024, top_p=0.7):
        self.model_name = os.getenv('MODEL_NAME') or "meta-llama/Llama-3.2-3B-Instruct"
        self.client = InferenceClient()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def set_parameters(self, temperature=None, max_tokens=None, top_p=None):
        if temperature is not None:
            self.temperature = temperature
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if top_p is not None:
            self.top_p = top_p

    def ask_model(self, all_messages):
        representation = repr(self)
        print(representation)
        try:
            chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "Your name is Casy. \
                                               You are specialized at conducting surveys related to technical debts in IT sector on participants that work on IT sector. \
                                               You should start the conversation by introducing yourself.\
                                               You shouldn't answer if the user asks irrelevant questions. \
                                               You should ask for elaboration when you think that the answer is not good enough.\
                                               You should always stay in the context and ask user to do the same when necessary."},
            ] + all_messages,
            stream=True,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p
            )
            for message in chat_completion:
                yield message.choices[0].delta.content
        except Exception as e:
            print("Error:", e)
            return None
        
    def __repr__(self):
        return (f"Chatbot(model_name={self.model_name}, temperature={self.temperature}, "
                f"max_tokens={self.max_tokens}, top_p={self.top_p})")