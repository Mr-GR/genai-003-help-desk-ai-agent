#Define the rules as conditions and reponses
rules = {
    "hello": "Hello! How can I help you?",
    "prices": "Our prices start at $10. Let me know if you need more details!",
    "bye": "Goodbye! Have a great day!"

}

def rule_based_chatbot(user_input):
    # check each rule to find a matching reponse 

    for keyword, reponse in rules.items():
        if keyword in user_input.lower():
            return reponse
        
    return "I'm here to help with any questions you have."

print(f"Your reponse: Hello there?\nAgent Reponse: {rule_based_chatbot("Hello there!")}")
print(rule_based_chatbot("Can you tell me the price?"))
print(rule_based_chatbot("Thanks bye!"))
print(rule_based_chatbot("What's your policy?"))