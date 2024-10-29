from huggingface_hub import InferenceClient
import os

class Chatbot:
    def __init__(self):
        # Define your model name
        self.model_name = os.getenv('MODEL_NAME')
        self.client = InferenceClient()

    def ask_model(self, prompt):
        
        try:
            chat_completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful an honest assistant."},
                {"role": "user", "content": prompt},
            ],
            stream=True,
            max_tokens=500,
            )
            for message in chat_completion:
                yield message.choices[0].delta.content
        except Exception as e:
            print("Error:", e)
            return None