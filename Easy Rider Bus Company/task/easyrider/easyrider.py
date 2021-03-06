# Write your awesome code here
import json
import re

#with open('easyrider.json','r') as f1:
#    data = json.load(f1)

data = json.loads(input())

def checktype(target,type_check):
    if type(target) == type_check:
        return(True)
    else:
        return(False)


#regex templates
name_re = r"([A-Z][a-z]+\s)+(Road|Avenue|Boulevard|Street)$"

time_temp = '[01][0-9]:[0-5][0-9]$|2[0-3]:[0-5][0-9]$'

data_check = {'bus_id': {'datatype': int, 'typeErrors': 0, 'emptyErrors': 0, 'formatErrors': 0},
              'stop_id': {'datatype': int, 'typeErrors': 0, 'emptyErrors': 0, 'formatErrors': 0},
              'stop_name': {'datatype': str, 'typeErrors': 0, 'emptyErrors': 0, 'formatErrors': 0},
              'next_stop': {'datatype': int, 'typeErrors': 0, 'emptyErrors': 0, 'formatErrors': 0},
              'stop_type': {'datatype': str, 'typeErrors': 0, 'emptyErrors': 0, 'formatErrors': 0},
              'a_time': {'datatype': str, 'typeErrors': 0, 'emptyErrors': 0, 'formatErrors': 0}
              }


for item in data:
    for item_obj in item:
        if not checktype(item[item_obj],data_check[item_obj]['datatype']):
            data_check[item_obj]['typeErrors'] += 1
        else:
            if item[item_obj] == "" and item_obj != "stop_type":
                data_check[item_obj]['emptyErrors'] += 1
            elif item_obj == "stop_type":
                if not re.match('[OSF]?$',item[item_obj]):
                    data_check[item_obj]['formatErrors'] += 1
            elif item_obj == 'a_time':
                if not re.match(time_temp,item[item_obj]):
                    data_check[item_obj]['formatErrors'] += 1
            elif item_obj == 'stop_name':
                if not (re.match(name_re,item[item_obj])):
                    data_check[item_obj]['formatErrors'] += 1

total_errors = 0

for item_obj in data_check:
    total_errors += data_check[item_obj]['typeErrors'] + data_check[item_obj]['emptyErrors'] + data_check[item_obj]['formatErrors']

# print("Format validation errors: " + str(total_errors) + " errors")

#for item_obj in data_check:
#    if data_check[item_obj]['typeErrors'] + data_check[item_obj]['emptyErrors']+ + data_check[item_obj]['formatErrors'] > 0:
#        print(item_obj + ": " + str(data_check[item_obj]['typeErrors'] + data_check[item_obj]['emptyErrors']+ + data_check[item_obj]['formatErrors']))

# print("stop_name: " + str(data_check['stop_name']['formatErrors']))
# print("stop_type: " + str(data_check['stop_type']['formatErrors']))
# print("a_time: " + str(data_check['a_time']['formatErrors']))


busses = []
busses_and_stops = {}
for item in data:
    if item['bus_id'] not in busses:
        busses.append(item['bus_id'])
        busses_and_stops[item['bus_id']] = 1
    else:
        busses_and_stops[item['bus_id']] += 1

#for bus in busses_and_stops:
 #   print('bus_id: ' + str(bus) + ', stops: ' + str(busses_and_stops[bus]))

lines = set()
passed = True
for item in data:
    lines.add(item['bus_id'])

start_stops = set()
transfer_stops = set()
finish_stops = set()
all_stops = set()

for line in lines:
    start= False
    finish = False
    for item in data:
        if(item['bus_id']==line):
            if(item['stop_type']=="S"):
                start=True
                start_stops.add(item['stop_name'])
            elif(item['stop_type']=="F"):
                finish=True
                finish_stops.add(item['stop_name'])

            if(item['stop_name'] in all_stops):
                transfer_stops.add(item['stop_name'])
            else:
                all_stops.add(item['stop_name'])

    if not start or not finish:
        print("There is no start or end stop for the line: " + str(line))
        passed=False
        break

#if passed:
#    print("Start stops: " + str(len(start_stops)) + " " + str(sorted(start_stops)))
#    print("Transfer stops: " + str(len(transfer_stops)) + " " + str(sorted(transfer_stops)))
#    print("Finish stops: " + str(len(finish_stops)) + " " + str(sorted(finish_stops)))

wrong_times = {}
for line in lines:
    this_line_stops = []
    this_line_times = {}
    this_line_stop_names = {}
    this_line_nextstops = {}
    for item in data:
        if item['bus_id'] == line:
            this_line_stops.append(item['stop_id'])
            this_line_times[item['stop_id']] = item['a_time']
            this_line_stop_names[item['stop_id']] = item['stop_name']
            this_line_nextstops[item['stop_id']] = item['next_stop']
            if item['stop_type'] == 'S':
                start_stop = item['stop_id']


    this_stop = start_stop
    next_stop = this_line_nextstops[this_stop]
    for i in range(len(this_line_stops)-1):
        if this_line_times[next_stop] < this_line_times[this_stop]:
            wrong_times[line] = this_line_stop_names[next_stop]
            break
        this_stop = next_stop
        next_stop = this_line_nextstops[this_stop]

# print("Arrival time test:")
# if len(wrong_times) == 0:
#     print("OK")
# else:
#     for wrong_time in wrong_times:
#         print("bus_id line " + str(wrong_time) + " wrong time on station " + wrong_times[wrong_time])


wrong_stops = set()

for item in data:
    if(item['stop_type']=="O"):
        if item['stop_name'] in start_stops:
            wrong_stops.add(item['stop_name'])
        elif item['stop_name'] in finish_stops:
            wrong_stops.add(item['stop_name'])
        elif item['stop_name'] in transfer_stops:
            wrong_stops.add(item['stop_name'])

# def wrong_stop_printer(wrong_stops):
#     start_string = "Wrong stop type: ["
#     for i in range(len(wrong_stops)):
#         if i == 1:
#             start_string += wrong_stops[i]
#         else:
#             start_string += ", " + wrong_stops[i]
#         if i == len(wrong_stops):
#             start_string += "]"

print('On demand stops test:')
if len(wrong_stops) == 0:
    print("OK")
else:
    print('Wrong stop type: ' + str(list(wrong_stops)))
