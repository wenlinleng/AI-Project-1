import itertools
import copy

from search.Board import Board
from search.Stack import Stack


class Coordinate:
    # TODO replace all "coordinates" with this object. Lists are confusing
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str([self.x, self.y])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def get_explode_coordinates(coordinate):
    """
    Input a coordinate with Class Coordinate, return the explosion coordinates around it.

    :param coordinate: the stack of token in board
    :return: a coordinate list that boom at this coordinate make input coordinate disappear
    """
    explode_coordinates = []
    for x in range(coordinate.x - 1, coordinate.x + 2):
        for y in range(coordinate.y - 1, coordinate.y + 2):
            try:
                current_coor = Coordinate(x, y)
            except KeyError:
                continue
            if not coordinate.__eq__(current_coor) :
                if ( 7 >= x >= 0) & ( 7 >= y >= 0):
                    explode_coordinates.append(current_coor)
    return explode_coordinates


def get_all_explode_coordinates(black_list):
    """
    Find the coordinates of the exploded points by processing the black list

    :param black_list: the list of black stacks of token in board
    :return: a coordinate list that boom at this coordinate make any black coordinates disappear
    """
    total_explode_list = []
    for i in black_list:
        coordinate = Coordinate(i[1], i[2])
        explode_coordinators = get_explode_coordinates(coordinate)
        for j in explode_coordinators:
            total_explode_list.append(j)
    return total_explode_list


def get_boom_points(total_explode_list, white_list, board_copy: Board):
    """
    Loop the exploded list and find the combination with fewer number of boom coordinates to clear all the black tokens

    :param total_explode_list: a coordinate list that boom at this coordinate make any black coordinates disappear
    :param white_list: the list of white stacks of token in board
    :param board_copy: copied chess board
    :return: the fewer number of token that boom all the black tokens -> tuple with Coordinates inside
    """

    # create the list of variable length array
    explode_combinations = []
    for i in range(1, len(white_list) + 1):
        iter = itertools.combinations(total_explode_list, i)
        explode_combinations.append(list(iter))

    # wipe out white chess
    board_copy.clear_white_tokens()

    # check every list for the emptyness after booming
    for lst in explode_combinations:

        for order in range(len(lst)):
            # put the white stack I want them to boom
            test_board = copy.deepcopy(board_copy)
            for item in lst[order]:
                test_stack = Stack(item.x, item.y, 'W', 1)
                test_board.boom(test_stack, False)

            if test_board.is_empty():
                return lst[order]


def divide_token(white_list, black_list, path):
    """
    Divide the white token at the beginning of the game, find a available point to put.

    :param white_list
    :param black_list
    :param path: save the way white chess move
    """
    white_list_copy = white_list.copy()
    black_list_copy = black_list.copy()
    white_list_copy.extend(black_list_copy)
    sum_list = white_list_copy
    num = 0
    for item in white_list:
        n = item[0]
        while n != 1:
            x = item[1]
            y = item[2]
            movable_list = []
            for i in range(1, n + 1):
                movable_list.append([x + i, y])
                movable_list.append([x - i, y])
                movable_list.append([x, y + i])
                movable_list.append([x, y - i])
            order = 0
            for j in movable_list:
                for k in sum_list:
                    if j == [k[1], k[2]]:
                        movable_list.pop(order)
                order += 1
            white_list.append([1, movable_list[0][0], movable_list[0][1]])
            white_list[num][0] -= 1
            path.append([item, n, movable_list[0][0], movable_list[0][1]])
            n = white_list[num][0]
            item = [1, movable_list[1][0], movable_list[1][1]]
        num += 1


# function: transfer board to string dict format
def get_board_string_list(chess_board):
    """
    :param chess_board:
    :return: dict [(x, y)]:  ['(1, 2)', '(3, 4)']
    """
    graph = {}

    for x in range(8):
        for y in range(8):
            value_list = []
            for surrounding_coords in [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]:
                try:
                    stack = chess_board[surrounding_coords]
                    if stack.is_empty():
                        value_list.append(str(list(stack.get_coords())))
                except KeyError:
                    continue
            graph[str(str([x,y]))] = value_list
    return graph


def find_path(graph, start, end, path=[]):
    """
    Input a white chess coordinates, find the path to the destination point

    :param graph: string dict format of board, show all the path a coordinate can move
    :param start: start coordinate
    :param end: end coordinate
    :param path: save the path of white token move
    """
    path = path + [start]
    if start == end:
        return path
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None


# function: find the shortest path --> not used, take too much time to run
def find_shortest_path(graph, start, end, path=[]):
    """
    Input a white chess coordinates, find the shortest path to the destination point, but not used, because of taking
    too much time to run

    :param graph: string dict format of board, show all the path a coordinate can move
    :param start: start coordinate
    :param end: end coordinate
    :param path: save the path of white token move
    """
    path = path + [start]
    if start == end:
        return path
    shortest_path = []
    if start in graph:
        for node in graph[start]:
            if node not in path:
                new_path = find_shortest_path(graph, node, end, path)
                if new_path:
                    if not shortest_path or len(new_path) < len(shortest_path):
                        shortest_path = new_path

    return shortest_path


def find_all_paths(useful_exploded_list, white_list, graph):
    """
    Find all the path with dict of white_list

    :param useful_exploded_list: the best point for a white token to exlplode
    :param white_list: a list of white tokens
    :param graph: string dict format of board that represent all the possible move of any coordinate
    """

    path_dict = {}
    for order in range(len(useful_exploded_list)):
        white_point = white_list[order]
        destination_point = useful_exploded_list[order]
        start_point = str([white_point[1], white_point[2]])
        end_point = str([destination_point.x, destination_point.y])
        path = find_path(graph, start_point, end_point)
        path_dict[str(start_point)] = path
    return path_dict