import streamlit as st
import pandas as pd
import plotly.express as px

from agent import (
    calculate_pd,
    decision_engine,
    risk_category,
    explain_risk,
    business_recommendation
)

from utils import generate_llm_insight, create_cro_report


# ---------------- CONFIG ----------------
st.set_page_config(page_title="CRO Intelligence Desk", layout="wide")

# ---------------- STATE ----------------
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "results" not in st.session_state:
    st.session_state.results = {}

if "pdf_file" not in st.session_state:
    st.session_state.pdf_file = None


# ---------------- UI ----------------
st.title("🏛️ Agentic Credit Risk Intelligence")

api_key = st.secrets.get("GOOGLE_API_KEY")

tab1, tab2 = st.tabs(["📊 Risk Analysis", "📈 Portfolio"])

# ---------------- TAB 1 ----------------
with tab1:

    st.header("Borrower Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:
        loan_amount = st.number_input("Loan Amount", value=100000)
        income = st.number_input("Income", value=50000)

    with col2:
        credit_score = st.slider("Credit Score", 300, 900, 650)
        market_vol = st.slider("Market Volatility", 0, 100, 40)

  if st.button("🚀 Run Agentic Risk Analysis"):

    payload = {
        "LoanAmount": loan_amount,
        "Income": income,
        "CreditScore": credit_score,
        "MarketVolatility": market_vol
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()

        st.session_state.results = data
        st.session_state.analysis_done = True

    if st.session_state.analysis_done:

        res = st.session_state.results

	st.success(f"PD: {res['pd']:.2f}")
	st.success(f"Decision: {res['decision']}")
	st.success(f"Risk: {res['category']}")

for exp in res["explanations"]:
    st.write(f"- {exp}")

	st.info(res["recommendation"])

        if api_key:
            insight = generate_llm_insight(api_key, res)
            st.markdown(insight)

            pdf_metrics = {"PD": res["pd"], "Decision": res["decision"]}
            st.session_state.pdf_file = create_cro_report(insight, pdf_metrics)

    if st.session_state.pdf_file:
        st.download_button(
            "Download Report",
            st.session_state.pdf_file,
            "report.pdf",
            key="pdf_download"
        )