from fastapi import FastAPI
from pydantic import BaseModel

from agent import (
    calculate_pd,
    decision_engine,
    risk_category,
    explain_risk,
    business_recommendation
)

app = FastAPI(title="Agentic Credit Risk API")


class BorrowerInput(BaseModel):
    LoanAmount: float
    Income: float
    CreditScore: int
    MarketVolatility: int


@app.post("/analyze")
def analyze(data: BorrowerInput):

    features = data.dict()

    pd_score = calculate_pd(features)
    decision = decision_engine(pd_score)
    category = risk_category(pd_score)
    explanations = explain_risk(features)
    recommendation = business_recommendation(pd_score, decision)

    return {
        "pd": pd_score,
        "decision": decision,
        "category": category,
        "explanations": explanations,
        "recommendation": recommendation
    }