import enum
import datetime


class States(enum.StrEnum):
    OPEN = "open"  # We are not allowing traffic.
    CLOSED = "closed"  # Normal operation we are allowing traffic.
    HALF_OPEN = "half_open"  # We are allowing traffic but only test probe.


class CircuitBreaker:
    def __init__(
        self,
        closed_failure_threshold: int,
        cooldown: int,
        half_open_probe_size: int = 3,
        half_open_success_threshold: int = 1,
        half_open_fail_threshold: int = 1,
        suppress_exc: bool = False,
    ):
        """
        Args:
            closed_failure_threshold (int): The number of consecutive failures allowed
                                     After this, the circuit is opened.
            cooldown (int): The time period (in seconds) to wait.
                             Cooldown state is States.OPEN, and waits for reset
            supress_exc (bool): Whether to suppress exceptions.
        """
        self._state = States.CLOSED
        self.closed_failure_threshold = closed_failure_threshold
        self.cooldown = cooldown
        self.half_open_probe_size = half_open_probe_size
        self.half_open_success_threshold = half_open_success_threshold
        self.half_open_fail_threshold = half_open_fail_threshold
        self._half_open_requests_count: int = 0
        self._half_open_success_count: int = 0
        self._half_open_fail_count: int = 0
        self.suppress_exc = suppress_exc
        self._closed_failures_count: int = 0
        self._cooldown_start: datetime.datetime = datetime.datetime(1970, 1, 1)

    def __enter__(self):
        if self._state == States.CLOSED:
            return self
        # if self.state == States.OPEN:
        # From now on State is OPEN or HALF_OPEN
        time_diff = datetime.datetime.now() - self._cooldown_start
        if time_diff.total_seconds() > self.cooldown:
            if self._state == States.OPEN:
                self._half_open_requests_count = 0
                self._state = States.HALF_OPEN
            if self._state == States.HALF_OPEN:
                if self._half_open_requests_count < self.half_open_probe_size:
                    self._half_open_requests_count += 1
                    return self
                raise Exception("Half-open probe limit reached")
        print("Circuit breaker is OPEN")
        raise Exception("Circuit breaker is OPEN")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any((exc_type, exc_val, exc_tb)):
            if self._state == States.CLOSED:
                self.increment_closed_failures()
            if self._state == States.HALF_OPEN:
                self.increment_half_open_failures()
            return self.suppress_exc # If true then suppress. If False raise.
        if self._state == States.HALF_OPEN:
            self.increment_half_open_success()
        return True

    def reset_failures(self):
        self._closed_failures_count = 0
        self._cooldown_start = datetime.datetime(1970, 1, 1)

    def increment_half_open_success(self):
        self._half_open_success_count += 1
        self._half_open_fail_count = 0
        if self._half_open_success_count >= self.half_open_success_threshold:
            self._state = States.CLOSED
            self._half_open_success_count = 0
            self._half_open_fail_count = 0
            self._half_open_requests_count = 0
            self.reset_failures()

    def increment_half_open_failures(self):
        self._half_open_fail_count += 1
        if self._half_open_fail_count >= self.half_open_fail_threshold:
            self._half_open_requests_count = 0
            self._half_open_success_count = 0
            self._state = States.OPEN
            self._cooldown_start = datetime.datetime.now()

    def increment_closed_failures(self):
        self._closed_failures_count += 1
        if self._closed_failures_count >= self.closed_failure_threshold:
            self._closed_failures_count = 0
            self._state = States.OPEN
            self._cooldown_start = datetime.datetime.now()
