import sys
import json

from search.util import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

    board_dict = load_board(data)

    print_board(board_dict, unicode=True, compact=True)
    print_board(board_dict, unicode=True, compact=False)

    print('END')


if __name__ == '__main__':
    main()
