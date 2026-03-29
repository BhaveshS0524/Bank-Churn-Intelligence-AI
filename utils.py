from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
import re
import google.generativeai as genai


def generate_llm_insight(api_key, res):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a Chief Risk Officer.

    Borrower Profile:
    Loan: {res['features']['LoanAmount']}
    Income: {res['features']['Income']}
    Credit Score: {res['features']['CreditScore']}
    Market Volatility: {res['features']['MarketVolatility']}

    PD: {res['pd']}
    Risk Category: {res['category']}
    Decision: {res['decision']}

    Provide reasoning and mitigation strategy.
    """

    response = model.generate_content(prompt)
    return response.text


def create_cro_report(report_text, metrics_dict):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("<b>CONFIDENTIAL: Strategic Risk Report</b>", styles["Title"]))
    content.append(Spacer(1, 12))

    data = [["Metric", "Value"]] + [[k, v] for k, v in metrics_dict.items()]

    table = Table(data)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    for line in report_text.split("\n"):
        if line.strip():
            clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            content.append(Paragraph(clean, styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer