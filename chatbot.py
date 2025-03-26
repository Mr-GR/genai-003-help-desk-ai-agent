class Chatbot:
    def _init__(self):
        self.state = "Greeting"
    
    def perceive_input(self, text):
        if "hello" in text.lower():
            self.state = "Greeting"
        elif "bye" in text.lower():
            self.state = "Closing"
        else:
            self.state = "Listening"

    def decide_reponse(self):
        if self.state == "Greeting":
            return "Hello! How can I help you today?"
        elif self.state == "Listening":
            return "I'm Listening. Please go on."
        elif self.state == "Closing":
            return "Goodbye! Have a great day!"
        else:
            return "I'm here if you need assistance."
        
    def perform_action(self, response):
        print("Agent says:", response)

chatbot = Chatbot()
user_input = "hello"
chatbot.perceive_input(user_input)
response = chatbot.decide_reponse()
print("Your query:", user_input)
chatbot.perform_action(response)