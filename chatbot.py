def chatbot_response(user_input):
    
    user_input = user_input.lower()

    if "tomato" in user_input:
        return "Tomato prices depend on trends. Use prediction tool."

    elif "buy" in user_input:
        return "If predicted price is higher, you should BUY."

    elif "sell" in user_input:
        return "If predicted price is lower, you should SELL."

    else:
        return "Ask about tomato price or buy/sell suggestion."