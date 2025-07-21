import streamlit as st
import requests
import pandas as pd

# ✅ Streamlit Page Configuration
st.set_page_config(page_title="📊 Historical Crypto Data", layout="wide")


# ✅ Function to Fetch Historical Data from CoinGecko API
def get_historical_data(coin_name, days=20):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": str(days),
        "interval": "daily"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"⚠️ Error fetching data: {response.status_code}")
        return None


# ✅ User Input for Cryptocurrency
st.markdown("## 📈 Enter Cryptocurrency for Historical Data")
coin_name = st.text_input("Enter cryptocurrency name (e.g., bitcoin, ethereum, usdc):", "bitcoin").strip().lower()

# ✅ Fetch & Display Data
if coin_name:
    data = get_historical_data(coin_name, days=20)

    if data:
        timestamps = pd.to_datetime([x[0] for x in data["prices"]], unit="ms")
        prices = [x[1] for x in data["prices"]]
        market_caps = [x[1] for x in data["market_caps"]]
        volumes = [x[1] for x in data["total_volumes"]]

        # ✅ Create DataFrame
        df = pd.DataFrame({
            "Date": timestamps,
            "Market Cap": market_caps,
            "Volume": volumes,
            "Price": prices
        })
        df.set_index("Date", inplace=True)

        # ✅ Display Table
        st.dataframe(df.style.format({"Market Cap": "${:,.0f}", "Volume": "${:,.0f}", "Price": "${:.6f}"}))

    else:
        st.error("⚠️ No data found. Please check the cryptocurrency name.")

