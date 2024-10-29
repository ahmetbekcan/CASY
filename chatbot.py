from huggingface_hub import InferenceClient
import os

class Chatbot:
    def __init__(self):
        # Define your model name
        self.model_name = os.getenv('MODEL_NAME')
        self.client = InferenceClient()

    def ask_model(self, prompt):
        try:
            initial_prompt = "You are a helpful assistant. Your main and only goal is to answer the questions given by the user or respond to their sentences \
                              without leaving the context. You should not do write any other things than that. If the thing the user given doesn't make sense \
                              just ask the user to elaborate on that. Now, answer or respond to the following." 
            final_prompt = initial_prompt + prompt
            if (final_prompt[-1] != ".")
                final_prompt += "."
            response = self.client.text_generation(model=self.model_name, prompt=final_prompt)
            return response
        except Exception as e:
            print("Error:", e)
            return None