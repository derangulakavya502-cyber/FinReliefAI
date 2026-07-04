from pydantic import BaseModel


class LoanCreate(BaseModel):
    borrower_name: str
    monthly_income: float
    monthly_expenses: float
    loan_amount: float
    interest_rate: float
    tenure_months: int


class LoanUpdate(BaseModel):
    borrower_name: str
    monthly_income: float
    monthly_expenses: float
    loan_amount: float
    interest_rate: float
    tenure_months: int


class LoanResponse(BaseModel):
    id: int
    borrower_name: str
    monthly_income: float
    monthly_expenses: float
    loan_amount: float
    interest_rate: float
    tenure_months: int

    class Config:
        from_attributes = True
