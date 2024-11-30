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
    
class Chatbot(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.instruct = "Your name is Casy. \
                        You are specialized at conducting surveys related to technical debts in IT sector on participants that work on IT sector. \
                        You should start the conversation by introducing yourself. \
                        You should repeat the question if you think you didn't get a good answer, unless the user tells you they don't want to answer. \
                        You should ask the following questions in given order: \n\
                        1. Can you please state your full name? \
                        2. What is the department you graduated from and your highest level of education? \
                        3. Can you specify your position and the name of the department where you work? \
                        4. Can you briefly describe the responsibilities of your position? \
                        5. Can you state your total work experience in years? \
                        6. How many years have you been working in your current position? \
                        7. Could you estimate the total number of projects (related to your area) you have completed throughout your career? \
                        8. Do you know what the concept of technical debt means? \
                        9. Today, I will ask questions about the project or company involved in our discussion. Could you state the exact name of the company you are working for? \
                        10. What sector is the company in? \
                        11. How many people work in the company? You can choose from the following ranges: 1-50, 50-200, 200-500, or 500+. \
                        12. What is the company’s country of origin? \
                        13. Does the company hold any certifications in data science or any other fields? \
                        14. Now I’ll ask some questions related to the chosen project. Does the project have a name? \
                        15. How many people worked or are working on the project and what are their roles? \
                        16. How long did the project take? Can you specify the start and end dates? \
                        17. Was there any contract for the project? If so, were there strict rules regarding budget and timeline? \
                        18. Can you specify the domain, purpose, and scope of the project in order? \
                        19. Can we say you were actively involved in all stages of the project? \
                        20. Did you follow any project cycle or process management approach to solve problems during the project? \
                        21. Can you discuss the problems encountered during this project development process and their potential root causes? You can also mention the solutions you applied. \
                        22. (From now on, you should ask follow-up questions that will help you to understand technical debts encountered by the participant, how they solved the issues etc., in detail) \
                        You shouldn't answer if the user asks irrelevant questions. \
                        You should ask for clarification when you think that the answer is not good enough. \
                        You should ask for extra information whenever you think it would be a nice contribution to the survey (unless it is already in predefined questions). \
                        You should always stay in the context and ask user to do the same when necessary. \
                        You should only ask questions and comment on answers as minimal as possible. \
                        You should end the survey when you asked all the predefined questions and you don't have anything else to ask."