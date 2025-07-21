import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

# ✅ Page Configuration
st.set_page_config(page_title="📉 Crypto Prediction", layout="wide")

# ✅ Function to Fetch Historical Price Data from CoinGecko API
def get_crypto_data(crypto_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": str(days),
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch historical data. Error: {response.status_code}")
        return None

# ✅ User Input for Cryptocurrency Selection
st.markdown("## 🔮 Predict Cryptocurrency Price")
crypto_name = st.text_input("Enter cryptocurrency name (e.g., bitcoin, ethereum):", "bitcoin").strip().lower()

# ✅ Fetch Data & Predict Future Prices
if crypto_name:
    crypto_data = get_crypto_data(crypto_name, days=30)  # Last 30 days data
    if crypto_data:
        timestamps = pd.to_datetime([x[0] for x in crypto_data["prices"]], unit="ms")
        prices = [x[1] for x in crypto_data["prices"]]

        # ✅ Create DataFrame
        df = pd.DataFrame({"Date": timestamps, "Price": prices})
        df.set_index("Date", inplace=True)

        # ✅ Train ARIMA Model (Basic Forecasting)
        model = ARIMA(df["Price"], order=(5,1,0))
        model_fit = model.fit()

        # ✅ Predict Next 7 Days
        forecast_steps = 7
        forecast = model_fit.forecast(steps=forecast_steps)
        future_dates = pd.date_range(df.index[-1], periods=forecast_steps+1, freq="D")[1:]

        # ✅ Create Forecast DataFrame
        forecast_df = pd.DataFrame({"Date": future_dates, "Predicted Price": forecast})
        forecast_df.set_index("Date", inplace=True)

        # ✅ Plot Graph
        fig = px.line(df, x=df.index, y="Price", title=f"📈 {crypto_name.capitalize()} Price Prediction", markers=True, color_discrete_sequence=["red"])
        fig.add_scatter(x=forecast_df.index, y=forecast_df["Predicted Price"], mode="lines+markers", name="Predicted", line=dict(color="blue", dash="dot"))

        # ✅ Display Chart
        st.plotly_chart(fig, use_container_width=True)

        # ✅ Show Predicted Prices
        st.write("### 📅 Predicted Prices for Next 7 Days")
        st.dataframe(forecast_df.style.format({"Predicted Price": "${:.2f}"}))
    else:
        st.error("⚠️ Failed to fetch data. Please enter a valid coin name.")

