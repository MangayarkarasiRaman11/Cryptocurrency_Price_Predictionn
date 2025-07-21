import streamlit as st
import pandas as pd
import plotly.express as px

# Sample Data
exchange_data = [
    {"Exchange": "Coinbase Exchange", "Trust Score": "10/10", "24h Volume": 1509384894, "Monthly Visits": "46.3M", "Trend": "Up"},
    {"Exchange": "Bitget", "Trust Score": "10/10", "24h Volume": 1472374312, "Monthly Visits": "19.7M", "Trend": "Down"},
    {"Exchange": "OKX", "Trust Score": "10/10", "24h Volume": 1415156435, "Monthly Visits": "23M", "Trend": "Down"},
    {"Exchange": "Bybit", "Trust Score": "10/10", "24h Volume": 1391956038, "Monthly Visits": "19M", "Trend": "Down"},
    {"Exchange": "Crypto.com Exchange", "Trust Score": "10/10", "24h Volume": 661761407, "Monthly Visits": "8.83M", "Trend": "Down"},
    {"Exchange": "Kraken", "Trust Score": "10/10", "24h Volume": 419194747, "Monthly Visits": "7.75M", "Trend": "Down"}
]

df = pd.DataFrame(exchange_data)

# Streamlit UI
st.title("Crypto Exchange Rankings")
st.write("A dashboard displaying the top cryptocurrency exchanges and their 24-hour trading volumes.")

# Display Table
st.dataframe(df.style.format({"24h Volume": "${:,}"}))

# Trend Visualization
fig = px.bar(df, x="Exchange", y="24h Volume", color="Trend",
             title="24h Trading Volume per Exchange",
             color_discrete_map={"Up": "green", "Down": "red"})
st.plotly_chart(fig)
