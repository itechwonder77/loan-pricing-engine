from typing import List, Dict, Optional
from pydantic import BaseModel

class PaymentScheduleItem(BaseModel):
    period: int
    payment: float
    principal: float
    interest: float
    balance: float

class PricingResultResponse(BaseModel):
    success: bool
    schedule: List[PaymentScheduleItem]
    metadata: Dict[str, Optional[float]]