import sqlite3
from datetime import datetime

DB_NAME = "credit_risk.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            loan_amount REAL,
            income REAL,
            credit_score INTEGER,
            market_volatility INTEGER,
            pd REAL,
            decision TEXT,
            category TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_decision(data, result):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO decisions (
            loan_amount, income, credit_score, market_volatility,
            pd, decision, category, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["LoanAmount"],
        data["Income"],
        data["CreditScore"],
        data["MarketVolatility"],
        result["pd"],
        result["decision"],
        result["category"],
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_all_decisions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM decisions ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows