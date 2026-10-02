import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv("data/sample_tomato.csv")

# Features
X = df[['year', 'month', 'day', 'prev_price', 'price_change', 'rolling_avg_7']]
y = df['modal_price']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# =====================
# 1. Actual vs Predicted
# =====================
plt.figure()
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Prices")
plt.show()

# =====================
# 2. Trend over time
# =====================
df_sample = df.head(200)

plt.figure()
plt.plot(df_sample['modal_price'], label="Actual")
plt.title("Price Trend")
plt.legend()
plt.show()