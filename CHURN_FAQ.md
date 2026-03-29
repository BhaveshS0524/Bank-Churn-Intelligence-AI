# Bank Churn Intelligence AI - Technical FAQ Generator
# Designed By: Bhavesh Suryavanshi (AI Solutions Consultant)

# 📑 Bank Churn Technical FAQ & Strategy Governance

This document outlines the predictive logic and operational framework of the **Bank Churn Intelligence AI** system.

---

### 🔍 Q1: How does the "Agentic" layer differ from a standard Churn Dashboard?
**A:** Most dashboards are **descriptive** (showing who left). This system is **prescriptive**. Using Gemini 1.5 Flash, the AI doesn't just show a high churn score; it synthesizes the customer's specific transaction history to explain *why* they are leaving (e.g., "Decreased utility due to high international transaction fees") and drafts a specific retention offer.

### 📈 Q2: What is "Balance Velocity" and why is it a primary metric?
**A:** Balance Velocity measures the rate of capital depletion over a rolling 30, 60, and 90-day window. 
* **Logic:** A customer rarely closes an account with a full balance. They usually "bleed" funds into a competitor bank first. By detecting a negative velocity early, we can intervene while the customer still has significant "Assets Under Management" (AUM) with us.

### 🍷 Q3: How do we handle "False Positives" (Customers flagged as churners who aren't leaving)?
**A:** We use a **Multi-Factor Validation** approach. A high churn score is only triggered if at least two of the following conditions are met:
1. Significant drop in Balance Velocity.
2. Complete cessation of "Sticky" transactions (e.g., automated bill payments).
3. Increased "Outward Remittance" to known competitor financial institutions.

### 🛡️ Q4: Can the AI handle unstructured data like Customer Support logs?
**A:** Yes. Because we utilize the **Gemini 1.5 Flash** model, the system can ingest "Sentiment Data" from recent support tickets or chat transcripts. If a customer recently complained about a technical error and *then* reduced their balance, the Churn Score is automatically escalated to "Critical."

### 🌪️ Q5: What is the "Product Depth" theory in your retention logic?
**A:** Statistical analysis shows that "Product Depth" is the strongest deterrent to churn. A customer with a Savings Account + Credit Card + Personal Loan has a 90% lower churn probability than a Savings-only customer. Our AI specifically recommends "Cross-Sell" opportunities as a primary retention tactic.

---
**Designed By:** Bhavesh Suryavanshi | *AI Solutions Consultant*
EOF

echo "✅ CHURN_FAQ.md has been generated for your Bank Churn project!"
