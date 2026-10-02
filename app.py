import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify, render_template
from models.recommend import get_recommendation
from chatbot import chatbot_response

app = Flask(__name__)

# =========================
# LOAD OR TRAIN MODEL
# =========================
MODEL_PATH = "models/price_model.pkl"

if os.path.exists(MODEL_PATH):
    print("✅ Loading existing model...")
    model = joblib.load(MODEL_PATH)
else:
    print("⚠️ Model not found. Training new model...")

    from models.train_model import train_model
    model = train_model()

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("💾 Model saved!")

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message")

    response = chatbot_response(user_msg)

    return jsonify({"reply": response})

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
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)