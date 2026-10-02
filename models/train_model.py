import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


def train_model():
    # =========================
    # 1. LOAD DATA
    # =========================
    df = pd.read_csv("data/sample_tomato.csv")

    print("Original data shape:", df.shape)

    # =========================
    # 2. FEATURE ENGINEERING
    # =========================
    df = df.sort_values(by=['year', 'month', 'day'])

    # Create features if not already present
    if 'prev_price' not in df.columns:
        df['prev_price'] = df['modal_price'].shift(1)

    if 'price_change' not in df.columns:
        df['price_change'] = df['modal_price'].diff()

    if 'rolling_avg_7' not in df.columns:
        df['rolling_avg_7'] = df['modal_price'].rolling(7).mean()

    df = df.dropna()

    print("After feature engineering:", df.shape)

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
        n_estimators=100,
        random_state=42,
        n_jobs=-1
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
    # 7. SAVE MODEL
    # =========================
    joblib.dump(model, "models/price_model.pkl")
    print("💾 Model saved!")

    return model