import pytest
from decimal import Decimal
from datetime import date
from domain.models import LoanParameters, AmortizationType
from domain.services import LoanPricingService

def test_fixed_rate_calculation():
    params = LoanParameters(
        principal=Decimal("100000"),
        term_months=360,
        base_interest_rate=Decimal("0.035"),
        amortization_type=AmortizationType.FIXED
    )
    
    service = LoanPricingService(params)
    schedule = service.calculate_payment_schedule()
    
    assert len(schedule) == 360
    assert pytest.approx(schedule[0]["payment"], abs=0.01) == 449.04
    assert schedule[-1]["balance"] == 0

def test_interest_only_calculation():
    params = LoanParameters(
        principal=Decimal("100000"),
        term_months=60,
        base_interest_rate=Decimal("0.035"),
        amortization_type=AmortizationType.INTEREST_ONLY
    )
    
    service = LoanPricingService(params)
    schedule = service.calculate_payment_schedule()
    
    assert len(schedule) == 61  # 60 interest payments + 1 principal
    assert pytest.approx(schedule[0]["payment"], abs=0.01) == 291.67
    assert schedule[-1]["payment"] == 100000