from search.Stack import Stack
from search import util


class Board:
    size = 8

    def __init__(self, data: dict):
        self.board_dict = self.load_board_dict(data)

    def __str__(self):
        return util.print_board(self.board_dict, unicode=True, compact=False,
                                return_as_string=True)

    def __repr__(self):
        return super().__repr__() + '\n' + self.__str__()

    def __getitem__(self, item) -> Stack:
        return self.board_dict[item]

    def move(self, stack: Stack, moving_stack: Stack):
        """
        A move action (a ‘move’) involves moving some or all of the tokens in
        a stack some number of squares in one of the four cardinal directions
        — up, down, left, or right. From a stack of n tokens (n ≥ 1), the
        player may move up to n of those tokens a distance of up to n squares
        in a single direction. The tokens may not move diagonally, and must
        move by at least one square. The destination square may be unoccupied,
        or it may already be occupied by tokens of the same colour — in this
        case, the moved tokens join the tokens on the destination square,
        forming a new stack whose number of tokens is equal to the number of
        tokens originally on the square plus the number of tokens moved onto
        the square. The tokens may not move onto a square occupied by the
        opponent’s tokens. However, the tokens may move ‘over’ it (as long as
        the total distance moved is not more than n squares). A token cannot
        move off the board. There is no limit to the number of tokens in a
        stack.

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
            raise InvalidMove(
                'Location {} not on board'.format(moving_stack.get_coords())
            )

        # check moving_stack is same colour
        if stack.colour != moving_stack.colour:
            raise InvalidMove(
                'Colours do not match, check the moving stack shares colour with stack'
            )

        # check new location is same colour or empty
        if not stack.is_colour_empty(destination_stack):
            raise InvalidMove(
                '{} is currently occupied by the other colour ({})'
                .format(moving_stack.get_coords(), destination_stack.colour)
            )

        # check moving stack is not higher than original
        if moving_stack.height > stack.height:
            raise InvalidMove(
                'Number of tiles being moved ({}) is greater than the stack\'s height ({})'
                .format(moving_stack.height, stack.height)
            )

        # check new location is straight line from stack
        if not stack.is_inline_to(moving_stack):
            raise InvalidMove(
                '{} -> {} is not straight line'
                .format(stack.get_coords(), moving_stack.get_coords())
            )

        # distance moving cannot be greater than height of moving stack
        d = stack.get_distance_to(moving_stack)
        if d > moving_stack.height:
            raise InvalidMove(
                'Stack is moving more tiles ({}) than tokens ({}) being moved'
                .format(d, moving_stack.height)
            )

        # moving the tokens
        stack.change_height(-moving_stack.height)
        destination_stack.colour = moving_stack.colour
        destination_stack.change_height(moving_stack.height)

        """
        To output a move action, print a line in the format ‘MOVE n from 
        (xa, ya) to (xb, yb).’ where n is the number of tokens in the stack to 
        move, (xa, ya) are the coordinates of the moving tokens before the 
        move, and (xb, yb) are the coordinates after the move. Note: If you 
        want to output the action of moving a whole stack, n would just be 
        equal to the number of tokens in the stack.
        """
        print('MOVE {} from {} to {}.'.format(
            moving_stack.height, stack.get_coords(), moving_stack.get_coords()
        ))

    def boom(self, stack: Stack, print_action=True):
        """
        A boom action (a ‘boom’) involves choosing a stack to explode. All of
        the tokens in this stack are removed from play as a result of this
        explosion. Additionally, the explosion immediately causes any stacks
        (of either color) in a 3 × 3 area surrounding this stack to also
        explode. These explosions may go on to trigger further explosions in
        a recursive chain reaction. In this way, long chains of stacks may be
        removed from play as the result of a single action.

        :param stack:
            stack being 'boom'ed
        :param print_action:
            True if the action should be printed
        :return:
        """
        stack.reset()
        if print_action:
            """
            To output a boom action, print a line in the format 
            ‘BOOM at (x, y).’ where (x, y) are the coordinates of the stack 
            initiating the explosion.
            """
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

    def is_empty(self) -> bool:
        """
        Checks if there are no pieces left on the board
        :return: True if the board is empty
        """
        return all([i.height == 0 for i in self.board_dict.values()])

    def clear_white_tokens(self):
        """
        clears all white pieces from the board
        :return:
        """
        for stack in self.board_dict.values():
            if stack.colour[0] == 'w':
                stack.reset()

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
                n, x, y = stack
                board_dict[(x, y)] = Stack(x, y, colour, n)

        return board_dict


class InvalidMove(Exception):
    pass
