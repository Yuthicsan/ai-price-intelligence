document.getElementById("result").innerHTML =
    "💰 Price: ₹ " + result.predicted_price +
    "<br>📊 Action: " + result.recommendation.action +
    "<br>💡 Reason: " + result.recommendation.reason;