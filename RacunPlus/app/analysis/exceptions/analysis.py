class AnalysisError(Exception):
    pass
class RateLimitExceededError(AnalysisError):
    pass

class InvalidAnalysisTypeError(AnalysisError):
    pass

class NoBillsFoundError(AnalysisError):
    pass

class AIResponseInvalidError(AnalysisError):
    pass
