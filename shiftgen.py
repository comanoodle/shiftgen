__author__ = 'orish_000'
"""
* Generate shotef for 4 weeks
* Allow to add arbitrary constraints on each person:
 ** No shotef after weekend shift
 ** No shotef after night shift [v]
 ** No shotef two days in a row [v]
 ** Other unavailabilities (days off, cleaning duty, etc.)
 ** Optional minimum proximity (e.g. one shotef every 3 weeks)
"""
import calendar
from pprint import pprint
from consts import WEEKDAYS
from day_factory import create_day_factory
from constraints.constraints import create_person_constraint
from constraints.severity import *
from collections import namedtuple, OrderedDict




def choose(set):
    import random
    return random.choice(list(set))

DayWithFollowingDays = namedtuple("DayWithFollowingDays", ["day", "possible_following_days"])
def generate_concrete_week(week, people):
    concrete_week = {}

    sunday_factory = create_day_factory(calendar.SUNDAY, people)
    possible_sundays = sunday_factory.get_all_possible_days()
    monday_factories = []
    sundays_and_mondays = []
    for possible_sunday in possible_sundays:
        monday_factory = create_day_factory(calendar.MONDAY, people)
        monday_factory.add_constraint(create_person_constraint(possible_sunday.person, VERY_INCONVENIENT))
        sundays_and_mondays.append(DayWithFollowingDays(day=possible_sunday,
                                                        possible_following_days=
                                                        [DayWithFollowingDays(day=x,
                                                                              possible_following_days=[])
                                                         for x in monday_factory.get_all_possible_days()]))
    from collections import defaultdict
    score_dict = defaultdict(list)
    for sunday, following_days in sundays_and_mondays:
        for day in following_days:
            score = sunday.score + day.day.score
            score_dict[score].append([sunday, day])
    for score, day_pair_list in score_dict.iteritems():
        for day_pair in day_pair_list:
            print "[Score %d] %s (%d) and then %s (%d)" % (score, day_pair[0].person, day_pair[0].score, day_pair[1].day.person, day_pair[1].day.score)



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

def create_day_factories(people):
    # First constraint: Michal and Shaked don't do weekends.
    week = {day_num: create_day_factory(day_num, people)for day_num in WEEKDAYS}
    pprint(week)

    return week

def main():
    people = ["Michal", "Shaked", "OriO", "Omri"]
    theoretical_week = create_day_factories(people)

    perform_count = {person: 0 for person in people}

    concrete_week = generate_concrete_week(theoretical_week, people)
    print
    #for day_num in WEEKDAYS:
    #    print "%s: " % calendar.day_name[day_num],
    #    print concrete_week[day_num]
    pprint(perform_count)


if __name__ == "__main__":
    main()
