def calculate_pd(features):
    score = (
        0.3 * (features['LoanAmount'] / 500000) +
        0.2 * (1 - features['CreditScore'] / 900) +
        0.2 * (features['MarketVolatility'] / 100) +
        0.3 * (features['LoanAmount'] / max(features['Income'], 1))
    )
    return min(max(score, 0), 1)


def decision_engine(pd):
    if pd < 0.3:
        return "APPROVE"
    elif pd < 0.7:
        return "REVIEW"
    return "REJECT"


def risk_category(pd):
    if pd < 0.3:
        return "LOW RISK"
    elif pd < 0.7:
        return "MEDIUM RISK"
    return "HIGH RISK"


def explain_risk(features):
    explanations = []

    if features['CreditScore'] < 600:
        explanations.append("Low credit score increasing default risk")

    if features['LoanAmount'] > features['Income'] * 5:
        explanations.append("High loan-to-income ratio")

    if features['MarketVolatility'] > 60:
        explanations.append("Unstable market conditions")

    return explanations if explanations else ["Stable financial profile"]


def business_recommendation(pd, decision):
    if decision == "APPROVE":
        return "Proceed with standard loan approval."
    elif decision == "REVIEW":
        return "Request additional documents or collateral."
    else:
        return "Reject or reduce loan exposure."