# function: print board
def print_board(board):
    for i in range(8):
        print('\n')
        for j in range(8):
            print(board[i][j], end='')


# function: input a coordinator with format [x, y], return the explode coordinator around it.
def get_explode_coordinators(coordinator):
    explode_coordinators = []
    for i in range(1, 4):
        x = coordinator[0] - 1  # 0
        y = coordinator[1] - 1 + i - 1  # 0
        for j in range(3):  # 1,2,3
            explode_coordinator = [x, y]
            if (coordinator != explode_coordinator):
                explode_coordinators.append(explode_coordinator)
            x += 1
    return explode_coordinators


# function: find the coordinator of the explode point by processing the black list
def get_all_explode_coordinators(black_list):
    total_explode_list = []
    for i in black_list:
        coordinator = [i[1], i[2]]
        explode_coordinators = get_explode_coordinators(coordinator)
        for j in explode_coordinators:
            total_explode_list.append(j)
    return total_explode_list


# function: get the frequency list with descending sequence
def get_frequency_list(total_explode_list):
    frequency_list = []
    for item in total_explode_list:
        count = 0
        for coordinator in total_explode_list:
            if coordinator == item:
                count += 1
        frequency_list.append([item[0], item[1], count])
    frequency_list = list(set([tuple(t) for t in frequency_list]))
    frequency_list = sorted(frequency_list, key=(lambda x: x[2]), reverse=True)
    return frequency_list


# function: find the explode black token of given coordinate
def get_exploded_black_coordinator(coordinator, black_list):
    coordinator_x = coordinator[0]
    coordinator_y = coordinator[1]
    exploded_list = []
    number = 0
    for item in black_list:
        number += 1
        x = item[1]
        y = item[2]
        if (coordinator_x in [x - 1, x, x + 1]) & (coordinator_y in [y - 1, y, y + 1]):
            exploded_list.append(item)
    return exploded_list


# function: test the repetitive points that explode same set of black token, only keep first one
def get_useful_exploded_coordinator(frequenct_list, black_list, white_list):
    total_exploded_list = []
    for coordinator in frequenct_list:
        exploded_list = get_exploded_black_coordinator(coordinator, black_list)
        total_exploded_list.append([coordinator, exploded_list])
    previous_item = total_exploded_list[0]
    total_exploded_list_without_1st = total_exploded_list[1:len(total_exploded_list)]
    order = 1
    for item in total_exploded_list_without_1st:
        if item[1] == previous_item[1]:
            total_exploded_list.pop(order)
        else:
            previous_item = item
            order += 1
    useful_exploded_coordinator_list = []
    for white_item in total_exploded_list:
        useful_exploded_coordinator_list.append(white_item[0])
    return useful_exploded_coordinator_list[0:len(white_list)]


# function: divide the token at the beginning of the game, find a available point to put
def divide_token(white_list, black_list, path):
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
            path.append([item, 1, movable_list[0][0], movable_list[0][1]])
            n = white_list[num][0]
            item = [1, movable_list[1][0], movable_list[1][1]]
        num += 1


# function: transfer board to string list format
def get_board_string_list(chess_board):
    graph = {}
    for row in range(8):
        for item in chess_board[row]:
            x = item[0][0]
            y = item[0][1]
            value_list = []
            for row_2 in range(8):
                for surrounding_item in chess_board[row_2]:
                    if (surrounding_item[0] in [[x - 1, y], [x + 1, y], [x, y + 1], [x, y - 1]]) & (
                            surrounding_item[1][1] == 0):
                        value_list.append(str(surrounding_item[0]))
                graph[str(item[0])] = value_list
    return graph


# function: input a white chess coordinator, find the path to the destination point
def find_path(graph, start, end, path=[]):
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
    path = path + [start]
    if start == end:
        return path
    shortestPath = []
    if start in graph:
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortestPath or len(newpath) < len(shortestPath):
                        shortestPath = newpath

    return shortestPath


# function: find all the path with dict of white_list
def find_all_paths(useful_exploded_list, white_list, graph):
    path_dict = {}
    for order in range(len(white_list)):
        white_point = white_list[order]
        destination_point = useful_exploded_list[order]
        start_point = str([white_point[1], white_point[2]])
        end_point = str([destination_point[0], destination_point[1]])
        path = find_path(graph, start_point, end_point)
        path_dict[str(start_point)] = path
    return path_dict
