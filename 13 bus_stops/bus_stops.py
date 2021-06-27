import datetime
import json
from math import ceil


FILENAME_ROUTES = "bus_stops_routes_2.json"           # file with routes info
FILENAME_SECTIONS = "bus_stops_sections_2.json"       # file with sections distances info

MINUTES_IN_HOUR = 60                                # 60 minutes in 1 hour
MINUTES_IN_DAY = 24 * 60                            # 1440 minutes in 1 day
DELTA_T = 10                                        # 10 minutes range for departures


# loading data from files
def load_data():
    with open(FILENAME_ROUTES) as fin:
        routes = json.load(fin)

    with open(FILENAME_SECTIONS) as fin:
        sections = json.load(fin)

    return routes, sections


# make "routes_through_stops" dictionary:
def describe_stops(routes):
    routes_through_stops = {}
    # key - name of stop, value - list of route numbers through this stop
    # example: {"A": [104, 437], "D": [104]}
    for route_num, param in routes.items():
        for stop in param["stops"]:
            routes_through_stops[stop] = routes_through_stops.get(stop, []) + [route_num]
    return routes_through_stops


# main algorithm to get the bus/departure for ONE direction of a route
def get_bus_one_way(stop, t_current, dt, t_start, t_end, interval, route_stops):
    bus_one_way = []
    i = 0
    current_stop = route_stops[i]                       # starting from the terminus
    # after the while loop we will have the time of the first departure and the last departure
    # for the particular stop/station stored in t_start and t_end variables
    while current_stop != stop:
        i += 1
        next_stop = route_stops[i]
        t_start += sections[current_stop][next_stop]    # adding the time to get to the next stop
        t_end += sections[current_stop][next_stop]
        current_stop = next_stop

    bus_i_min = ceil((t_current - t_start) / interval)      # this is the ID of the next bus (ID of the first bus = 1)
    bus_i_min = max(bus_i_min, 0)
    t_i_min = t_start + bus_i_min * interval                # the time when the next bus departures
    t_wait = t_i_min - t_current                            # the time one should wait for the next departure

    if t_start <= t_i_min <= t_end and t_i_min <= t_current + dt:   # add the calculated departure info
        if route_stops[-1] != stop:
            bus_one_way.append([route_num, route_stops[0], route_stops[-1], t_wait])

    return bus_one_way


# get the bus/departure for BOTH directions of a route
def get_buses_two_ways(stop, t_current, dt, t_start, t_end, interval, route_stops):
    bus_first_way = get_bus_one_way(stop, t_current, dt, t_start, t_end, interval, route_stops)
    bus_second_way = get_bus_one_way(stop, t_current, dt, t_start, t_end, interval, route_stops[::-1])
    buses_two_ways = bus_first_way + bus_second_way
    return buses_two_ways


if __name__ == "__main__":
    routes, sections = load_data()                          # loading data
    routes_through_stops = describe_stops(routes)           # getting routes lists for all stops/stations

    while True:
        input_string = input("\nEnter station: ").strip()   # get the stop/station name from the user
        if not input_string:                                # exit on empty line (or only spaces)
            break
        if input_string not in sections:                    # wrong stop/station name
            print("No such station!")
            continue

        stop = input_string                                 # user's stop/station name
        datetime_now = datetime.datetime.now()              # current datetime
        curr_h = datetime_now.hour                          # current hour
        curr_m = datetime_now.minute                        # current minutes
        t_curr = curr_h * MINUTES_IN_HOUR + curr_m          # current time, integer
        buses = []                                          # buses/departures for the user's stop/station

        for t_current in [t_curr, t_curr + MINUTES_IN_DAY]:     # this loop is needed because the schedule covers 2 days
            for route_num in routes_through_stops[stop]:    # loop for all the routes through the user's stop/station
                route = routes[route_num]
                route_stops = route["stops"]
                t_start = route["start_time"]
                t_end = route["end_time"]
                interval = route["interval"]
                buses += get_buses_two_ways(stop, t_current, DELTA_T, t_start, t_end, interval, route_stops)

        buses.sort(key=lambda x: x[3])  # sort by waiting time

        # print the results
        print(f"Station name: {stop}\nCurrent time: {str(curr_h).zfill(2)}:{str(curr_m).zfill(2)}\nSchedule:")
        for x in buses:
            print(f"Route {x[0]},\t{x[1]}\t->\t{x[2]},\t\tin {x[3]} min.")

        if not buses:
            print("No buses")

