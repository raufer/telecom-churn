import sys
import yaml

from functools import reduce


def update_jsonpath(data, jsonpath, value):
    tmp = data
    paths = jsonpath.split('.')

    for i, path in enumerate(paths):
        if i < (len(paths) - 1):
            tmp = tmp[path]
        else:
            tmp[path] = value

    return data


def test_update_jsonpath():
    d = {'A': {'B': 1, 'C': 2}, 'F': 10, 'C': 20}
    expected = {'A': {'B': 100, 'C': 2}, 'F': 10, 'C': 20}
    result = update_jsonpath(d, 'A.B', 100)
    assert result == expected


if __name__ == '__main__':
    test_update_jsonpath()

    filename = sys.argv[1]
    key = sys.argv[2]
    value = sys.argv[3]

    with open(filename) as f:
        data = yaml.load(f)

    data = update_jsonpath(data, key, value)

    with open(filename, 'w') as f:
        yaml.dump(data, f)

