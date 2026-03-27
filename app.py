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

# --- STEP 4: AGENTIC PREDICTION (PLACEHOLDER) ---
st.divider()
st.subheader("🤖 AI Risk Assessment")
st.info("In the next update, we will integrate Gemini 3 to generate personalized retention offers for these customers.")