import sys
import json

from search.util import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

    print(json.dumps(data, indent=4))

    # print_board(data)

    print('END')


if __name__ == '__main__':
    main()
