from fastapi import Depends
from domain.services import LoanPricingService
from domain.models import LoanParameters

def get_pricing_service(loan_params: LoanParameters) -> LoanPricingService:
    return LoanPricingService(loan_params)