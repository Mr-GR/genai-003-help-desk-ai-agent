def reactive_chatbot(user_input):
    if "hello" in user_input.lower():
        return "Hello how can I help you?"
    elif "price" in user_input.lower():
        return "Our prices start at $10. Let me know if you need more details!"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day!"
    else:
        return "I'm here to help with any questions you have"


print(reactive_chatbot("Hello"))
print(reactive_chatbot("Can you tell me the price?"))
print(reactive_chatbot("Thanks bye!"))