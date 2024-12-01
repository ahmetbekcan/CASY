from models.large_language_models import *
import random
from enum import IntEnum
from utils import read_file

class PromptType(IntEnum):
    NORMAL = 1
    OFFTOPIC = 2
    UNINFORMATIVE = 3

class SurveySimulator:
    def __init__(self, number_of_questions = 5, normal_answer_weight = 0.8, offtopic_answer_weight = 0.1, uninformative_answer_weight = 0.1, initial_messages = [], agent = "alex"):
        self.no_of_questions = number_of_questions
        self.normal_weight = normal_answer_weight
        self.offtopic_weight = offtopic_answer_weight
        self.uninformative_weight = uninformative_answer_weight
        self._normalize_weights()
        self.messages = initial_messages
        self.offtopic_bot = self._get_offtopic_bot()
        self.lazy_bot = self._get_lazy_bot()
        self.simulation_data = []
        self.surveyor = Chatbot()
        self.participant = Agent()
        self.participant.set_instruct("Your goal is to answer survey questions. You should only answer the questions by using your background.\
                                      You shouldn't ask any questions.\n" + read_file(f"tests/test_data/{agent}.txt") )

    def _normalize_weights(self):
        sum = self.normal_weight + self.offtopic_weight + self.uninformative_weight
        self.normal_weight /= sum
        self.offtopic_weight /= sum
        self.uninformative_weight /= sum

    def _get_offtopic_bot(self):
        bot = Agent()
        bot.set_instruct("You are a person who is currently participating in a survey.\
                         You should answer the given questions in an irrelevant manner or ask an irrelevant question to the surveyor.")
        return bot
    
    def _get_lazy_bot(self):
        bot = Agent(max_tokens=5)
        bot.set_instruct("You are a person who is currently participating in a survey.")
        return bot
    
    def _get_answer_no(self):
        return sum(1 for item in self.messages if item.get("role") == "user") + 1

    def _save_data(self,type):
        self.simulation_data.append({self._get_answer_no():type})
        print(f"{type}: {self._get_answer_no()} \n")

    def _simulate_surveyor(self):
        res = ''.join(self.surveyor.ask_model(self.messages))
        self.messages.append({"role": "assistant", "content": res})

    def _simulate_participant(self):
        res = ""
        weights = [self.normal_weight, self.offtopic_weight, self.uninformative_weight]
        selection = random.choices(list(PromptType), weights=weights, k=1)[0]

        if (selection == PromptType.NORMAL):
            res = self.participant.ask_model_reversed(self.messages)
            self._save_data("normal")
        elif (selection == PromptType.OFFTOPIC):
            res = self.offtopic_bot.ask_model_reversed(self.messages)
            self._save_data("offtopic")
        elif (selection == PromptType.UNINFORMATIVE):
            res = self.lazy_bot.ask_model_reversed(self.messages)
            self._save_data("uninformative")
        
        self.messages.append({"role": "user", "content": res})

    def _simulate_q_and_a(self):
        if (self.messages[-1].get("role") == "assistant" if self.messages else False):
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
    
    def get_simulation_result(self):
        return self.messages