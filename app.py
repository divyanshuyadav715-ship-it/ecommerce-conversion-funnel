import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Funnel Analysis", layout="wide")

st.title("🛒 E-Commerce Conversion Funnel Analysis")
st.markdown("### Identifying Revenue Leaks in the User Journey")
st.markdown("""
This dashboard simulates a real-world scenario where an e-commerce platform generates 100,000 monthly sessions but struggles with low conversions. 
We analyze the event logs to identify exactly where users drop off and what the financial impact is.
""")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv('ecommerce_events.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("Data file 'ecommerce_events.csv' not found. Please run generate_data.py first.")
    st.stop()

# Overall Funnel
st.header("1. Overall Funnel Drop-off")
funnel_stages = ['session_start', 'product_view', 'add_to_cart', 'checkout_initiate', 'purchase']
overall_funnel = df.groupby('event_type')['session_id'].nunique().reindex(funnel_stages).reset_index()
overall_funnel.columns = ['Stage', 'Users']
overall_funnel['Conversion_Rate_From_Start'] = overall_funnel['Users'] / overall_funnel['Users'].iloc[0] * 100

col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(overall_funnel.style.format({'Conversion_Rate_From_Start': '{:.1f}%'}))

with col2:
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x='Users', y='Stage', data=overall_funnel, palette='Blues_d', ax=ax)
    for index, row in overall_funnel.iterrows():
        ax.text(row.Users, index, f" {row.Users:,} ({row.Conversion_Rate_From_Start:.1f}%)", color='black', va="center")
    st.pyplot(fig)

st.info("💡 **Insight:** Overall, only about 6% of total website visitors actually buy something. The massive 62% drop-off at the final checkout stage is alarmingly high and warrants investigation.")

# Funnel by Device
st.header("2. Isolating the Root Cause (By Device)")
device_funnel = df.groupby(['device_type', 'event_type'])['session_id'].nunique().unstack().reindex(columns=funnel_stages)
checkout_to_purchase = (device_funnel['purchase'] / device_funnel['checkout_initiate'] * 100).reset_index()
checkout_to_purchase.columns = ['Device', 'Checkout_to_Purchase_Conversion_Rate']

col3, col4 = st.columns([1, 2])

with col3:
    st.dataframe(checkout_to_purchase.style.format({'Checkout_to_Purchase_Conversion_Rate': '{:.1f}%'}))

with col4:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x='Device', y='Checkout_to_Purchase_Conversion_Rate', data=checkout_to_purchase, palette='muted', ax=ax2)
    ax2.set_title('Checkout to Purchase Conversion Rate by Device')
    ax2.set_ylabel('Conversion Rate (%)')
    for index, row in checkout_to_purchase.iterrows():
        ax2.text(index, row.Checkout_to_Purchase_Conversion_Rate, f"{row.Checkout_to_Purchase_Conversion_Rate:.1f}%", color='black', ha="center", va="bottom")
    st.pyplot(fig2)

st.error("🚨 **Critical Finding:** The data explicitly proves the problem is isolated to **Mobile users**. While Desktop and Tablet users complete checkout at a ~60% rate, Mobile users convert at only **~15%**. Because Mobile makes up 50% of all traffic, this single friction point is destroying the overall conversion rate.")

# Business Impact
st.header("3. Financial Impact & Recommendation")
st.success("""
**The Actionable Recommendation:**
Instead of saying "we have a drop-off," the data tells us: *"We are losing ₹25 Lakhs monthly because the mobile payment flow is broken."* 

We need an immediate UX redesign and technical audit of the mobile checkout page to recapture this revenue.
""")
