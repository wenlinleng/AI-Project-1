import sys
import json
import os
import copy

from search.Board import Board
from search.Stack import Stack
from search import Handler as handler


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

    board = Board(data)

    # print(board)

    # create white and black token list
    white_list = data['white']
    black_list = data['black']

    # --------- divide the white token at beginning --------------

    # create divided path: in the format of [[1, 5, 3], n, x, y]
    token_divided_path = []

    # divide the white token at the beginning
    handler.divide_token(white_list, black_list, token_divided_path)

    # ------------ find expected explosion point -----------------

    # get all the points that make black token to explode
    total_explode_list = handler.get_all_explode_coordinates(black_list)

    # get the deep copy of board and as input of get_boom_points
    board_copy = copy.deepcopy(board)

    useful_exploded_coordinates_list = handler.get_boom_points(total_explode_list, white_list, board_copy)

    # ---------------------- find path ----------------------------

    # transfer board to string list format
    graph = handler.get_board_string_list(board)

    # get the path for all white tokens
    path_dict = handler.find_all_paths(useful_exploded_coordinates_list, white_list, graph)

    # ---------------------- print paths ----------------------------

    # print the information about divided token
    if len(token_divided_path) != 0:
        for item in token_divided_path:
            stack_from = board[(item[0][1], item[0][2])]
            moving_stack = Stack(item[2], item[3], 'w', 1)
            board.move(stack_from, moving_stack, print_action=True)

    # print the information of different path of the white token
    for white_chess, move_list in path_dict.items():
        if move_list:
            for index in range(len(move_list) - 1):
                stack_from = board[(int(move_list[index][1]), int(move_list[index][4]))]
                moving_stack = Stack(int(move_list[index + 1][1]), int(move_list[index + 1][4]), 'w', 1)
                board.move(stack_from, moving_stack, print_action=True)

                if index == len(move_list) - 2:
                    x = int(move_list[index + 1][1])
                    y = int(move_list[index + 1][4])
                    stack_boom = board[(x, y)]
                    print('BOOM at {}.'.format(stack_boom.get_coords()))
                    board.boom(stack_boom, print_action=False)

    # print(board)
    # print('END')


if __name__ == '__main__':
    main()
