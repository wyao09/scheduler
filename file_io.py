import re

#need to generate this based on commandline input of perference number
#better way to write this?
survey_re = re.compile(r'(.*),(.*),(.*),(.*),(.*),(.*)') 
events_re = re.compile(r'(.*),(.*)')

events_srt_list = [] #list all the events once
events_list = [] #repeats events according to slots available

def setup(survey_file, events_file, people, events, available_events):
    #construct avaialble_events and events
    with open(events_file) as f:
        for line in f:
            event = events_re.match(line).group(1) 
            slots = int(events_re.match(line).group(2))
            
            available_events.add(event)
            events[event] = slots
    f.close()


    #construct people
    with open(survey_file) as f:
        f.readline() #skip first line (for now)
        for line in f:
            m = survey_re.match(line)
            #assume for now that all names are unique
            #maybe write another function to check this?
            p = m.group(2)
            people[p] = {'top':[], 'assigned':set([])}

            #populate top choices
            people[p]['top'].append(m.group(4))
            people[p]['top'].append(m.group(5))
            people[p]['top'].append(m.group(6))
    f.close()
    return True

def write_back(assignment):
    print 'hi'

#write back
#delegate ratio constraint
#event conflict constraints
#code read/refactor code
#comment/finalize
