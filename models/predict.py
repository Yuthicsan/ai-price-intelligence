import joblib

model = joblib.load('models/saved_model.pkl')

def predict_price(date_index):
    return model.predict([[date_index]])[0]