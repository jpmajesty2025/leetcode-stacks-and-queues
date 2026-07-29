'''
Given an array of integers temperatures that represents the daily temperatures, return an array answer such that answer[i] is the number
of days you have to wait after the ith day to get a warmer temperature. If there is no future day that is warmer, have answer[i] = 0 instead.
'''


def daily_temperatures(temperatures: list[int]) -> list[int]:
    pending_indices: list[int] = []
    wait_days = [0] * len(temperatures)

    for day, temperature in enumerate(temperatures):
        while pending_indices and temperatures[pending_indices[-1]] < temperature:
            previous_day = pending_indices.pop()
            wait_days[previous_day] = day - previous_day
        pending_indices.append(day)

    return wait_days
