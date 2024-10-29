from huggingface_hub import InferenceClient
import os

class Chatbot:
    def __init__(self):
        # Define your model name
        self.model_name = os.getenv('MODEL_NAME')
        self.client = InferenceClient()

    def ask_model(self, prompt):
        try:
            initial_prompt = "You are a helpful assistant. Your main goal is to answer the questions given by the user or respond to their sentences without leaving the context. Now, answer or respond to the following." 
            final_prompt = initial_prompt + prompt
            response = self.client.text_generation(model=self.model_name, prompt=final_prompt)
            return response
        except Exception as e:
            print("Error:", e)
            return None