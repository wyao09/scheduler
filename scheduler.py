from sys import argv, exit
from random import choice, randint
from copy import deepcopy
import file_io

"""
people = {'name' : {'top_choices':[listed in order], 'assigned':set([...])}
          'name' : {'top_choices':[listed in order], 'assigned':set([...])}}
events = {'event_name' : 10,
          'event_name' : 10}
available_events = set(...)
"""

#read file name from commandline arg
if len(argv) != 5:
    print "usage: scheduler.py [survey.csv] [events.csv] [# preferences] [# iterations]"
    print "exiting..."
    exit()
survey_file = argv[1]
events_file = argv[2]
preferences = int(argv[3])
iterations = int(argv[4])

people = {}
events = {}
available_events = set([])

#read csv files
if not file_io.setup(survey_file, events_file, 
                     people, events, available_events, preferences):
    raise Exception

#need to check event not already in 'assigned'
def assign(events, available_events, people, p):
    try:
        event = people[p]['top'].pop(0)
        if event not in available_events or event in people[p]['assigned']:
            return False
    except IndexError:
        #check there are still events available
        if len(available_events) == 0:
            return False
        
        #random assignment of available events
        event = choice(list(available_events))
        if event in people[p]['assigned']:
            return False
    people[p]['assigned'].add(event)
    events[event] -= 1
    #if last event spot is being taken
    if events[event] == 0:
        available_events.remove(event)
    return True

#random assignments
def schedule(people, events, available_events):
    while True:
        n = len(people)
        lottery = list(people)
        while n != 0:
            i = randint(0,n-1)
            p = lottery.pop(i)

            #performs assignment
            attempts = 0
            
            success = False
            while not success:
                success = assign(events, available_events, people, p)

                if attempts > 100:
                    return
                attempts += 1
            n -= 1

#assign a score to the current assignment for comparison
def score(assignments, preference):
    s = 0
    keys = assignments.keys()
    for key in keys:
        assigned = list(assignments[key]['assigned'])
        for event in assigned:
            #example scoring for 6 preferences : 13,11,9,7,5,3,1
            try:
                s += 2*preferences+1-(preference[key]['top'].index(event) << 1)
            except ValueError:
                s += 1
    return s

max_score = 0

for i in range (0,iterations):
    p = deepcopy(people)
    e = deepcopy(events)
    a = deepcopy(available_events)
    schedule(p, e, a)
    
    s = score(p,people)
    if s > max_score:
        max_score = s
        final_assignment = p
        leftover_events = e

#need to sort alphebatically
keys = final_assignment.keys();
keys.sort();

#print result
for key in keys:
    print key,
    for event in list(final_assignment[key]['assigned']):
        print ","+event,
    print ''

#print leftover events
for key in leftover_events:
    if leftover_events[key] > 0:
        print key, " : ", leftover_events[key]

print "------------------------"

#print by event
for event in events:
    print event
    for key in keys:
        if event in final_assignment[key]['assigned']:
            print key
    print ''
