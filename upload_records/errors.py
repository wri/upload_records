class DatasetFailedError(Exception):
    """Exception raised for when dataset update failed."""
    pass


class DatasetPendingError(Exception):
    """Exception raised for when dataset status is still pending."""
    pass
