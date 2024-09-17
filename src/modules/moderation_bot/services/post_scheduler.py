from datetime import datetime, time, timedelta
from dataclasses import dataclass
from enum import Enum


class Weekday(int, Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


@dataclass
class PostRule:
    weekday: Weekday
    times: list[time]


class PostScheduler:

    def __init__(self, rules: list[PostRule]):
        """
        Initialize the scheduler with a list of PostRule objects.
        Each PostRule contains a weekday and a list of times.
        """
        self.rules = self._parse_rules(rules)

    def _parse_rules(self, rules: list[PostRule]) -> dict[int, list[time]]:
        """Convert the list of PostRule objects to a dictionary."""
        parsed_rules = {}
        for rule in rules:
            parsed_rules[rule.weekday.value] = rule.times
        return parsed_rules

    def _get_next_time_for_day(
            self, current_day: int, current_time: time
    ) -> time:
        """Helper method to find the next valid time for a given day."""
        if current_day not in self.rules:
            return None

        times = sorted(self.rules[current_day])
        for post_time in times:
            if post_time > current_time:
                return post_time
        return None

    def get_next_post_time(self, ftom_datetime: datetime = None) -> datetime:
        """
        Get the next post time based on the current or provided datetime.
        """
        if ftom_datetime is None:
            ftom_datetime = datetime.now()

        current_day = ftom_datetime.weekday()
        current_time = ftom_datetime.time()

        # Check for the next available time on the current day
        next_time = self._get_next_time_for_day(current_day, current_time)
        if next_time:
            return datetime.combine(ftom_datetime.date(), next_time)

        # If no time is found for today, move to the next day
        for i in range(1, 8):
            next_day = (current_day + i) % 7
            next_time = self._get_next_time_for_day(next_day, time.min)
            if next_time:
                next_date = ftom_datetime.date() + timedelta(days=i)
                return datetime.combine(next_date, next_time)

        return None


times = [
    time(16, 00),
    time(19, 00),
    time(21, 00),
]
rules = [
    PostRule(Weekday.MONDAY, times),
    PostRule(Weekday.TUESDAY, times),
    PostRule(Weekday.WEDNESDAY, times),
    PostRule(Weekday.THURSDAY, times),
    PostRule(Weekday.FRIDAY, times),
    PostRule(Weekday.SATURDAY, times),
    PostRule(Weekday.SUNDAY, times),
]
post_scheduler = PostScheduler(rules)
