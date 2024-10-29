from huggingface_hub import InferenceClient
import os

class Chatbot:
    def __init__(self):
        # Define your model name
        self.model_name = os.getenv('MODEL_NAME')
        self.client = InferenceClient()

    def ask_model(self, prompt):
        try:
            response = self.client.text_generation(model=self.model_name, prompt=prompt)
            return response
        except Exception as e:
            print("Error:", e)
            return None