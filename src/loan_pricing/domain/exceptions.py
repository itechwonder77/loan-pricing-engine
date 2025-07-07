class InvalidLoanTermsError(Exception):
    """Raised when loan terms are invalid or incompatible"""
    pass

class ExcelLoadError(Exception):
    """Raised when there are issues loading Excel data"""
    pass