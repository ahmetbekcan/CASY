#
class SurveySimulator:
    def __init__(self, number_of_questions = 5, adversarial_prompt_rate = 0.5, short_answer_rate = 0.5):
        self.adversarial_rate = adversarial_prompt_rate
        self.short_answer_rate = short_answer_rate
        self.messages = []
        self.no_of_questions = number_of_questions


    def reverse_message_roles(self):
        for msg in self.messages:
            if (msg['role'] == "user"):
                msg['role'] = "assistant"
            else:
                msg['role'] = "user"

    def simulate_answer(self, first, surveyor, participant):
        if (first):
            self.reverse_message_roles()
            res = ''.join(participant.ask_model(self.messages))
            self.reverse_message_roles()
            self.messages.append({"role": "user", "content": res})
    
        res2 = ''.join(surveyor.ask_model(self.messages))
        self.messages.append({"role": "assistant", "content": res2})
        if res2:
            self.reverse_message_roles()
            res3 = ''.join(participant.ask_model(self.messages))
            self.reverse_message_roles()
            self.messages.append({"role": "user", "content": res3})

    def simulate(self, surveyor, participant):
        i = 0
        while (i < self.no_of_questions):
            self.simulate_answer(i==0, surveyor, participant)
            i+=1