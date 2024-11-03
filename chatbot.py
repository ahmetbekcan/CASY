from huggingface_hub import InferenceClient
import os

class Chatbot:
    def __init__(self):
        # Define your model name
        self.model_name = os.getenv('MODEL_NAME') or "meta-llama/Llama-3.2-3B-Instruct"
        self.client = InferenceClient()

    def ask_model(self, all_messages):
        
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
            max_tokens=500,
            )
            for message in chat_completion:
                yield message.choices[0].delta.content
        except Exception as e:
            print("Error:", e)
            return None