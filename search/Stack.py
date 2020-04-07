from math import sqrt


class Stack:

    def __init__(self, x: int, y: int, colour: str = None, height: int = 0):
        self.x, self.y = x, y

        if height > 0:
            assert colour

        if colour and colour.lower() in ['w', 'b']:
            self.colour = {'w': 'white', 'b': 'black'}[colour.lower()]
        else:
            self.colour = colour

        self.height = height

    def __str__(self):
        # eg. 03w = 3 white or 10b = 10 black
        if self.height > 0:
            return '{:>02d}{}'.format(self.height, self.colour[0].upper())
        return ''

    def boom(self):
        """
        reset values for boom action.
        does not actually affect close by tiles, see Board.boom()
        :return:
        """
        self.height = 0
        self.colour = None

    def get_coords(self):
        return self.x, self.y

    def get_distance_to(self, other_stack) -> int:
        """
        :param other_stack:
            the stack we want the distance in relation to self
        :return:
            integer distance to other_stack
        """

        if not self.is_inline_to(other_stack):
            raise Exception('other_stack must be inline with stack')

        d = sqrt((self.x - other_stack.x)**2 + (self.y - other_stack.y)**2)
        return int(d)

    def is_empty(self):
        return True if self.height == 0 else False

    def is_colour_empty(self, other_stack):
        if other_stack.is_empty():
            return True

        return self.colour == other_stack.colour

    def is_inline_to(self, other_stack):
        """
        :param other_stack:
            the stack we want to know if we share a line with
        :return:
            whether the stacks are inline with each other
        """
        if self.x != other_stack.x:
            return self.y == other_stack.y

        if self.y != other_stack.y:
            return self.x == other_stack.x

        return True

    def change_height(self, delta):
        self.height += delta

        assert self.height >= 0

        if self.height == 0:
            self.colour = None

        elif not self.colour:
            raise Exception('Stack must have a colour before having a height')
