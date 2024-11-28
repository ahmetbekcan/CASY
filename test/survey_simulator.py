from models.agent import Agent
import random
from enum import IntEnum

class PromptType(IntEnum):
    OFFTOPIC = 1
    UNINFORMATIVE = 2

class SurveySimulator:
    def __init__(self, number_of_questions = 5, offtopic_answer_rate = 0.1, uninformative_answer_rate = 0.1, initial_messages = []):
        self.offtopic_rate = offtopic_answer_rate*2 #since we have 2 options
        self.uninformative_rate = uninformative_answer_rate*2
        self.messages = initial_messages
        self.no_of_questions = number_of_questions
        self.offtopic_bot = self.get_offtopic_bot()
        self.lazy_bot = self.get_lazy_bot()
        self.simulation_data = []
        self.participant_prompt_type = random.randint(1,2)

    def get_offtopic_bot(self):
        bot = Agent()
        bot.set_instruct("You are a person who is currently participating in a survey.\
                         You should answer the given questions in an irrelevant manner or ask an irrelevant question to the surveyor.")
        return bot
    
    def get_lazy_bot(self):
        bot = Agent()
        bot.set_instruct("You are a person who is currently participating in a survey.\
                         You should answer the given question only with the word 'Sure' or 'OK' or 'I would'.")
        return bot
    
    def get_answer_no(self):
        return sum(1 for item in self.messages if item.get("role") == "user") + 1

    def _simulate_surveyor(self, surveyor):
        res = ''.join(surveyor.ask_model(self.messages))
        self.messages.append({"role": "assistant", "content": res})

    def _simulate_participant(self, participant):
        threshold = random.random()
        res = ""
        
        if (self.participant_prompt_type == PromptType.OFFTOPIC):
            if (self.offtopic_rate > threshold):
                res = self.offtopic_bot.ask_model_reversed(self.messages)
                self.simulation_data.append({self.get_answer_no():"offtopic"}) # save data
                print(f"offtopic: {self.get_answer_no()} \n")
        elif (self.participant_prompt_type == PromptType.UNINFORMATIVE):
            if (self.uninformative_rate > threshold):
                res = self.lazy_bot.ask_model_reversed(self.messages)
                self.simulation_data.append({self.get_answer_no():"uninformative"}) # save data
                print(f"uninformative: {self.get_answer_no()} \n")
        
        if (not res):
            res = participant.ask_model_reversed(self.messages)
            self.simulation_data.append({self.get_answer_no():"normal"}) # save data
            print(f"normal: {self.get_answer_no()} \n")

        self.messages.append({"role": "user", "content": res})
        self.participant_prompt_type = 2 if self.participant_prompt_type == 1 else 1 #switch 1 and 2

    def _simulate_q_and_a(self, surveyor, participant):
        if (self.messages[-1].get("role") == "assistant" if self.messages else False):
            self._simulate_participant(participant)
        
        self._simulate_surveyor(surveyor)
        self._simulate_participant(participant)

    def simulate(self, surveyor, participant):
        i = 0
        while (i < self.no_of_questions):
            self._simulate_q_and_a(surveyor, participant)
            i+=1
    
    def get_simulation_result(self):
        return self.messages