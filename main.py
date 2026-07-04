from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
from models import Base, Loan
from schemas import LoanCreate, LoanUpdate
from auth import create_access_token

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Engine API",
    description="Loan EMI & Financial Health Calculator",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- LOGIN MODEL --------------------

class UserLogin(BaseModel):
    username: str
    password: str


# -------------------- HOME API --------------------

@app.get("/")
def home():
    return {
        "message": "Financial Engine API is Running Successfully"
    }


# -------------------- LOGIN API --------------------

@app.post("/login")
def login(user: UserLogin):
    token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
# -------------------- CREATE LOAN --------------------

@app.post("/loan")
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):

    # EMI Calculation
    monthly_rate = (loan.interest_rate / 12) / 100

    emi = (
        loan.loan_amount
        * monthly_rate
        * (1 + monthly_rate) ** loan.tenure_months
    ) / (
        ((1 + monthly_rate) ** loan.tenure_months) - 1
    )

    monthly_surplus = loan.monthly_income - loan.monthly_expenses - emi

    loan_data = Loan(
        borrower_name=loan.borrower_name,
        monthly_income=loan.monthly_income,
        monthly_expenses=loan.monthly_expenses,
        loan_amount=loan.loan_amount,
        interest_rate=loan.interest_rate,
        tenure_months=loan.tenure_months,
    )

    db.add(loan_data)
    db.commit()
    db.refresh(loan_data)

    return {
        "message": "Loan Created Successfully",
        "loan_id": loan_data.id,
        "monthly_emi": round(emi, 2),
        "monthly_surplus": round(monthly_surplus, 2),
    }
# -------------------- GET ALL LOANS --------------------

@app.get("/loans")
def get_all_loans(db: Session = Depends(get_db)):
    loans = db.query(Loan).all()

    return loans
# -------------------- GET LOAN BY ID --------------------

@app.get("/loan/{loan_id}")
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if loan is None:
        return {"message": "Loan Not Found"}

    return loan
# -------------------- UPDATE LOAN --------------------

@app.put("/loan/{loan_id}")
def update_loan(loan_id: int, updated_loan: LoanUpdate, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if loan is None:
        return {"message": "Loan Not Found"}

    loan.borrower_name = updated_loan.borrower_name
    loan.monthly_income = updated_loan.monthly_income
    loan.monthly_expenses = updated_loan.monthly_expenses
    loan.loan_amount = updated_loan.loan_amount
    loan.interest_rate = updated_loan.interest_rate
    loan.tenure_months = updated_loan.tenure_months

    db.commit()
    db.refresh(loan)

    return {
        "message": "Loan Updated Successfully",
        "loan": loan
    }
# -------------------- DELETE LOAN --------------------

@app.delete("/loan/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if loan is None:
        return {"message": "Loan Not Found"}

    db.delete(loan)
    db.commit()

    return {
        "message": "Loan Deleted Successfully"
    }
# -------------------- FINANCIAL HEALTH --------------------

@app.post("/financial-health")
def financial_health(loan: LoanCreate):

    # EMI Calculation
    monthly_rate = (loan.interest_rate / 12) / 100

    emi = (
        loan.loan_amount * monthly_rate * (1 + monthly_rate) ** loan.tenure_months
    ) / (
        ((1 + monthly_rate) ** loan.tenure_months) - 1
    )

    # Financial Metrics
    emi_ratio = (emi / loan.monthly_income) * 100
    debt_to_income = (loan.loan_amount / (loan.monthly_income * 12)) * 100
    monthly_surplus = loan.monthly_income - loan.monthly_expenses - emi

    # Financial Health Status
    if emi_ratio < 30:
        status = "Healthy"
    elif emi_ratio < 50:
        status = "Moderate"
    else:
        status = "Critical"

    return {
        "Monthly EMI": round(emi, 2),
        "EMI Ratio (%)": round(emi_ratio, 2),
        "Debt To Income (%)": round(debt_to_income, 2),
        "Monthly Surplus": round(monthly_surplus, 2),
        "Financial Status": status
    }
@app.get("/dashboard")
def dashboard_data():

    income = 50000
    expenses = 20000
    emi = 9680

    surplus = income - expenses - emi
    ratio = round((emi / income) * 100, 2)

    if ratio < 30:
        status = "Healthy"
    elif ratio < 50:
        status = "Moderate"
    else:
        status = "Critical"

    return {
        "income": income,
        "expenses": expenses,
        "emi": emi,
        "surplus": surplus,
        "ratio": ratio,
        "status": status
    }
