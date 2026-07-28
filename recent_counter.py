'''
You have a RecentCounter class which counts the number of recent requests within a certain time frame.

Implement the RecentCounter class:

RecentCounter() Initializes the counter with zero recent requests.
int ping(int t) Adds a new request at time t, where t represents some time in milliseconds, and returns the number of requests
that has happened in the past 3000 milliseconds (including the new request). Specifically, return the number of requests that
have happened in the inclusive range [t - 3000, t].
It is guaranteed that every call to ping uses a strictly larger value of t than the previous call.
'''

from collections import deque


class RecentCounter:
    def __init__(self, window_ms: int = 3000) -> None:
        if window_ms <= 0:
            raise ValueError("window_ms must be positive")

        self._window_ms = window_ms
        self._requests: deque[int] = deque()

    def ping(self, t: int) -> int:
        while self._requests and self._requests[0] < t - self._window_ms:
            self._requests.popleft()

        self._requests.append(t)
        return len(self._requests)
