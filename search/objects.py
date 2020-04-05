class Stack:

    def __init__(self, colour, height):
        self.colour = colour
        self.height = height

    def __str__(self):
        # eg. 03w = 3 white or 10b = 10 black
        return '{:>02d}{}'.format(self.height, self.colour[0])
