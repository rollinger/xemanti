from django.core.exceptions import SuspiciousOperation


def skip_suspicious_operations(record):
    """
    Skips the email notification if the Error was due to incompatible host
    """
    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
    return True