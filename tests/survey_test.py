from models.large_language_models import *
import random
from enum import IntEnum
from helpers.utils import read_file
from dataclasses import dataclass
import wandb

class PromptType(IntEnum):
    NORMAL = 1
    OFFTOPIC = 2
    UNINFORMATIVE = 3

@dataclass
class SurveyData:
    messages: list
    data: list #{prompt_type (key) : prompt_id (value)}

class SurveySimulator:
    def __init__(self, number_of_questions = 5, normal_answer_weight = 0.8, offtopic_answer_weight = 0.1, uninformative_answer_weight = 0.1, initial_messages = [], agent = "alex", log_data = False):
        self.no_of_questions = number_of_questions
        self.normal_weight = normal_answer_weight
        self.offtopic_weight = offtopic_answer_weight
        self.uninformative_weight = uninformative_answer_weight
        self.is_log_data = log_data
        self._normalize_weights()
        self.simulation_data = SurveyData(messages=initial_messages,data=[])
        self.offtopic_bot = self._get_offtopic_bot()
        self.lazy_bot = self._get_lazy_bot()
        self.surveyor = Chatbot(max_tokens=350)
        self.participant = Agent(max_tokens=350)
        self.participant.set_instruct("Your goal is to answer survey questions. You should only answer the questions by using your background.\
                                      You shouldn't ask any questions.\n" + read_file(f"tests/test_data/{str.lower(agent)}.txt") )

    def _normalize_weights(self):
        sum = self.normal_weight + self.offtopic_weight + self.uninformative_weight
        self.normal_weight /= sum
        self.offtopic_weight /= sum
        self.uninformative_weight /= sum

    def _get_offtopic_bot(self):
        bot = Agent(temperature=0.5, max_tokens=256)
        bot.set_instruct("You are a person who is currently participating in a survey.\
                         You should answer the given questions in an irrelevant manner or ask an irrelevant question to the surveyor.")
        return bot
    
    def _get_lazy_bot(self):
        bot = Agent(max_tokens=5)
        bot.set_instruct("You are a person who is currently participating in a survey.")
        return bot
    
    def _get_answer_no(self):
        return sum(1 for item in self.simulation_data.messages if item.get("role") == "user") + 1

    def _save_data(self,type):
        self.simulation_data.data.append({self._get_answer_no():type})
        print(f"{type}: {self._get_answer_no()} \n")

    def _simulate_surveyor(self):
        res = ''.join(self.surveyor.ask_model(self.simulation_data.messages))
        self.simulation_data.messages.append({"role": "assistant", "content": res})

    def _simulate_participant(self):
        res = ""
        weights = [self.normal_weight, self.offtopic_weight, self.uninformative_weight]
        selection = random.choices(list(PromptType), weights=weights, k=1)[0]

        if (selection == PromptType.NORMAL):
            res = self.participant.ask_model_reversed(self.simulation_data.messages)
            self._save_data("normal")
        elif (selection == PromptType.OFFTOPIC):
            res = self.offtopic_bot.ask_model_reversed(self.simulation_data.messages)
            self._save_data("offtopic")
        elif (selection == PromptType.UNINFORMATIVE):
            res = self.lazy_bot.ask_model_reversed(self.simulation_data.messages)
            self._save_data("uninformative")
        
        self.simulation_data.messages.append({"role": "user", "content": res})

    def _simulate_q_and_a(self):
        if (self.simulation_data.messages[-1].get("role") == "assistant" if self.simulation_data.messages else False):
            self._simulate_participant()
        
        self._simulate_surveyor()
        self._simulate_participant()
    
    def set_surveyor(self, _surveyor):
        self.surveyor = _surveyor
    
    def simulate(self):
        i = 0
        while (i < self.no_of_questions):
            self._simulate_q_and_a()
            i+=1
        if (self.is_log_data):
            self.log_data()
    
    def get_simulation_messages(self):
        return self.simulation_data.messages

    def log_data(self):
        wandb.init(project="survey-chatbot", name="experiment-log")
        logged_data = []
        label_dict = {int(k): v for d in self.simulation_data.data for k, v in d.items()}
        print(label_dict)
        for idx, data in enumerate(self.simulation_data.messages):
            question_no = idx + 1
            if data["role"] == "user":
                label = label_dict.get((question_no)/2, "unknown")
                logged_data.append({
                    "answer_no": question_no/2,
                    "role": data["role"],
                    "content": data["content"],
                    "label": label
                })
            else:
                logged_data.append({
                    "question_no": (question_no+1)/2,
                    "role": data["role"],
                    "content": data["content"]
                })

        wandb.log({
            "conversation": logged_data,
            "surveyor_prompt": self.surveyor.instruct,
            "model_parameters": {
                "model_name": self.surveyor.model_name,
                "temperature": self.surveyor.temperature,
                "max_tokens": self.surveyor.max_tokens,
                "top_p": self.surveyor.top_p
            }
        })
        wandb.finish()

class SurveyEvaluator:
    def __init__(self, survey_data=None):
        self.survey_data = survey_data

    def _get_evaluator_agent_params(self):
        params = {
            "temperature": 0.1,
            "max_tokens": 100,
            "top_p": 0.4,
            "frequency_penalty": 0.4,
            "presence_penalty": 0,
        }
        return params