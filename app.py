import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import plotly.io as pio
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from docx import Document

# ---------------- CONFIG & THEME ----------------
st.set_page_config(page_title="BFSI Churn Intelligence", layout="wide")
pio.templates.default = "plotly_white"

# ---------------- HELPER FUNCTIONS (UTILITIES) ----------------
def create_enterprise_docx(report_text, user_query):
    doc = Document()
    doc.add_heading("BFSI Customer Churn Intelligence Report", 0)
    doc.add_heading("User Query", level=1)
    doc.add_paragraph(user_query)
    doc.add_heading("AI Insights", level=1)
    doc.add_paragraph(report_text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def create_pdf(report_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = [Paragraph("BFSI Churn Intelligence Report", styles["Title"]), 
               Paragraph("<br/><br/>", styles["Normal"]),
               Paragraph(report_text, styles["Normal"])]
    doc.build(content)
    buffer.seek(0)
    return buffer

def calculate_risk(balance, age, active, products):
    active_val = 1 if active == "Yes" else 0
    if balance > 100000 and active_val == 0:
        return "High"
    elif age > 45 and products <= 2:
        return "Medium"
    else:
        return "Low"

# ---------------- DATA LOADING ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Bank_Churn.csv")
    # Feature Engineering
    df["RevenueRisk"] = df["Balance"] * df["Exited"]
    return df

df = load_data()

# ---------------- HEADER ----------------
st.title("🏦 BFSI Customer Churn Intelligence Platform")
st.markdown("### AI-Powered Retention & Revenue Risk System")

# ---------------- KPI METRICS ----------------
total_customers = len(df)
churned = df["Exited"].sum()
churn_rate = (churned / total_customers) * 100
total_revenue_risk = df["RevenueRisk"].sum()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Customers", f"{total_customers:,}")
m2.metric("Churn Rate", f"{churn_rate:.2f}%")
m3.metric("Churned Customers", f"{churned:,}")
m4.metric("Revenue at Risk ($)", f"{total_revenue_risk:,.0f}")

st.divider()

# ---------------- GLOBAL VISUALS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Churn Rate by Geography (%)")
    geo = df.groupby("Geography")["Exited"].mean().reset_index()
    geo["Exited"] *= 100
    fig_geo = px.bar(geo, x="Exited", y="Geography", orientation="h",
                     text=geo["Exited"].round(1), color="Exited",
                     color_continuous_scale="RdPu")
    fig_geo.update_traces(textposition="outside")
    st.plotly_chart(fig_geo, use_container_width=True)

with col2:
    st.subheader("Customer Segmentation")
    def segment_customer(row):
        if row["Exited"] == 1 and row["Balance"] > 100000: return "High Value Risk"
        elif row["Exited"] == 1: return "Low Value Risk"
        elif row["IsActiveMember"] == 1: return "Loyal"
        else: return "Inactive/At Risk"
    
    df["Segment"] = df.apply(segment_customer, axis=1)
    seg_counts = df["Segment"].value_counts().reset_index()
    fig_seg = px.pie(seg_counts, names="Segment", values="count", hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_seg, use_container_width=True)

# ---------------- AI DECISION LAYER (ASK AI) ----------------

st.divider()
st.header("❓ Frequently Asked Questions (Ask AI)")

# ---------- BUSINESS INSIGHTS ----------
with st.expander("📊 Business Insights"):
    st.markdown("""
- Which customers are most likely to churn and why?
- What are the main drivers of churn in this dataset?
- Which geography has the highest churn risk and what could be the reason?
- What trends do you observe in customer churn behavior?
""")

# ---------- REVENUE & RISK ----------
with st.expander("💰 Revenue & Risk Analysis"):
    st.markdown("""
- What is the estimated revenue at risk due to churn?
- Which customer segment contributes the most to revenue loss?
- How can the bank reduce financial impact from churn?
- Which high-value customers should be prioritized for retention?
""")

# ---------- RETENTION STRATEGY ----------
with st.expander("🎯 Retention Strategy"):
    st.markdown("""
- What retention strategies should be applied to high-risk customers?
- Suggest personalized offers to retain premium customers
- How can we improve engagement for inactive users?
- What actions should be taken immediately to reduce churn?
""")

# ---------- DATA ANALYSIS ----------
with st.expander("📈 Data Analysis & Patterns"):
    st.markdown("""
- What is the relationship between balance and churn?
- How does customer activity impact churn?
- Which age group has the highest churn rate?
- Does the number of products affect retention?
""")

# ---------- SCENARIO ANALYSIS ----------
with st.expander("🔮 Scenario Analysis"):
    st.markdown("""
- What will happen if customer engagement increases by 20%?
- How would reducing churn by 5% impact revenue?
- What if high-balance customers become inactive?
""")

# ---------- USER GUIDANCE ----------
st.info("💡 Tip: Ask business-focused questions like 'How can we reduce churn?' for better AI insights.")

st.divider()
st.header("🧠 AI Decision Intelligence Layer")
user_query = st.text_input("Ask a business question about the data (e.g., 'How to reduce churn in Germany?'):")

if user_query:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    summary = f"Total Customers: {len(df)}, Churn Rate: {churn_rate:.2f}%"
    prompt = f"System: Senior Banking Analyst. Context: {summary}. Question: {user_query}. Provide business insights."

    with st.spinner("Analyzing..."):
        try:
            response = model.generate_content(prompt)
            st.markdown("### 🤖 AI Insight")
            st.write(response.text)
            
            # Export Section
            c1, c2, c3 = st.columns(3)
            with c1: st.download_button("📄 DOCX", create_enterprise_docx(response.text, user_query), "BFSI_Report.docx")
            with c2: st.download_button("📕 PDF", create_pdf(response.text), "BFSI_Report.pdf")
            with c3: st.download_button("📄 TXT", response.text, "BFSI_Report.txt")
        except Exception as e:
            st.error(f"AI error: {e}")

# ---------------- SIDEBAR: INDIVIDUAL 360 ANALYSIS ----------------
st.sidebar.header("🔍 Customer 360 Analysis")
cs = st.sidebar.slider("Credit Score", 300, 850, 650)
geo_sel = st.sidebar.selectbox("Geography", ["France", "Germany", "Spain"])
age_sel = st.sidebar.number_input("Age", 18, 100, 35)
bal_sel = st.sidebar.number_input("Balance", value=50000)
prod_sel = st.sidebar.selectbox("Products", [1, 2, 3, 4])
act_sel = st.sidebar.radio("Active Member", ["Yes", "No"])

if st.sidebar.button("🚀 Analyze Individual Risk"):
    risk_level = calculate_risk(bal_sel, age_sel, act_sel, prod_sel)
    st.divider()
    st.subheader(f"👤 Individual Intelligence Report ({risk_level} Risk)")
    
    # AI Strategy for Individual
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    ind_model = genai.GenerativeModel("gemini-2.5-flash")
    ind_prompt = f"Profile: Age {age_sel}, Bal {bal_sel}, Geo {geo_sel}, Active {act_sel}. Risk: {risk_level}. Create a 3-step retention plan."
    
    with st.spinner("Generating strategy..."):
        res = ind_model.generate_content(ind_prompt)
        st.write(res.text)

# ---------------- EXPORT SECTION ----------------

st.markdown("### 📥 Export Enterprise Report")

docx_file = create_enterprise_docx(response.text, user_query)
pdf_file = create_pdf(response.text)

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        "📄 Download DOCX",
        docx_file,
        file_name="BFSI_Churn_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

with col2:
    st.download_button(
        "📕 Download PDF",
        pdf_file,
        file_name="BFSI_Churn_Report.pdf",
        mime="application/pdf"
    )

with col3:
    st.download_button(
        "📄 Download TXT",
        response.text,
        file_name="BFSI_Report.txt"
    )
# ---------------- FOOTER & SOCIALS ----------------
st.sidebar.divider()
st.sidebar.link_button("🤝 Connect with Developer", "https://www.linkedin.com/in/bhaveshsuryavanshi/")
st.sidebar.code(f"App Link: bank-churn-intelligence-bhavesh.streamlit.app")