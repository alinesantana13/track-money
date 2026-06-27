class DomainError(Exception):
    """Base class for domain exceptions."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
    
    def __str__(self):
        return self.message
    
    @staticmethod
    def validate(condition: bool, message: str):
        """Validate a condition and raise DomainError if it fails."""
        if not condition:
            raise DomainError(message)