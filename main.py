# ----------------------- import -------------------------

# import file containing helper function and standard libs
import handler
import sys
import json

# ------------------- data preparing ----------------------
# Fraser: remove

sys.argv = [
            '',
            'test/test_cases/test-level-{}.json'.format(1)
        ]

# create a dictionary which contains input data
with open(sys.argv[1]) as file: data = json.load(file)

# ---------------- chess board preparing -------------------
# Fraser: now handled by Board class - remove

# create white and black token list
wList = data['white']
bList = data['black']

# create nest-listed board
board = [[0 for x in range(8)] for y in range(8)]
for i in range(8):
    for j in range(8):
        board[i][j] = [[i,j],['', 0]]
for elem in bList:
    n = elem[0]
    x = elem[2]
    y = elem[1]
    board[x][y] = [[x,y],['black', n]]
for elem in wList:
    n = elem[0]
    x = elem[2]
    y = elem[1]
    board[x][y] = [[x,y],['white', n]]
    # board[(x, y)] = Stack(x, y, colour, n)

# --------- divide the white token at beginning --------------
# Fraser: moved to search.__main__

# create divided path: in the format of [[1, 5, 3], n, x, y]
token_divided_path = []

# divide the white token at the beginning
handler.divide_token(wList,bList,token_divided_path)

# ------------ find expected explosion point -----------------
# Fraser: moved to search.__main__

# create list containing all the exploded points
total_explode_list = []

# get the all the points that make black token to explode
total_explode_list = handler.get_all_explode_coordinators(bList)

# get the frequency list of most useful explosion point with the descending trend
frequency_list = []
frequency_list = handler.get_frequency_list(total_explode_list)

# exclude repetitive points that explode same set of black token
useful_exploded_coordinator_list = handler.get_useful_exploded_coordinator(frequency_list, bList,wList)

# ---------------------- find path ----------------------------
# Fraser: moved to search.__main__

# transfer board to string list format
graph = handler.get_board_string_list(board)

# create path
path = []

# find all the paths and stored in format of dict
path_dict = {}
path_dict = handler.find_all_paths(useful_exploded_coordinator_list, wList, graph)

# ---------------------- print paths ----------------------------
# Fraser: moved to search.__main__ - needs changing

# print the information about divided token
for item in token_divided_path:
    print("MOVE ", item[1], "from ", (item[0][1],item[0][2]), "to ", (item[2], item[3]))

# print the information of different path of the white token
for white_chess in path_dict.keys():
    move_list = path_dict[white_chess]
    for index in range(len(move_list)-1):
        print("MOVE 1 from ", move_list[index], "to ", (move_list[index+1]))
        if index == len(move_list)-2:
            print("BOOM at ", (move_list[index+1]))



