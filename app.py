from flask import Flask, request, jsonify
from flask import render_template
from models.recommend import get_recommendation
import joblib
import pandas as pd

app = Flask(__name__)

# =========================
# LOAD TRAINED MODEL
# =========================
model = joblib.load("models/price_model.pkl")

# =========================
# HOME ROUTE
# =========================
# @app.route("/")
# def home():
#     return "✅ AI Price Prediction API is Running!"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message")

    response = chatbot_response(user_msg)

    return jsonify({"reply": response})

# =========================
# PREDICT ROUTE
# =========================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return "Use POST request with JSON data"

    data = request.json

    input_data = pd.DataFrame({
        'year': [data["year"]],
        'month': [data["month"]],
        'day': [data["day"]],
        'prev_price': [data["prev_price"]],
        'price_change': [data["price_change"]],
        'rolling_avg_7': [data["rolling_avg_7"]]
    })
    prediction = model.predict(input_data)[0]

    recommendation = get_recommendation(
        current_price=data["prev_price"],
        predicted_price=prediction
    )

    return jsonify({
        "predicted_price": round(float(prediction), 2),
        "recommendation": recommendation
    })

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)


