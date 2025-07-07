from typing import Dict, Any
from domain.models import LoanParameters

class LoanRepository:
    def __init__(self):
        self._storage = {}

    def save_calculation(self, loan_params: LoanParameters, result: Dict[str, Any]) -> str:
        calculation_id = str(hash(loan_params.json()))
        self._storage[calculation_id] = {
            "parameters": loan_params.dict(),
            "result": result
        }
        return calculation_id

    def get_calculation(self, calculation_id: str) -> Dict[str, Any]:
        return self._storage.get(calculation_id)