from datetime import date
from enum import Enum
from decimal import Decimal
from typing import Optional, Dict
from pydantic import BaseModel, Field, condecimal, conint, confloat

class PaymentFrequency(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"

class AmortizationType(str, Enum):
    FIXED = "fixed"
    VARIABLE = "variable"
    INTEREST_ONLY = "interest_only"

class FeeType(str, Enum):
    ORIGINATION = "origination"
    PROCESSING = "processing"
    UNDERWRITING = "underwriting"
    LATE = "late"

class LoanParameters(BaseModel):
    principal: condecimal(gt=0, decimal_places=2)
    term_months: conint(gt=0)
    base_interest_rate: condecimal(ge=0, le=1, decimal_places=6)
    amortization_type: AmortizationType
    payment_frequency: PaymentFrequency = PaymentFrequency.MONTHLY
    start_date: date = Field(default_factory=date.today)
    fees: Dict[FeeType, condecimal(ge=0, le=1)] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            Decimal: lambda v: str(v),
            date: lambda v: v.isoformat()
        }

class BorrowerProfile(BaseModel):
    credit_score: conint(ge=300, le=850)
    debt_to_income: confloat(ge=0)
    collateral_value: Optional[condecimal(ge=0)] = None

    @validator('debt_to_income')
    def validate_dti(cls, v):
        if v > 1:
            raise ValueError("DTI ratio cannot exceed 1.0 for this product")
        return v