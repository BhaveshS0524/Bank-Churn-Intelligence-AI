# 🏦 BFSI Customer Churn Intelligence Platform
### **Predictive Analytics & Agentic AI Strategy Orchestrator**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg.svg)](https://bank-churn-intelligence-bhavesh.streamlit.app/)

## 📖 Overview
This platform is a **Decision Intelligence** solution designed for the Banking and Financial Services (BFSI) sector. While traditional dashboards only show historical churn, this engine uses **Agentic AI** to simulate future risk and prescribe immediate retention actions.

By integrating **Gemini 2.5 Flash**, the system analyzes 10,000+ customer records to identify "Revenue at Risk" and generates boardroom-ready executive reports in seconds.



## 🚀 Key Features
* **Agentic Risk Reasoning:** Uses LLM-based reasoning to explain *why* specific segments (e.g., high-balance inactive users in Germany) are exiting.
* **360° Customer Simulator:** A sidebar-driven "What-If" tool for managers to test churn probability based on Credit Score, Age, and Product Engagement.
* **Automated Strategy Orchestration:** Generates personalized 3-step retention plans and professional email drafts for high-value clients.
* **Enterprise Export Ops:** Built-in PDF and DOCX generation to convert AI insights into portable, well-formatted business documents.
* **Interactive Geospatial Analytics:** Visualizes churn density across international markets to identify regional systemic risks.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **AI Engine:** Google Gemini 2.5 Flash (Generative AI SDK)
* **Frontend:** Streamlit (Mobile-Responsive UI)
* **Data Science:** Pandas, NumPy, Plotly Express
* **Document Engineering:** ReportLab (PDF), python-docx (Word), IO (Memory Buffer)

## 🏗️ Architecture
1.  **Data Layer:** Ingests raw bank telemetry data (CSV/SQL).
2.  **Logic Layer:** Performs feature engineering to calculate `RevenueRisk` and `EngagementScore`.
3.  **Intelligence Layer:** Orchestrates prompts to Gemini 2.5 Flash for strategic analysis.
4.  **Presentation Layer:** Renders real-time Plotly visuals and handles asynchronous document generation.

## Install dependencies:
pip install -r requirements.txt

## Set up Secrets:
Create a .streamlit/secrets.toml file and add your API key:

Ini, TOML

GOOGLE_API_KEY = "your_gemini_api_key_here"
Run the App:
streamlit run app.py

## 📈 Business Impact
**Efficiency:** Reduces the time for a Senior Analyst to create a retention report from 4 hours to 4 seconds.

**Proactive Retention:** Identifies high-value "At Risk" customers before they move their capital.

**Scalability:** The architecture is designed to handle enterprise-level datasets with minimal latency thanks to the Flash 2.5 model.

**Developed by Bhavesh Suryavanshi | Connect on [LinkedIn](https://www.linkedin.com/in/bhaveshsuryavanshi/)**

## ⚡ Quick Start
1. **Clone the repository:**

git clone [https://github.com/BhaveshS0524/bank-churn-intelligence-ai.git](https://github.com/BhaveshS0524/bank-churn-intelligence-ai.git)
