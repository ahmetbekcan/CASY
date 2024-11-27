from huggingface_hub import InferenceClient
import os

class Agent:
    def __init__(self, model_name=None, temperature=0.2, max_tokens=500, top_p=0.7):
        self.model_name = model_name or os.getenv('MODEL_NAME') or "meta-llama/Llama-3.2-3B-Instruct"
        self.client = InferenceClient()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
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
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": self.instruct}] + all_messages,
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
        return (f"{self.__class__.__name__}(model_name={self.model_name}, temperature={self.temperature}, "
                f"max_tokens={self.max_tokens}, top_p={self.top_p})")