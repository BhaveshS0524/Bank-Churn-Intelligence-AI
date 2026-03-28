import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="BFSI Churn Intelligence", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Bank_Churn.csv")
    return df

df = load_data()

# ---------------- FEATURE ENGINEERING ----------------
df["CustomerValue"] = df["Balance"] * df["NumOfProducts"]
df["EngagementScore"] = df["IsActiveMember"] * df["NumOfProducts"]
df["RevenueRisk"] = df["Balance"] * df["Exited"]

# ---------------- HEADER ----------------
st.title("🏦 BFSI Customer Churn Intelligence Platform")
st.markdown("### AI-Powered Retention & Revenue Risk System")

# ---------------- KPI METRICS ----------------
total_customers = len(df)
churned = df["Exited"].sum()
churn_rate = (churned / total_customers) * 100
total_revenue_risk = df["RevenueRisk"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate:.2f}%")
col3.metric("Churned Customers", f"{churned:,}")
col4.metric("Revenue at Risk ($)", f"{total_revenue_risk:,.0f}")

st.divider()

# ---------------- SEGMENTATION ----------------
st.subheader("🎯 Customer Risk Segmentation")

def segment_customer(row):
    if row["Exited"] == 1 and row["Balance"] > 100000:
        return "High Value - High Risk"
    elif row["Exited"] == 1:
        return "Low Value - High Risk"
    elif row["IsActiveMember"] == 1:
        return "Loyal"
    else:
        return "At Risk"

df["Segment"] = df.apply(segment_customer, axis=1)

seg_counts = df["Segment"].value_counts().reset_index()
fig_seg = px.pie(seg_counts, names="Segment", values="count",
                 title="Customer Segmentation")
st.plotly_chart(fig_seg, use_container_width=True)

# ---------------- VISUALS ----------------
col1, col2 = st.columns(2)

with col1:
    geo = df.groupby("Geography")["Exited"].mean().reset_index()
    geo["Exited"] *= 100
    fig_geo = px.bar(geo, x="Geography", y="Exited",
                     title="Churn Rate by Geography (%)",
                     color_discrete_sequence=["red"])
    st.plotly_chart(fig_geo, use_container_width=True)

with col2:
    fig_balance = px.box(df, x="Exited", y="Balance",
                         color="Exited",
                         title="Balance vs Churn")
    st.plotly_chart(fig_balance, use_container_width=True)

# ---------------- TOP RISK CUSTOMERS ----------------
st.subheader("⚠️ High Revenue Risk Customers")

top_risk = df[df["Exited"] == 1].sort_values(by="Balance", ascending=False).head(10)
st.dataframe(top_risk[["CustomerId", "Balance", "Geography", "NumOfProducts"]])

# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("🔍 Customer 360 Analysis")

cs = st.sidebar.slider("Credit Score", 300, 850, 650)
geo = st.sidebar.selectbox("Geography", ["France", "Germany", "Spain"])
age = st.sidebar.number_input("Age", 18, 100, 35)
tenure = st.sidebar.slider("Tenure", 0, 10, 5)
balance = st.sidebar.number_input("Balance", value=50000)
products = st.sidebar.selectbox("Products", [1, 2, 3, 4])
active = st.sidebar.radio("Active Member", ["Yes", "No"])

analyze = st.sidebar.button("🚀 Analyze Customer")

# ---------------- BUSINESS LOGIC ----------------
def calculate_risk(balance, age, active, products):
    active_val = 1 if active == "Yes" else 0
    
    if balance > 100000 and active_val == 0:
        return "High"
    elif age > 45 and products <= 2:
        return "Medium"
    else:
        return "Low"

# ---------------- AI ENGINE ----------------
if analyze:
    risk = calculate_risk(balance, age, active, products)
    revenue_risk = balance if risk == "High" else balance * 0.5
    
    st.divider()
    st.subheader(f"🧠 Customer Intelligence Report ({risk} Risk)")

    col1, col2 = st.columns(2)
    col1.metric("Estimated Revenue Risk", f"${revenue_risk:,.0f}")
    col2.metric("Risk Level", risk)

    # Gemini Config
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a Senior Banking Retention Strategist.

    Customer Profile:
    - Age: {age}
    - Geography: {geo}
    - Balance: {balance}
    - Products: {products}
    - Active: {active}

    Risk Level: {risk}

    Provide:
    1. Key churn drivers
    2. Revenue impact
    3. 3-step retention strategy
    4. Suggested personalized offer
    """

    with st.spinner("Generating AI strategy..."):
        try:
            response = model.generate_content(prompt)
            st.write(response.text)
        except:
            st.error("AI service unavailable")

# ---------------- WHAT-IF SIMULATION ----------------
st.divider()
st.subheader("🔮 Scenario Simulation")

new_balance = st.slider("Adjust Balance", 0, 200000, 50000)

sim_risk = calculate_risk(new_balance, age, active, products)

st.metric("Simulated Risk Level", sim_risk)

# ---------------- FOOTER ----------------
st.sidebar.divider()
st.sidebar.markdown("### 💼 About")
st.sidebar.info("AI-powered BFSI churn intelligence system for decision-makers.")