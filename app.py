# app.py - SIMPLE WORKING VERSION
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Bike Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    df['day'] = df['datetime'].dt.day_name()
    return df

df = load_data()

# Sidebar
st.sidebar.title("Filters")
year = st.sidebar.selectbox("Select Year", df['year'].unique())
month = st.sidebar.slider("Select Month", 1, 12, 6)
weather = st.sidebar.selectbox("Weather", ["All", 1, 2, 3, 4])

# Filter data
filtered = df[df['year'] == year]
filtered = filtered[filtered['month'] == month]
if weather != "All":
    filtered = filtered[filtered['weather'] == weather]

# Dashboard
st.title("🚲 Bike Rental Dashboard")
st.write(f"Showing: Year {year}, Month {month}")

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    total = filtered['count'].sum()
    st.metric("Total Rentals", f"{total:,}")
with col2:
    avg = filtered['count'].mean()
    st.metric("Average/Hour", f"{avg:.0f}")
with col3:
    peak = filtered.groupby('hour')['count'].mean().idxmax() if not filtered.empty else 0
    st.metric("Peak Hour", f"{peak}:00")

st.markdown("---")

# Chart 1: Hourly pattern
st.subheader("Hourly Rental Pattern")
fig1, ax1 = plt.subplots(figsize=(10, 4))
if not filtered.empty:
    filtered.groupby('hour')['count'].mean().plot(ax=ax1, color='blue', linewidth=2)
ax1.set_xlabel("Hour of Day")
ax1.set_ylabel("Average Rentals")
ax1.grid(True)
st.pyplot(fig1)

# Chart 2: Weather impact
st.subheader("Weather Impact")
fig2, ax2 = plt.subplots(figsize=(8, 4))
if not filtered.empty:
    filtered.groupby('weather')['count'].mean().plot(kind='bar', ax=ax2, color=['green', 'blue', 'orange', 'red'])
ax2.set_xlabel("Weather (1=Clear, 4=Heavy Rain)")
ax2.set_ylabel("Average Rentals")
st.pyplot(fig2)

# Chart 3: Day of week
st.subheader("Rentals by Day of Week")
fig3, ax3 = plt.subplots(figsize=(8, 4))
if not filtered.empty:
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_data = filtered.groupby('day')['count'].mean().reindex(day_order)
    day_data.plot(kind='bar', ax=ax3, color='purple')
ax3.set_xlabel("Day of Week")
ax3.set_ylabel("Average Rentals")
st.pyplot(fig3)

# Chart 4: Temperature vs Rentals
st.subheader("Temperature Impact")
fig4, ax4 = plt.subplots(figsize=(8, 4))
if not filtered.empty:
    ax4.scatter(filtered['temp'], filtered['count'], alpha=0.5, color='red')
ax4.set_xlabel("Temperature (°C)")
ax4.set_ylabel("Rentals")
st.pyplot(fig4)

# Insights
st.markdown("---")
st.subheader("Key Insights")
st.write("1. **Peak hours**: Usually 8 AM and 5-6 PM (commute times)")
st.write("2. **Weather effect**: Clear days have highest rentals")
st.write("3. **Weekend pattern**: Different from weekdays")
st.write("4. **Temperature**: Warmer days = more rentals")


st.success("✅ Dashboard loaded successfully!")
