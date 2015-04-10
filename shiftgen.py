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
from pprint import pprint





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
    # First constraint: Michal and Shaked don't do weekends.
    week = {day_num: create_day_factory(day_num, people)for day_num in WEEKDAYS}
    pprint(week)
    week[calendar.SUNDAY].add_constraint("Michal", DayFactory.VERY_INCONVENIENT)
    week[calendar.SUNDAY].add_constraint("Shaked", DayFactory.VERY_INCONVENIENT)
    week[calendar.THURSDAY].add_constraint("Michal", DayFactory.IMPOSSIBLE)
    week[calendar.THURSDAY].add_constraint("Shaked", DayFactory.IMPOSSIBLE)

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
