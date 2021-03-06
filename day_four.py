'''
https://adventofcode.com/2018/day/4
'''

import re

date_regexp = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'

time_regexp = r'([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'

id_regexp = r'#\d[0-9]{0,3}'

act_regexp = r'\].(.*)'

four_inp = "inp/day_four_sched.txt"
#four_inp = "day_four_sample.txt"
def get_schedules():

    schedule_items = []

    with open(four_inp, 'r') as f:
        
        for line in [ln.rstrip() for ln in f.readlines()]:

            c_date = re.search(date_regexp, line)[0]
            c_time = re.search(time_regexp, line)[0]
            c_guard_id_ret = re.search(id_regexp, line)
            c_guard_id = c_guard_id_ret[0] if c_guard_id_ret else None
            c_action = re.search(act_regexp, line)[1]

            c_item = {
                'date': c_date,
                'time': c_time,
                'guard_id': c_guard_id,
                'action': c_action
            }

            schedule_items.append(c_item)

    return schedule_items

def retrieve_year(val):
    return int(val['date'].split('-')[0])

def retrieve_mon(val):
    return int(val['date'].split('-')[1])

def retrieve_day(val):
    return int(val['date'].split('-')[2])

def retrieve_hour(val):
    return int(val['time'].split(':')[0])

def retrieve_minute(val):
    return int(val['time'].split(':')[1])

if __name__ == "__main__":

    #programmer's note: anything involving dates kind of sucks!!!
    #there's definitely a python library that sorts by time but I'm a special kind of persistent
    schedule = get_schedules()

    schedule.sort(key=retrieve_mon)
    
    month_list = {key: [] for key in range(1,13)}
    month_key_list = []

    #Round one processing: Split up actions by month, and group them together
    for sched_line in schedule:

        month_list[int(retrieve_mon(sched_line))].append(sched_line)

    time_table = {}
    actions_per_day_map = {}

    for month in month_list:
        if month not in month_key_list and len(month_list[month]) > 0:
            month_key_list.append(month)
            time_table[month] = []
            actions_per_day_map[month] = {}

        #Round Two: Sort the days within each month so that they're ascending order
        month_list[month].sort(key=retrieve_day)

        #Round Three: Group actions performed within individual days, and group them under their respective month
        for action in month_list[month]:

            if retrieve_day(action) not in actions_per_day_map[month]:
                actions_per_day_map[month][retrieve_day(action)] = []
        
            actions_per_day_map[month][retrieve_day(action)].append(action)

        #Round Four: For every day, initialize a 60 element/minute time table array.
        for sched_line in month_list[month]:
            day = retrieve_day(sched_line)

            if day not in time_table[month]:
                time_table[month].append((day, [-1 for x in range(0,60)]))
    
    #Round Five: Sort the times within each day by minute, then by hour
    for month in actions_per_day_map:
        for day in actions_per_day_map[month]:
            actions_per_day_map[month][day].sort(key=retrieve_minute)
            actions_per_day_map[month][day].sort(key=retrieve_hour)

    valid_entries = 0

    final_chronological_list = []

    #Round Six: Create the final chronological itinerary
    for month in actions_per_day_map:
        for day in actions_per_day_map[month]:
            for action in actions_per_day_map[month][day]:
                final_chronological_list.append(action)

    c_guard_id = None
    c_date = ''
    b_isasleep = False
    asleep_start = -1

    '''
    Go through the now chronologically sorted items and determine minutes that guards were asleep
    '''
    for action in final_chronological_list:
        print("{0} {1} {2} {3}".format(action['date'], action['time'], action.get('guard_id', 'NA'), action['action']))

        this_guard_id = action.get('guard_id', None)
        this_date = action.get('date')
        this_month = retrieve_mon(action)
        this_day = retrieve_day(action)

        if this_guard_id is not None:
            c_guard_id = this_guard_id
            b_isasleep = False
            asleep_start = -1

        if 'falls asleep' in action['action']:
            b_isasleep = True
            asleep_start = retrieve_minute(action)
        elif 'wakes up' in action['action'] and b_isasleep:
            #print("WAKE UP WAKE UP WAKE UP", c_guard_id)

            #Round Seven: As sleep/wake intervals are encountered, mark elements within each day by the guard asleep during them
            for index in range(asleep_start, retrieve_minute(action)):
                time_table[this_month][this_day][1][index] = c_guard_id

            b_isasleep = False
            asleep_start = -1

        valid_entries += 1

    #print("Valid entries:", valid_entries)

    id_min_map = {}
    tot_min_asleep = {}
    #Round Eight: Sum up the total minutes each guard was asleep across the itinerary
    for month in time_table:
        for day in time_table[month]:
            for index, entry in enumerate(day[1]):
                if entry is not None and entry != -1:
                    if entry not in id_min_map:
                        id_min_map[entry] = {}
                        tot_min_asleep[entry] = 1
                    else:
                        tot_min_asleep[entry] += 1
                    
                    if index not in id_min_map[entry]:
                        id_min_map[entry][index] = 1
                    else:
                        id_min_map[entry][index] += 1
    
    max_min_per_id = {key: 0 for key in id_min_map}

    #Round Nine: Determine what given minute was each guard most asleep during
    for id in id_min_map:
        #print(id_min_map[id])
        c_max = 0
        for minute in id_min_map[id]:
            if id_min_map[id][minute] > c_max:
                c_max = id_min_map[id][minute]
                max_min_per_id[id] = minute

    sleepiest_guard = ''
    sleepiest_guard_val = 0

    #FINAL ROUND, LET'S ROCK: Determine the sleepiest guard, Then look them up in the max_min_per_id dictionary
    for guard in tot_min_asleep:
        if tot_min_asleep[guard] > sleepiest_guard_val:
            sleepiest_guard_val = tot_min_asleep[guard]
            sleepiest_guard = guard
    
    print("THE SLEEPIEST GUARD:", sleepiest_guard, "THE MINUTE THEY WERE MOST ASLEEP DURING:", max_min_per_id[sleepiest_guard])
    print("FINAL RESULT:", int(sleepiest_guard[1:])*max_min_per_id[sleepiest_guard])

    #Part Two: Determine minute that was most slept during.
    leading_minute = 0
    leading_minute_val = 0
    leading_guard = ''

    for id in id_min_map:
        for minute in id_min_map[id]:
            if id_min_map[id][minute] > leading_minute_val:
                leading_minute = minute
                leading_minute_val = id_min_map[id][minute]
                leading_guard = id
    
    print("Guard", leading_guard, "Most Frequently Slept This Amount of times:", leading_minute_val, "During minute:", leading_minute)
    print("PART TWO FINAL VAL:", int(leading_guard[1:])*leading_minute)
