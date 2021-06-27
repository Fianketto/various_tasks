import argparse
import requests
import json


FILE_NAME = 'truth.csv'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_params", nargs=2)
    parser.add_argument("--not_mult", type=int)
    parser.add_argument("--smallest", type=int)
    not_mult, smallest, data = get_data(parser)
    parsed_dict = parse_data(data)
    metrics_list = get_metrics(parsed_dict, not_mult, smallest)
    write_data(metrics_list, FILE_NAME)


def get_data(parser):
    args = parser.parse_args()
    not_mult = args.not_mult or 100
    smallest = args.smallest or 0
    host = args.server_params[0]
    port = args.server_params[1]
    url = f"http://{host}:{port}"
    response = requests.get(url)
    data = json.loads(response.content.decode("utf-8"))
    return not_mult, smallest, data


def parse_data(data):
    joined_data = {}
    for d in data:
        for k, v in d.items():
            cur_list = joined_data.get(k, [])
            cur_list.extend(v)
            joined_data[k] = cur_list
    return joined_data


def get_metrics(parsed_dict, not_mult, smallest):
    rows = []
    for k, v in parsed_dict.items():
        v_modified = [x for x in v if fits(x, not_mult, smallest)] or [0]
        row = [k, max(v_modified), min(v_modified), avg(v_modified), sum(v_modified)]
        rows.append(row)
    return rows


def fits(x, not_mult, smallest):
    return x >= smallest and x % not_mult > 0


def avg(v):
    try:
        average = round(sum(v) / len(v), 2)
        return average
    except ZeroDivisionError:
        return 0


def write_data(metrics_list, file_name):
    sorted_metrics_list = sorted(metrics_list, key=lambda x: x[0])
    with open(file_name, 'w') as f:
        for row in sorted_metrics_list:
            print(";".join(list(map(str, row))), file=f)


if __name__ == '__main__':
    main()
