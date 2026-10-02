import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("data/sample_tomato.csv")

print("Original data shape:", df.shape)

# =========================
# 2. FEATURE ENGINEERING
# =========================

# Sort by date (IMPORTANT)
df = df.sort_values(by=['year', 'month', 'day'])

# Add previous day price (trend feature)
df['prev_price'] = df['modal_price'].shift(1)

# Remove NaN rows created due to shift
df = df.dropna()

print("After adding prev_price:", df.shape)

# =========================
# 3. SELECT FEATURES
# =========================
X = df[['year', 'month', 'day', 'prev_price', 'price_change', 'rolling_avg_7']]
y = df['modal_price']
# =========================
# 4. TRAIN-TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 5. TRAIN MODEL
# =========================
model = RandomForestRegressor(
    n_estimators=100,     # more trees = better accuracy
    random_state=42,
    n_jobs=-1             # use all CPU cores
)

model.fit(X_train, y_train)

# =========================
# 6. EVALUATE MODEL
# =========================
y_pred = model.predict(X_test)

error = mean_absolute_error(y_test, y_pred)

print("\n✅ Model trained successfully!")
print("📉 Mean Absolute Error:", error)

# =========================
# 7. TEST PREDICTION
# =========================
# IMPORTANT: you must give last known price
sample = pd.DataFrame({
    'year': [2026],
    'month': [1],
    'day': [10],
    'prev_price': [3000],
    'price_change': [50],
    'rolling_avg_7': [2950]
})
predicted_price = model.predict(sample)

print("\n📊 Predicted Tomato Price:", predicted_price[0])

# =========================
# 8. SAVE MODEL
# =========================
joblib.dump(model, "models/price_model.pkl")

print("\n💾 Model saved as price_model.pkl")