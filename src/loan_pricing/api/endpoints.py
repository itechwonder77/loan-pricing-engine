from fastapi import APIRouter, Depends, HTTPException
from domain.models import LoanParameters
from domain.services import LoanPricingService
from .schemas import PricingResultResponse

router = APIRouter(prefix="/pricing", tags=["loan_pricing"])

@router.post("/calculate", response_model=PricingResultResponse)
async def calculate_pricing(loan_params: LoanParameters):
    try:
        service = LoanPricingService(loan_params)
        schedule = service.calculate_payment_schedule()
        
        return {
            "success": True,
            "schedule": schedule,
            "metadata": {
                "total_interest": float(sum(p["interest"] for p in schedule)),
                "total_cost": float(sum(p["payment"] for p in schedule)),
                "apr": None  # TODO: Implement APR calculation
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )