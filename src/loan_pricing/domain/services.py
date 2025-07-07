from decimal import Decimal, getcontext
from typing import List, Dict
from .models import LoanParameters, AmortizationType, PaymentFrequency
from .exceptions import InvalidLoanTermsError

getcontext().prec = 10  # Set decimal precision

class LoanPricingService:
    def __init__(self, loan_params: LoanParameters):
        self.params = loan_params
        self._validate_terms()

    def _validate_terms(self):
        if (self.params.amortization_type == AmortizationType.INTEREST_ONLY and 
            self.params.term_months > 60):
            raise InvalidLoanTermsError("Interest-only loans max term is 60 months")

    def calculate_payment_schedule(self) -> List[Dict]:
        if self.params.amortization_type == AmortizationType.FIXED:
            return self._calculate_fixed_rate_schedule()
        elif self.params.amortization_type == AmortizationType.INTEREST_ONLY:
            return self._calculate_interest_only_schedule()
        else:
            raise NotImplementedError("Variable rate loans not yet implemented")

    def _calculate_fixed_rate_schedule(self) -> List[Dict]:
        schedule = []
        balance = Decimal(str(self.params.principal))
        monthly_rate = Decimal(str(self.params.base_interest_rate)) / Decimal(12)
        payment = self._calculate_monthly_payment(balance, monthly_rate)
        
        for period in range(1, self.params.term_months + 1):
            interest = balance * monthly_rate
            principal = payment - interest
            balance -= principal
            
            schedule.append({
                "period": period,
                "payment": round(payment, 2),
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "balance": round(balance, 2)
            })
        
        return schedule

    def _calculate_interest_only_schedule(self) -> List[Dict]:
        schedule = []
        balance = Decimal(str(self.params.principal))
        monthly_rate = Decimal(str(self.params.base_interest_rate)) / Decimal(12)
        interest_payment = balance * monthly_rate
        
        for period in range(1, self.params.term_months + 1):
            schedule.append({
                "period": period,
                "payment": round(interest_payment, 2),
                "principal": Decimal(0),
                "interest": round(interest_payment, 2),
                "balance": round(balance, 2)
            })
        
        # Add final balloon payment
        if self.params.term_months > 0:
            schedule.append({
                "period": self.params.term_months + 1,
                "payment": round(balance, 2),
                "principal": round(balance, 2),
                "interest": Decimal(0),
                "balance": Decimal(0)
            })
        
        return schedule

    def _calculate_monthly_payment(self, principal: Decimal, monthly_rate: Decimal) -> Decimal:
        if monthly_rate == 0:
            return principal / Decimal(self.params.term_months)
            
        factor = (1 + monthly_rate) ** self.params.term_months
        return principal * monthly_rate * factor / (factor - 1)