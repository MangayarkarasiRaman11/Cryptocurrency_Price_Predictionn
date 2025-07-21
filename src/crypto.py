import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import base64
import os

# ✅ Step 1: Set Page Configuration
st.set_page_config(page_title="📈 Crypto Price Tracker", layout="wide")


# ✅ Step 2: Function to Fetch Cryptocurrency Data from CoinGecko API
def get_crypto_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    headers = {
        "x-cg-api-key": "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=1&interval=hourly"
        # Replace with your actual API key
    }
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "hourly"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code}, {response.text}")
        return None


# ✅ Step 3: Function to Fetch Real-Time Market Data
def get_market_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto_id,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch real-time market data. Check the coin name.")
        return None


# ✅ Step 4: Function to Apply Background Image
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    else:
        st.error("Error: Background image not found!")
        return None


st.markdown("<h2 style='text-align: center;'>Cryptocurrency Price Prediction</h2>", unsafe_allow_html=True)

# ✅ Step 6: User Input for Cryptocurrency Name
st.markdown("## 🔎 Search for Cryptocurrency Price")
crypto_name = st.text_input("Enter cryptocurrency name (e.g., bitcoin, ethereum, pi-network):",
                            "bitcoin").strip().lower()

# ✅ Step 7: Fetch Data Based on User Input
if crypto_name:
    market_data = get_market_data(crypto_name)
    if market_data and crypto_name in market_data:
        coin_data = market_data[crypto_name]
        price = coin_data["usd"]
        market_cap = coin_data["usd_market_cap"]
        volume = coin_data["usd_24h_vol"]
        change_24h = coin_data["usd_24h_change"]

        # ✅ Step 8: Display Real-Time Market Data
        st.markdown(f"## 📊 **{crypto_name.capitalize()} Live Market Stats**")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="**💰 Current Price (USD)**", value=f"${price:.2f}", delta=f"{change_24h:.2f}%")
        col2.metric(label="**📈 Market Cap (USD)**", value=f"${market_cap:,.0f}")
        col3.metric(label="**📊 24h Trading Volume (USD)**", value=f"${volume:,.0f}")

        # ✅ Step 9: Fetch and Plot Historical Price Data
        crypto_data = get_crypto_data(crypto_name)
        if crypto_data:
            timestamps = pd.to_datetime([x[0] for x in crypto_data["prices"]], unit="ms")
            prices = [x[1] for x in crypto_data["prices"]]

            # ✅ Create DataFrame for Plot
            df = pd.DataFrame({"Timestamp": timestamps, "Price": prices})

            # ✅ Generate Interactive Price Chart
            fig = px.line(df, x="Timestamp", y="Price", title=f"📉 **{crypto_name.capitalize()} Price Movement (24h)**",
                          markers=True)
            fig.update_traces(line_color="red")
            fig.update_layout(xaxis_title="Time", yaxis_title="Price (USD)", template="plotly_dark")

            # ✅ Display Chart
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("⚠️ Invalid cryptocurrency name. Please enter a valid coin name.")