"""
Add custom errors in here
"""

class FilterError(Exception):
    """
    Exception for filter operations
    """
    pass

class OperatorNotFoundError(Exception):
    """
    Exception for if operator is not found
    """
    pass
