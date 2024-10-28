import math
import random

from lib.variables import Variables


class City:

    def __init__(self):
        self.x = int(random.random() * Variables.WIDTH * .9 + Variables.WIDTH * .05)
        self.y = int(random.random() * Variables.HEIGHT * .9 + Variables.HEIGHT * .05)

    def distance(self, c):
        a_squared = math.fabs(self.x - c.x) ** 2
        b_squared = math.fabs(self.y - c.y) ** 2
        return math.sqrt(a_squared + b_squared)
