class GasReservationDurationTooLongException(Exception):
    """Raised when the requested gas reservation duration exceeds the maximum allowed duration."""

    def __init__(
        self,
        message="Max gas reservation duration is 600 seconds.",
    ):
        self.message = message
        super().__init__(self.message)
