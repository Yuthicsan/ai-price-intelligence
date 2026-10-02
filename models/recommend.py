def get_recommendation(current_price, predicted_price):
    
    if predicted_price > current_price:
        return {
            "action": "BUY",
            "reason": "Price is expected to increase"
        }
    
    elif predicted_price < current_price:
        return {
            "action": "SELL",
            "reason": "Price is expected to decrease"
        }
    
    else:
        return {
            "action": "HOLD",
            "reason": "Price is stable"
        }