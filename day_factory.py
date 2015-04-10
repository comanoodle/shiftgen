__author__ = 'orish_000'
from constraints.constraints import create_person_constraint
from constraints.severity import *
from consts import WEEKDAYS
import calendar
from collections import namedtuple, defaultdict

Day = namedtuple("Day", ["person", "score"])


def create_day_factory(day, people):
    static_constraints = defaultdict(list)
    static_constraints[calendar.SUNDAY] = \
        [create_person_constraint("Michal", VERY_INCONVENIENT),
         create_person_constraint("Shaked", VERY_INCONVENIENT)]
    static_constraints[calendar.THURSDAY] = \
        [create_person_constraint("Michal", IMPOSSIBLE),
         create_person_constraint("Shaked", IMPOSSIBLE)]

    assert day in WEEKDAYS

    return DayFactory(people, calendar.day_name[day], static_constraints[day])


class DayFactory(object):
    def __init__(self, people, day, constraints=None):
        self.people = people
        self.constraints = constraints
        self.day = day
        if constraints is None:
            self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def iterdays(self):
        for person in self.people:
            constraint_violations = []
            for constraint in self.constraints:
                    if not constraint.condition(person):
                        constraint_violations.append(constraint)
            yield Day(person=person, score=sum([violation.severity for violation in constraint_violations]))

    def get_all_possible_days(self):
        return [day for day in self.iterdays()]

    def __repr__(self):
        return "<%s for %s (id %s)>" % (self.__class__.__name__, self.day, id(self))
