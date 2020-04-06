from search.Stack import Stack
from search import util


class Board:
    size = 8

    def __init__(self, data: dict):
        self.board_dict = self.load_board_dict(data)

    def __str__(self):
        # TODO: could u check your print board function to see it right or not? I think it mix up the three number [n, x, y]
        #  in the form of input file, although I'm not sure.
        return util.print_board(self.board_dict, unicode=True, compact=False,
                                return_as_string=True)

    def __repr__(self):
        return super().__repr__() + '\n' + self.__str__()

    def __getitem__(self, item) -> Stack:
        return self.board_dict[item]

    def move(self, stack: Stack, moving_stack: Stack):
        """
        :param stack:
            the stack the tokens are being taken and moved from
        :param moving_stack:
            the portion of the stack that is being moved, represented as a
            separate stack, is agnostic as to what currently occupies the
            destination.
        :return:
        """

        try:
            destination_stack = self[moving_stack.get_coords()]
        except KeyError:
            raise InvalidMove('Location {} not on board'.format(moving_stack.get_coords()))

        # check moving_stack is same colour
        if stack.colour != moving_stack.colour:
            raise InvalidMove('Colours do not match, check the moving stack shares colour with stack')

        # check new location is same colour or empty
        if not stack.is_colour_empty(destination_stack):
            raise InvalidMove('{} is currently occupied by the other colour ({})'.format(moving_stack.get_coords(), destination_stack.colour))

        # check moving stack is not higher than original
        if moving_stack.height > stack.height:
            raise InvalidMove('Number of tiles being moved ({}) is greater than the stack\'s height ({})'.format(moving_stack.height, stack.height))

        # check new location is straight line from stack
        if not stack.is_inline_to(moving_stack):
            raise InvalidMove('{} -> {} is not straight line'.format(stack.get_coords(), moving_stack.get_coords()))

        # distance moving cannot be greater than height of moving stack
        d = stack.get_distance_to(moving_stack)
        if d > moving_stack.height:
            raise InvalidMove('Stack is moving more tiles ({}) than tokens ({}) being moved'.format(d, moving_stack.height))

        # moving the tokens
        stack.change_height(-moving_stack.height)
        destination_stack.colour = moving_stack.colour
        destination_stack.change_height(moving_stack.height)

        print('MOVE {} from {} to {}.'.format(moving_stack.height, stack.get_coords(), moving_stack.get_coords()))

    def boom(self, stack: Stack):
        stack.boom()
        print('BOOM at {}.'.format(stack.get_coords()))
        for x in range(stack.x - 1, stack.x + 2):
            for y in range(stack.y - 1, stack.y + 2):
                try:
                    current_stack = self[(x, y)]
                except KeyError:
                    # outside of board range, ignore
                    continue
                if not current_stack.is_empty():
                    self.boom(current_stack)

    def boom_without_print(self, stack: Stack):
        # TODO: I add this function which is almost the same with the above one, and it is used in the
        #  get_boom_points(total_explode_list, white_list, board: Board) function in Handler file.
        stack.boom()
        for x in range(stack.x - 1, stack.x + 2):
            for y in range(stack.y - 1, stack.y + 2):
                try:
                    current_stack = self[(x, y)]
                except KeyError:
                    # outside of board range, ignore
                    continue
                if not current_stack.is_empty():
                    self.boom(current_stack)

    # check board is empty or not
    # def __getitem__(self, item) -> Stack:
    #     return self.board_dict[item]
    def is_empty(self):
        # TODO: could u check if this function is right? I debug for a long time and not sure if wrong things happened there.
        n = 0
        for i in self.board_dict:
            stack = self.__getitem__(i)
            # print("Stack: ",stack)
            if stack.height == 0:
                n += 1;
                # print("n: ",n)
                continue
            else:
                break
        if n == len(self.board_dict):
            return True
        return False

    @staticmethod
    def load_board_dict(data: dict) -> dict:
        """
        :param data:
            a list (JSON array) of stacks, with each stack represented
            in the form [n,x,y].
        :return:
            A dictionary with (x, y) tuples as keys (x, y in range(8))
            and printable objects (e.g. strings, numbers) as values.
        """

        # initialising the board
        board_dict = {}
        for x in range(8):
            for y in range(8):
                board_dict[(x, y)] = Stack(x, y)

        # filling the starting board
        for colour in ['white', 'black']:
            for stack in data[colour]:
                x, y, n = stack
                board_dict[(x, y)] = Stack(x, y, colour, n)

        return board_dict


class InvalidMove(Exception):
    pass
