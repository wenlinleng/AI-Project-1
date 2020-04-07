import sys
import json
import os

from search.Board import Board
from search.Stack import Stack
from search import Handler as handler


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

    board = Board(data)

    # create white and black token list
    white_list = data['white']
    black_list = data['black']

    # --------- divide the white token at beginning --------------

    # create divided path: in the format of [[1, 5, 3], n, x, y]
    token_divided_path = []

    # divide the white token at the beginning
    handler.divide_token(white_list, black_list, token_divided_path)

    # ------------ find expected explosion point -----------------

    # create list containing all the exploded points
    total_explode_list = []

    # get the all the points that make black token to explode
    total_explode_list = handler.get_all_explode_coordinators(black_list)

    print("total_explode_list: ", total_explode_list)

    handler.get_boom_points(total_explode_list, white_list, board)

    # get the frequency list of most useful explosion point with the descending trend
    frequency_list = []
    frequency_list = handler.get_frequency_list(total_explode_list)
    print("frequency_list: ", frequency_list)

    # exclude repetitive points that explode same set of black token
    useful_exploded_coordinator_list = handler.get_useful_exploded_coordinator(frequency_list, black_list, white_list)

    # ---------------------- find path ----------------------------

    # transfer board to string list format
    graph = handler.get_board_string_list(board)

    # create path
    path = []

    # find all the paths and stored in format of dict
    path_dict = {}

    path_dict = handler.find_all_paths(useful_exploded_coordinator_list, white_list, graph)

    # ---------------------- print paths ----------------------------

    # print the information about divided token
    if len(token_divided_path) != 0:
        for item in token_divided_path:
            # TODO board.move()
            stack_from = Stack(item[0][1], item[0][2], 'w', item[1])
            stack_to = Stack(item[2], item[3], 'w')
            board.move(stack_from, stack_to)
            # print("MOVE ", item[1], "from ", (item[0][1], item[0][2]), "to ", (item[2], item[3]))

    # print the information of different path of the white token
    for white_chess in path_dict.keys():
        move_list = path_dict[white_chess]
        for index in range(len(move_list) - 1):
            stack_from = Stack(int(move_list[index][1]), int(move_list[index][4]), 'w', 1, )
            stack_to = Stack(int(move_list[index + 1][1]), int(move_list[index + 1][4]), 'w', 1)
            board.move(stack_from, stack_to)
            # TODO board.move()
            if index == len(move_list) - 2:
                # TODO baord.boom()
                x = int(move_list[index + 1][1])
                y = int(move_list[index + 1][4])
                stack_boom = Stack(x, y, 'w', 1)
                print("stack_boom.get_coords(): ", stack_boom.get_coords())
                board.boom(stack_boom)

    print('END')


def temp1():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = Board(data)

    print(board)

    stack_to_move = board[(1, 4)]
    moving_stack = Stack(1, 3, 'w', 1)
    board.move(stack_to_move, moving_stack)

    print(board)

    stack_to_boom = board[(1, 3)]
    board.boom(stack_to_boom)

    print(board)


def temp2():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board = Board(data)

    from search.util import print_board

    print_board(board.board_dict)


if __name__ == '__main__':
    os.chdir('..')
    sys.argv = [
        '',
        'test/test_cases/test-level-1.json'
    ]
    temp1()
