import argparse
import csv
import json
from collections import defaultdict


def read_data(filename):
    # [time, user_id, avatar_url, sender, message, likes]
    with open(filename) as f:
        data = [row for row in csv.reader(f)]

    data.reverse()
    return data

def dedup_list(items):
    seen = set()
    seen_add = seen.add
    return [x for x in items if not (x in seen or seen_add(x))]


def trace_names(messages):
    data = defaultdict(list)

    # Record list of all names
    for msg in messages:
        user_id = msg[1]
        name = msg[3]
        data[user_id].append(name)

    return {k: dedup_list(v) for k, v in data.iteritems()}


def main(filename):
    messages = read_data(filename)
    names = trace_names(messages)

    # Write output
    with open('data/output.json', 'wb') as f:
        f.write(json.dumps(names))

    # Patch messages file with consistent username
    with open('data/patched_messages.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'user_id', 'avatar_url', 'sender', 'message', 'likes'])

        for msg in messages:
            for user_id, possible_names in names.iteritems():
                if msg[3] in possible_names:

                    # Convert name
                    msg[3] = possible_names[0]

                    # Convert time
                    msg[0] = int(msg[0]) * 1000
                    writer.writerow(msg)
                    break


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Track usernames over time.')
    parser.add_argument('filename')
    args = parser.parse_args()
    main(args.filename)
