from pathlib import Path
from openpyxl import load_workbook
from domain.models import LoanParameters
from domain.exceptions import ExcelLoadError

class ExcelLoanLoader:
    def __init__(self, file_path: Path):
        try:
            self.wb = load_workbook(file_path, data_only=True)
        except Exception as e:
            raise ExcelLoadError(f"Failed to load Excel file: {str(e)}")
        
    def load_parameters(self, sheet_name: str = "Loan Inputs") -> LoanParameters:
        try:
            sheet = self.wb[sheet_name]
            
            return LoanParameters(
                principal=sheet["B2"].value,
                term_months=sheet["B3"].value,
                base_interest_rate=sheet["B4"].value,
                amortization_type=sheet["B5"].value.lower(),
                payment_frequency=sheet["B6"].value.lower(),
                start_date=sheet["B7"].value,
                fees={
                    "origination": sheet["B8"].value or 0,
                    "processing": sheet["B9"].value or 0
                }
            )
        except Exception as e:
            raise ExcelLoadError(f"Failed to parse Excel data: {str(e)}")