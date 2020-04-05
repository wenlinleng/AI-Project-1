import sys
import json

from search.Board import Board
from search.Stack import Stack


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

    board = Board(data)

    print(board)

    board.move(board[(1,4)], Stack(3,4,'black',3))

    print(board)

    print('END')


if __name__ == '__main__':
    main()
