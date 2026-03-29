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
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
from sklearn.preprocessing import StandardScaler

# --- 1. DATA PREPARATION ---
@st.cache_data
def load_data():
    df = pd.read_csv("Bank_Churn.csv")
    # We select the features for the Neural Network
    # CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary
    X = df[['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']]
    y = df['Exited'] # The target (Churn)
    return df, X, y

# Load the data first so 'X' is defined
df, X, y = load_data()

# --- 2. THE DEEP LEARNING ENGINE ---
# Now 'X' exists, so we can scale it
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Build the Sequential ANN
# 
ann_model = Sequential([
    Input(shape=(X_scaled.shape[1],)), # New modern way to define input
    Dense(16, activation='relu'),
    Dropout(0.2), 
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')
])
ann_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# We use a small epoch for the live demo to keep it fast
ann_model.fit(X_scaled, y, epochs=10, batch_size=32, verbose=0)

# ---------------- 1. FUNCTIONS FIRST (Prevents Indentation Errors) ----------------
def create_pdf(report_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    body_style = styles["Normal"]
    body_style.leading = 14 

    content = []
    content.append(Paragraph("<b>BFSI Strategic Retention Report</b>", styles["Title"]))
    content.append(Spacer(1, 20))

    paragraphs = report_text.split('\n')
    for p in paragraphs:
        if p.strip():
            # Convert **bold** to <b>bold</b>
            clean_p = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', p)
            content.append(Paragraph(clean_p, body_style))
            content.append(Spacer(1, 8))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ---------------- 2. SETUP & DATA ----------------
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
    # This finds the folder where your app.py is located
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "Bank_Churn.csv")
    
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}. Please check your GitHub upload.")
        return pd.DataFrame() # Returns empty so the app doesn't crash completely
        
    df = pd.read_csv(file_path)
    df["RevenueRisk"] = df["Balance"] * df["Exited"]
    return df
# ---------------- HEADER ----------------
st.title("🏦 BFSI Customer Churn Intelligence Platform")
st.markdown("### AI-Powered Retention & Revenue Risk System")

# ---------------- KPI CALCULATIONS ----------------
total_customers = len(df)
churned_df = df[df["Exited"] == 1]
churned_count = len(churned_df)
churn_rate = (churned_count / total_customers) * 100

# Revenue Risk is the total balance of customers who have already exited
total_revenue_risk = churned_df["Balance"].sum() 

# ---------------- DISPLAY METRICS ----------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Customers", f"{total_customers:,}")
m2.metric("Churn Rate", f"{churn_rate:.1f}%")
m3.metric("Revenue at Risk", f"${total_revenue_risk:,.0f}")
m4.metric("Avg Score", f"{df['CreditScore'].mean():.0f}")

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

st.subheader("⚠️ Risk Alerts")

high_risk_customers = df[
    (df["Balance"] > 100000) &
    (df["IsActiveMember"] == 0) &
    (df["Exited"] == 1)
]

if len(high_risk_customers) > 0:
    st.error(f"🚨 {len(high_risk_customers)} high-value customers have churned!")
else:
    st.success("✅ No critical churn risk detected")

st.subheader("🔮 Top Customers to Save")

df["ChurnProbability"] = (
    (1 - df["IsActiveMember"]) * 0.4 +
    (df["Balance"] / df["Balance"].max()) * 0.4 +
    (df["NumOfProducts"] <= 2) * 0.2
)

top_save = df.sort_values(
    by="ChurnProbability",
    ascending=False
).head(10)

st.dataframe(
    top_save[[
        "CustomerId",
        "Balance",
        "Geography",
        "NumOfProducts",
        "ChurnProbability"
    ]]
)


# ---------- BUSINESS INSIGHTS ----------
st.header("❓ Frequently Asked Questions (Ask AI)")

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
    
    prompt = f"Context: Churn is {df['Exited'].mean()*100:.2f}%. Question: {user_query}"

    with st.spinner("Analyzing..."):
        try:
            # All code inside 'try' must be indented exactly the same
            response = model.generate_content(prompt)
            report_text = response.text
            
            st.markdown("### 🤖 AI Insight")
            st.write(report_text)
            
            # PDF Generation
            pdf_data = create_pdf(report_text)
            
            st.download_button(
                label="📕 Download Formatted PDF",
                data=pdf_data,
                file_name="BFSI_Report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"AI Error: {e}")            

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

# ---------------- FOOTER & SOCIALS ----------------
st.sidebar.divider()
st.sidebar.link_button("🤝 Connect with Developer", "https://www.linkedin.com/in/bhaveshsuryavanshi/")
st.sidebar.code(f"App Link: bank-churn-intelligence-bhavesh.streamlit.app")