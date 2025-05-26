import os
import time
import math
from termcolor import colored

class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def hitsWall(self, point):
        #return point[0] < 0 or point[0] >= self._x or point[1] < 0 or point[1] >= self._y
        return round(point[0]) < 0 or round(point[0]) >= self._x or round(point[1]) < 0 or round(point[1]) >= self._y

    def setPos(self, pos, mark):
        self._canvas[round(pos[0])][round(pos[1])] = mark

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([col[y] for col in self._canvas]))

class TerminalScribe:
    def __init__(self, canvas, degrees=90):
        self.canvas = canvas
        self.trail = '.'
        self.mark = '*'
        self.framerate = 0.05
        self.pos = [0, 0]
        self.degrees = degrees
        self.radians = (self.degrees/180) * math.pi

    def setPosition(self, pos):
        self.pos = pos

    def setDirection(self, degrees):
        self.degrees = degrees
        self.radians = (self.degrees/180) * math.pi

    def up(self):
        pos = [self.pos[0], self.pos[1]-1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def down(self):
        pos = [self.pos[0], self.pos[1]+1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def right(self):
        pos = [self.pos[0]+1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def left(self):
        pos = [self.pos[0]-1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def forward(self):
        add_x = math.sin(self.radians)
        add_y = -math.cos(self.radians)
        pos = [self.pos[0] + add_x, self.pos[1] + add_y]
        if not self.canvas.hitsWall(pos):
            self.draw(pos)

    def drawSquare(self, size):
        for p in range(size):
            self.right()
        for p in range(size):
            self.down()
        for p in range(size):
            self.left()
        for p in range(size):
            self.up()

    def draw(self, pos):
        self.canvas.setPos(self.pos, self.trail)
        self.pos = pos
        self.canvas.setPos(self.pos, colored(self.mark, 'red'))
        self.canvas.print()
        time.sleep(self.framerate)

    def drawFunction(self, functionStr, duration):
        function = None
        if functionStr == 'up':
            function = self.up
        elif functionStr == 'down':
            function = self.down
        elif functionStr == 'right':
            function = self.right
        elif functionStr == 'left':
            function = self.left
        elif functionStr == 'forward':
            function = self.forward

        if not function:
            return

        for count in range(duration):
            function()


canvas = Canvas(30, 30)
scribe = TerminalScribe(canvas)

scribeData = [
    {'position': [15, 15], 'direction': 30, 'instructions' : [
        {'function': 'forward', 'duration' : 100},
    ]},
    {'position': [0, 0], 'direction': 135, 'instructions' : [
        {'function': 'forward', 'duration' : 10},
        {'function': 'down', 'duration' : 2},
        {'function': 'right', 'duration' : 20},
        {'function': 'down', 'duration' : 2},
    ]},
    {'position': [15, 0], 'direction': 180, 'instructions' : [
        {'function': 'down', 'duration' : 10},
        {'function': 'left', 'duration' : 10},
    ]},
]

for scribeDatum in scribeData:
    print(scribeDatum['direction'])
    scribe.setPosition(scribeDatum['position'])
    scribe.setDirection(scribeDatum['direction'])
    for instruction in scribeDatum['instructions']:
        scribe.drawFunction(instruction['function'], instruction['duration'])