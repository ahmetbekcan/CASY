from huggingface_hub import InferenceClient
import os

class Chatbot:
    def __init__(self):
        # Define your model name
        self.model_name = os.getenv('MODEL_NAME')
        self.client = InferenceClient()

    def ask_model(self, prompt):
        
        try:
            chat_completion = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful an honest programming assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            )
            #response = self.client.text_generation(model=self.model_name, prompt=final_prompt)
            #return response
            return chat_completion.choices[0].message
        except Exception as e:
            print("Error:", e)
            return None