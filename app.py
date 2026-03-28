import streamlit as st
import pandas as pd
import plotly.express as px

# --- STEP 0: CONFIGURATION ---
st.set_page_config(page_title="Bank Churn Intelligence", layout="wide")

# --- STEP 1: LOAD DATA ---
@st.cache_data
def load_data():
    # Ensure Bank_Churn.csv is in the same folder on GitHub
    df = pd.read_csv("Bank_Churn.csv")
    return df

df = load_data()

# --- STEP 2: HEADER & KEY METRICS ---
st.title("🏦 Bank Churn Intelligence AI")
st.markdown("### Executive Retention Dashboard")

# Calculate Churn Rate
total_customers = len(df)
churned_customers = df[df['Exited'] == 1].shape[0]
churn_rate = (churned_customers / total_customers) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%", delta="-2% Target", delta_color="inverse")

# --- STEP 3: VISUAL ANALYSIS ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("Churn by Geography")
    geo_churn = df.groupby('Geography')['Exited'].mean().reset_index()
    
    # 1. Multiply by 100 to show as percentage
    geo_churn['Exited'] = geo_churn['Exited'] * 100 
    
    fig_geo = px.bar(geo_churn, x='Geography', y='Exited', 
                     title="Churn Probability per Region (%)",
                     text_auto='.2f',  # Shows 2 decimal places on the bar
                     labels={'Exited': 'Churn Rate (%)'},
                     color_discrete_sequence=['#ff4b4b'])
    
    # 2. Force labels to sit ON TOP of the bars for clarity
    fig_geo.update_traces(textposition='outside', cliponaxis=False)
    
    # 3. Improve the hover tooltip detail
    fig_geo.update_layout(hovermode="x unified")
    
    st.plotly_chart(fig_geo, use_container_width=True)

with c2:
    st.subheader("Balance vs. Churn")
    # Analyzing if wealthier customers are leaving
    fig_balance = px.box(df, x='Exited', y='Balance', 
                         title="Account Balance Distribution (Stayed vs Exited)",
                         color='Exited',
                         color_discrete_map={0: "green", 1: "red"})
    st.plotly_chart(fig_balance, use_container_width=True)

import google.generativeai as genai

# --- STEP 4: PREDICTIVE SIDEBAR (THE VIRAL COMPONENT) ---
st.sidebar.header("🔍 Predict Churn Risk")
st.sidebar.markdown("Test a custom profile to see the AI's strategic advice.")

with st.sidebar:
    # Creating inputs that match your Bank_Churn.csv columns
    cs = st.slider("Credit Score", 300, 850, 650)
    geo = st.selectbox("Geography", ["France", "Germany", "Spain"])
    age = st.number_input("Age", 18, 100, 35)
    tenure = st.slider("Tenure (Years)", 0, 10, 5)
    balance = st.number_input("Account Balance ($)", value=50000)
    products = st.selectbox("Number of Products", [1, 2, 3, 4])
    is_active = st.radio("Is Active Member?", ["Yes", "No"])
    
    predict_btn = st.button("Analyze & Generate Strategy")

# --- STEP 5: THE AI "BRAIN" (GEMINI 3 FLASH) ---
if predict_btn:
    # Prepare the data for the AI
    active_val = 1 if is_active == "Yes" else 0
    
    # Simple logic to determine "Risk Level" before sending to AI
    # (In a real app, this is where your ML model would sit)
    risk_score = "High" if (age > 40 and products > 2) or (balance > 100000 and active_val == 0) else "Moderate"
    
    st.divider()
    st.subheader(f"🤖 AI Strategic Analysis: {risk_score} Risk Profile")
    
    # Configure Gemini
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash') # Using the stable flash model
    
    prompt = f"""
    You are a Senior Retention Manager at a global bank. 
    Analyze this customer profile:
    - Credit Score: {cs}
    - Location: {geo}
    - Age: {age}
    - Balance: ${balance}
    - Products: {products}
    - Active: {is_active}
    
    The risk level is estimated as {risk_score}. 
    Provide:
    1. A brief explanation of WHY they might leave.
    2. A 3-step 'Executive Retention Plan'.
    3. A short, professional email draft to send to this customer.
    """
    
    with st.spinner("Gemini is analyzing the risk..."):
        response = model.generate_content(prompt)
        st.write(response.text)

# --- STEP 4: AGENTIC PREDICTION (PLACEHOLDER) ---
st.divider()
st.subheader("🤖 AI Risk Assessment")
st.info("In the next update, we will integrate Gemini 3 to generate personalized retention offers for these customers.")