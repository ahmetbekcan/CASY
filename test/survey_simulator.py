from models.agent import Agent
import random

class SurveySimulator:
    def __init__(self, number_of_questions = 5, offtopic_answer_rate = 0.5, uninformative_answer_rate = 0.5, initial_messages = []):
        self.offtopic_rate = offtopic_answer_rate
        self.uninformative_rate = uninformative_answer_rate
        self.messages = initial_messages
        self.no_of_questions = number_of_questions
        self.offtopic_bot = self.get_offtopic_bot()
        self.lazy_bot = self.get_lazy_bot()
        self.simulation_data = []
    
    def get_offtopic_bot(self):
        bot = Agent()
        bot.set_instruct("You should answer the given questions in an irrelevant way.")
        return bot
    
    def get_lazy_bot(self):
        bot = Agent()
        bot.set_instruct("You should answer the given questions in a very short way, so that the user should ask for elaboration.")
        return bot
    
    def get_answer_no(self):
        return sum(1 for item in self.messages if "user" in item)

    def _simulate_surveyor(self, surveyor):
        res = ''.join(surveyor.ask_model(self.messages))
        self.messages.append({"role": "assistant", "content": res})

    def _simulate_participant(self, participant):
        option = random.randint(0,2) #determines the type of prompt
        threshold = random.random()
        res = ""
        if (option == 0):
            res = participant.ask_model_reversed(self.messages)
            self.simulation_data.append({self.get_answer_no():"normal"}) # save data
        elif (option == 1):
            if (self.offtopic_rate <= threshold):
                return
            res = self.offtopic_bot.ask_model_reversed(self.messages)
            self.simulation_data.append({self.get_answer_no():"offtopic"}) # save data
            print(f"offtopic: {self.get_answer_no()} \n")
        elif (option == 2):
            if (self.uninformative_rate <= threshold):
                return
            res = self.lazy_bot.ask_model_reversed(self.messages)
            self.simulation_data.append({self.get_answer_no():"uninformative"}) # save data
            print(f"uninformative: {self.get_answer_no()} \n")
        
        if (res):
            self.messages.append({"role": "user", "content": res})


    def _simulate_q_and_a(self, surveyor, participant):
        if (list(self.messages[-1].keys())[0] == "assistant"):
            self._simulate_participant(participant)
        
        self._simulate_surveyor(surveyor)
        self._simulate_participant(participant)

    def simulate(self, surveyor, participant):
        i = 0
        while (i < self.no_of_questions):
            self._simulate_q_and_a(i==0,surveyor, participant)
            i+=1
    
    def get_simulation_result(self):
        return self.messages