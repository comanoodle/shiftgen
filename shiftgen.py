__author__ = 'orish_000'
"""
* Generate shotef for 4 weeks
* Allow to add arbitrary constraints on each person:
 ** No shotef after weekend shift
 ** No shotef after night shift [v]
 ** No shotef two days in a row [v]
 ** Other unavailabilities (days off, cleaning duty, etc.)
 ** Optional maximum proximity (e.g. one shotef every 3 weeks)
"""
import calendar
WEEKDAYS = [calendar.SUNDAY, calendar.MONDAY, calendar.TUESDAY, calendar.WEDNESDAY, calendar.THURSDAY]
SLIGHTLY_INCONVENIENT = 1
VERY_INCONVENIENT = 2
IMPOSSIBLE = 3
from pprint import pprint


class Day(object):
    def __init__(self, people):
        self.score = 0
        self.people = people
        self.constraints = {}

    def set_unavailable(self, person, level):
        """
        level: 1 - slightly inconvenient (free time)
               2 - very inconvenient (family event / must move toranut)
               3 - impossible (abroad)
        """
        constraint = lambda p: p != person
        if level not in self.constraints:
            self.constraints[level] = []

        self.constraints[level].append(constraint)

    def generate_possible_outputs(self, ignore_level):
        for person in self.people:
            can_perform = True
            ignored_constraint_levels = range(ignore_level+1, 1, -1)
            for current_level in ignored_constraint_levels:
                for constraint in self.constraints[current_level]:
                    can_perform = can_perform and constraint(person)
            if can_perform:
                yield person

    def get_all_possible_outputs(self, ignore_level):
        return [x for x in self.generate_possible_outputs(ignore_level)]

class ConcreteWeek(object):
    def __init__(self):
        self.days = {}

    def select_day(self, day_num, day):
        assert day_num not in self.days
        self.days[day_num] = day

def choose(set):
    import random
    return random.choice(list(set))

def generate_concrete_week(week, perform_count):
    concrete_week = {}

    for day_num in WEEKDAYS:
        print "%s: " % calendar.day_name[day_num],
        outputs = set(week[day_num].get_all_possible_outputs(2))
        pprint(outputs)
        choice = choose(outputs)
        print "Initial choice is %s, who has %d shifts already" % (choice, perform_count[choice])
        while perform_count[choice] >= 1 and any((count == 0 for count in perform_count.itervalues())):
            outputs = outputs - set([choice])
            choice = choose(outputs)
        print "Selected random output: %s" % choice
        concrete_week[day_num] = choice
        #week[(day_num+1) % 5].set_unavailable(choice, )
        perform_count[choice] += 1

    return concrete_week

def generate_theoretical_week(people):
    text_cal = calendar.TextCalendar()
    text_cal.setfirstweekday(calendar.SUNDAY)
    # First constraint: Michal and Shaked don't do weekends.
    week = {day_num: Day(people) for day_num in text_cal.iterweekdays()}
    pprint(week)
    week[calendar.SUNDAY].set_unavailable("Michal", VERY_INCONVENIENT)
    week[calendar.SUNDAY].set_unavailable("Shaked", VERY_INCONVENIENT)
    week[calendar.THURSDAY].set_unavailable("Michal", IMPOSSIBLE)
    week[calendar.THURSDAY].set_unavailable("Shaked", IMPOSSIBLE)

    return week

def main():
    people = ["Michal", "Shaked", "OriO", "Omri"]
    theoretical_week = generate_theoretical_week(people)

    perform_count = {person: 0 for person in people}

    concrete_week = generate_concrete_week(theoretical_week, perform_count)
    print
    for day_num in WEEKDAYS:
        print "%s: " % calendar.day_name[day_num],
        print concrete_week[day_num]
    pprint(perform_count)


if __name__ == "__main__":
    main()
