import json

FILENAME_ROUTES = "bus_stops_routes.json"  # file with routes info
FILENAME_SECTIONS = "bus_stops_sections.json"  # file with sections distances info
FILENAME_ROUTES_2 = "bus_stops_routes_2.json"  # file with routes info
FILENAME_SECTIONS_2 = "bus_stops_sections_2.json"  # file with sections distances info


def get_integer_time(h, m, next_day=False):
    if next_day:
        return (h + 24) * 60 + m
    return h * 60 + m


routes = {104: {"stops": ["A", "B", "C", "D"],
                "start_time": get_integer_time(5, 0),
                "end_time": get_integer_time(1, 0, True),
                "interval": 10},
          437: {"stops": ["E", "A", "B", "F"],
                "start_time": get_integer_time(5, 10),
                "end_time": get_integer_time(1, 30, True),
                "interval": 5}
          }

sections = {"A": {"B": 3, "E": 6},
            "B": {"A": 3, "C": 5, "F": 5},
            "C": {"B": 5, "D": 4},
            "D": {"C": 4},
            "E": {"A": 6},
            "F": {"B": 5}
            }

with open(FILENAME_ROUTES, "w") as fout:
    json.dump(routes, fout)

with open(FILENAME_SECTIONS, "w") as fout:
    json.dump(sections, fout)


routes = {1: {"stops": ["A", "B", "C", "D", "E", "F", "T", "A1"],
              "start_time": get_integer_time(5, 0),
              "end_time": get_integer_time(1, 30, True),
              "interval": 15},
          2: {"stops": ["G", "H", "F", "I", "J", "K", "L"],
              "start_time": get_integer_time(4, 0),
              "end_time": get_integer_time(2, 30, True),
              "interval": 30},
          3: {"stops": ["N", "M", "J", "K", "L"],
              "start_time": get_integer_time(7, 0),
              "end_time": get_integer_time(22, 30),
              "interval": 5},
          4: {"stops": ["U", "S", "V", "W", "X", "Y", "Z", "A1", "N"],
              "start_time": get_integer_time(10, 0),
              "end_time": get_integer_time(1, 30, True),
              "interval": 10},
          5: {"stops": ["R", "S", "V", "W", "X"],
              "start_time": get_integer_time(6, 0),
              "end_time": get_integer_time(1, 0, True),
              "interval": 2},
          6: {"stops": ["G", "W", "X", "C1"],
              "start_time": get_integer_time(6, 0),
              "end_time": get_integer_time(1, 0, True),
              "interval": 2},
          7: {"stops": ["A1", "B1", "Q", "P", "O", "C1"],
              "start_time": get_integer_time(5, 0),
              "end_time": get_integer_time(2, 0, True),
              "interval": 60}
          }

sections = {"A": {"B": 2},
            "B": {"A": 2, "C": 3},
            "C": {"B": 3, "D": 5},
            "D": {"C": 5, "E": 6},
            "E": {"D": 6, "F": 6},
            "F": {"E": 6, "H": 5, "I": 3, "T": 7},
            "G": {"W": 9, "H": 5},
            "H": {"G": 5, "F": 5},
            "I": {"F": 3, "J": 6},
            "J": {"I": 6, "K": 4, "M": 8},
            "K": {"J": 4, "L": 4},
            "L": {"K": 4},
            "M": {"J": 8, "N": 8},
            "N": {"M": 8, "A1": 15},
            "O": {"C1": 12, "P": 4},
            "P": {"O": 4, "Q": 4},
            "Q": {"P": 3, "B1": 4},
            "R": {"S": 7},
            "S": {"R": 7, "U": 6, "V": 5},
            "T": {"F": 7, "A1": 6},
            "U": {"S": 6},
            "V": {"S": 5, "W": 3},
            "W": {"V": 5, "X": 4, "G": 9},
            "X": {"W": 4, "Y": 6, "C1": 2},
            "Y": {"X": 6, "Z": 5},
            "Z": {"Y": 5, "A1": 5},
            "A1": {"N": 15, "T": 6, "Z": 5, "B1": 3},
            "B1": {"Q": 4, "A1": 3},
            "C1": {"O": 12, "X": 2}
            }

with open(FILENAME_ROUTES_2, "w") as fout:
    json.dump(routes, fout)

with open(FILENAME_SECTIONS_2, "w") as fout:
    json.dump(sections, fout)

