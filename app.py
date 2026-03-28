import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import plotly.io as pio
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from io import BytesIO
import re

# ---------------- 1. PDF GENERATION FUNCTION (TOP LEVEL) ----------------
def create_pdf(report_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom body style
    body_style = styles["Normal"]
    body_style.leading = 14 

    content = []
    content.append(Paragraph("<b>BFSI Strategic Retention Report</b>", styles["Title"]))
    content.append(Spacer(1, 20))

    # Split text into paragraphs and handle bolding
    paragraphs = report_text.split('\n')
    for p in paragraphs:
        if p.strip():
            # Convert Gemini's **bold** to PDF <b>bold</b>
            clean_p = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', p)
            content.append(Paragraph(clean_p, body_style))
            content.append(Spacer(1, 8))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ---------------- 2. APP CONFIG ----------------
st.set_page_config(page_title="BFSI Churn Intelligence", layout="wide")
pio.templates.default = "plotly_white"

@st.cache_data
def load_data():
    df = pd.read_csv("Bank_Churn.csv")
    df["RevenueRisk"] = df["Balance"] * df["Exited"]
    return df

df = load_data()

# ---------------- 3. DASHBOARD UI ----------------
st.title("🏦 BFSI Customer Churn Intelligence Platform")
st.markdown("### AI-Powered Retention & Revenue Risk System")

# Metrics
t_cust = len(df)
c_rate = (df["Exited"].sum() / t_cust) * 100
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{t_cust:,}")
col2.metric("Churn Rate", f"{c_rate:.2f}%")
col3.metric("Revenue at Risk", f"${df['RevenueRisk'].sum():,.0f}")

st.divider()

# ---------------- 4. ASK AI SECTION ----------------
st.header("🧠 AI Decision Intelligence Layer")
user_query = st.text_input("Ask a business question about the customer data:")

if user_query:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    summary_context = f"Total Customers: {t_cust}, Churn Rate: {c_rate:.2f}%."
    prompt = f"System: Senior Banking Analyst. Context: {summary_context}. Question: {user_query}"

    with st.spinner("Analyzing data..."):
        try:
            response = model.generate_content(prompt)
            final_text = response.text # <--- Define it here
            
            st.markdown("### 🤖 AI Insight")
            st.write(final_text)
            
            # NOW generate the PDF using the text we just got
            pdf_data = create_pdf(final_text)
            
            st.download_button(
                label="📕 Download Formatted PDF",
                data=pdf_data,
                file_name="BFSI_Report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"AI Error: {e}")

# ---------------- 5. SIDEBAR & SOCIALS ----------------
st.sidebar.header("🔍 Individual Analysis")
# (Your sliders for Credit Score, Age, etc. go here)

st.sidebar.divider()
st.sidebar.link_button("🤝 Connect on LinkedIn", "https://www.linkedin.com/in/bhaveshsuryavanshi/")