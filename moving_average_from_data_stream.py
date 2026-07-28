'''
Given a stream of integers and a window size, calculate the moving average of all integers in the sliding window.

Implement the MovingAverage class:

MovingAverage(int size) Initializes the object with the size of the window size.
double next(int val) Returns the moving average of the last size values of the stream
'''

from collections import deque


class MovingAverage:
    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("size must be positive")

        self._size = size
        self._running_sum = 0
        self._window: deque[int] = deque()

    def next(self, val: int) -> float:
        self._window.append(val)
        self._running_sum += val

        if len(self._window) > self._size:
            self._running_sum -= self._window.popleft()

        return self._running_sum / len(self._window)
