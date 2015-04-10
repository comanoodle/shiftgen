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
from pprint import pprint
from collections import namedtuple
Day = namedtuple("Day", ["person", "score"])
ConstraintViolation = namedtuple("ConstraintViolation", ["constraint", "level"])

class DayGenerator(object):
    SLIGHTLY_INCONVENIENT = 1
    VERY_INCONVENIENT = 2
    IMPOSSIBLE = 3

    def __init__(self, people):
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

    def next_day(self):
        for person in self.people:
            constraint_violations = []
            for level, constraint_list in self.constraints.iteritems():
                for constraint in constraint_list:
                    if not constraint(person):
                        constraint_violations.append(ConstraintViolation(constraint=constraint, level=level))
            yield Day(person=person, score=sum([violation.level for violation in constraint_violations]))

    def get_all_possible_days(self):
        return [x for x in self.next_day()]

def choose(set):
    import random
    return random.choice(list(set))

def generate_concrete_week(week, perform_count):
    concrete_week = {}

    for day_num in WEEKDAYS:
        print "%s: " % calendar.day_name[day_num],
        outputs = set(week[day_num].get_all_possible_days())
        pprint(outputs)
        #choice = choose(outputs)
        #print "Initial choice is %s, who has %d shifts already" % (choice, perform_count[choice])
        #while perform_count[choice] >= 1 and any((count == 0 for count in perform_count.itervalues())):
        #    outputs = outputs - set([choice])
        #    choice = choose(outputs)
        #print "Selected random output: %s" % choice
        #concrete_week[day_num] = choice
        ##week[(day_num+1) % 5].set_unavailable(choice, )
        #perform_count[choice] += 1

    return concrete_week

def generate_theoretical_week(people):
    text_cal = calendar.TextCalendar()
    text_cal.setfirstweekday(calendar.SUNDAY)
    # First constraint: Michal and Shaked don't do weekends.
    week = {day_num: DayGenerator(people) for day_num in text_cal.iterweekdays()}
    pprint(week)
    week[calendar.SUNDAY].set_unavailable("Michal", DayGenerator.VERY_INCONVENIENT)
    week[calendar.SUNDAY].set_unavailable("Shaked", DayGenerator.VERY_INCONVENIENT)
    week[calendar.THURSDAY].set_unavailable("Michal", DayGenerator.IMPOSSIBLE)
    week[calendar.THURSDAY].set_unavailable("Shaked", DayGenerator.IMPOSSIBLE)

    return week

def main():
    people = ["Michal", "Shaked", "OriO", "Omri"]
    theoretical_week = generate_theoretical_week(people)

    perform_count = {person: 0 for person in people}

    concrete_week = generate_concrete_week(theoretical_week, perform_count)
    print
    #for day_num in WEEKDAYS:
    #    print "%s: " % calendar.day_name[day_num],
    #    print concrete_week[day_num]
    pprint(perform_count)


if __name__ == "__main__":
    main()
