__author__ = 'orish_000'
Day = namedtuple("Day", ["person", "score"])
def create_day_factory(day, people):
    from collections import defaultdict
    static_constraints = defaultdict(list)
    static_constraints[calendar.SUNDAY] = \
        [create_person_constraint("Michal", VERY_INCONVENIENT),
         create_person_constraint("Shaked", VERY_INCONVENIENT)],
    static_constraints[calendar.THURSDAY] = \
        [create_person_constraint("Michal", IMPOSSIBLE),
         create_person_constraint("Shaked", IMPOSSIBLE)]

    assert day in WEEKDAYS

    return DayFactory(people, static_constraints[day])


class DayFactory(object):
    def __init__(self, people, constraints=None):
        self.people = people
        if constraints is None:
            self.constraints = {}

    def add_constraint(self, constraint):
        """
        level: 1 - slightly inconvenient (free time)
               2 - very inconvenient (family event / must move toranut)
               3 - impossible (abroad)
        """
        if constraint.severity not in self.constraints:
            self.constraints[constraint.severity] = []

        self.constraints[constraint.severity].append(constraint)

    def next_day(self):
        for person in self.people:
            constraint_violations = []
            for constraint_list in self.constraints.itervalues():
                for constraint in constraint_list:
                    if not constraint.constraint_func(person):
                        constraint_violations.append(constraint)
            yield Day(person=person, score=sum([violation.level for violation in constraint_violations]))

    def get_all_possible_days(self):
        return [x for x in self.next_day()]