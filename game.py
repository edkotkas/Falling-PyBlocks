import pygame
import random
import sys

GRID_ENABLED = True


class Game:

    def __init__(self):
        """
        Falling PyBlocks, a clone of Tetris.
        :return:
        """
        pygame.init()

        # grid shortcut
        self.GRID_X = 10
        self.GRID_Y = 20

        # colours
        self.colour_clear = (25,)*3

        # window setup
        self.window_width = 460
        self.window_height = 460

        self.display_width = 320
        self.display_height = 440

        self.score_width = 100
        self.score_height = 40

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.blocks = Blocks()

    def loop(self, frames):
        """
        Main game loop.
        :param frames: integer to represent how many frames to display per second
        :return: the game
        """
        scroll_y = 0
        scroll_x = 0
        lowest = 0
        highest = 418
        speed = 500
        current_shape = None
        move = None
        trajectory = []
        while True:

            pygame.time.Clock().tick(frames)

            # clear screen
            self.screen.fill(self.colour_clear)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    if event.key == pygame.K_SPACE:
                        speed = 100

                    if current_shape is not None:
                        if event.key == pygame.K_LEFT:
                            move = 'left'
                        if event.key == pygame.K_RIGHT:
                            move = 'right'

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        speed = 500
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            move = None

            pygame.draw.rect(self.screen, (20,)*3, (0, 0, self.display_width, self.display_height))

            x = self.display_width/self.GRID_X
            y = self.display_height/self.GRID_Y

            if GRID_ENABLED is True:
                for column in range(self.GRID_X):
                    for row in range(self.GRID_Y):
                        pygame.draw.rect(self.screen, (10,)*3, (x*column, y*row, x, y), 1)

            score = pygame.font.SysFont("monospace", 18)
            score = score.render("Score: 1000", 1, (200,)*3)
            self.screen.blit(score, (10, self.display_height))

            pygame.time.delay(speed)

            if current_shape is None:
                self.blocks.new()
                current_shape = self.blocks.get()

            allowed = True
            for i, (xp, yp) in enumerate(self.blocks.get()):
                xp, yp = self.pixel(xp+scroll_x, yp+scroll_y)
                trajectory.append((xp, yp))

                if i <= 3:
                    if lowest < yp:
                        lowest = yp

                if lowest == y*(self.GRID_Y-1):
                    allowed = False

                pygame.draw.rect(self.screen, (100,)*3, (xp, yp, x, y), 3)

                # fix this
                if move == 'left':
                    scroll_x -= 1
                if move == 'right':
                    scroll_x += 1

                # modify this and anything below
                if i == 3 and allowed:
                    if highest > yp:
                        highest = yp
                    scroll_y += 1

                if lowest == y*(self.GRID_Y-1):
                    for track in trajectory[-4:]:
                        self.blocks.record(track)
                    current_shape = None
                    scroll_y = 0
                    lowest = 0

            # testing block recording functino
            # for rec_x, rec_y in self.blocks.display():
            #     pygame.draw.rect(self.screen, (100,)*3, (rec_x, rec_y, x, y), 3)

            pygame.display.flip()

    def pixel(self, x=0, y=0):
        """
        Converts grid coordinates to pixel coordinates.
        :param x: int between 0 and 10
        :param y: int between 0 and 20
        :return: converted coordinates
        """
        return x*(self.display_width/10), y*(self.display_height/20)


class Blocks:

    def __init__(self):
        """
        Manage the block shapes.
        :return:
        """
        self._shape = []
        self._rotation = 0

        self._x = 0
        self._y = 0

        self._record = []

        self._shapes = {
            'O': (
                ((self._x, self._y), (self._x+1, self._y+1), (self._x+1, self._y), (self._x, self._y+1)),
            ),
            'I': (
                ((self._x, self._y), (self._x, self._y+1), (self._x, self._y+2), (self._x, self._y+3)),
                ((self._x, self._y), (self._x+1, self._y), (self._x+2, self._y), (self._x+3, self._y))
            ),
            'S': (
                ((self._x, self._y+1), (self._x+1, self._y+1), (self._x+1, self._y), (self._x+2, self._y)),
                ((self._x, self._y), (self._x, self._y+1), (self._x+1, self._y+1), (self._x+1, self._y+2))
            ),
            'Z': (
                ((self._x, self._y), (self._x+1, self._y), (self._x+1, self._y+1), (self._x+2, self._y+1)),
                ((self._x, self._y+1), (self._x, self._y+2), (self._x+1, self._y+1), (self._x, self._y+1))
            ),
            'L': (
                ((self._x, self._y), (self._x, self._y+1), (self._x, self._y+2), (self._x+1, self._y+2)),
                ((self._x, self._y), (self._x, self._y+1), (self._x+1, self._y), (self._x+2, self._y)),
                ((self._x, self._y), (self._x+1, self._y), (self._x+1, self._y+1), (self._x+1, self._y+2)),
                ((self._x, self._y+1), (self._x+1, self._y+1), (self._x+2, self._y+2), (self._x+2, self._y))
            ),
            'J': (
                ((self._x, self._y+2), (self._x+1, self._y+2), (self._x+1, self._y+1), (self._x+1, self._y)),
                ((self._x, self._y), (self._x, self._y+1), (self._x+1, self._y+1), (self._x+2, self._y+1)),
                ((self._x, self._y), (self._x, self._y+1), (self._x, self._y+2), (self._x, self._y+1)),
                ((self._x, self._y), (self._x+1, self._y), (self._x+2, self._y), (self._x+2, self._y+1))
            ),
            'T': (
                ((self._x, self._y), (self._x+1, self._y), (self._x+1, self._y+1), (self._x+2, self._y)),
                ((self._x, self._y+1), (self._x+1, self._y), (self._x+1, self._y+1), (self._x+2, self._y)),
                ((self._x, self._y+1), (self._x+1, self._y), (self._x+1, self._y+1), (self._x+2, self._y+1)),
                ((self._x, self._y), (self._x, self._y+1), (self._x+1, self._y+1), (self._x+2, self._y))
            )
        }

    def new(self):
        self._shape = []
        shape = self._shapes.get(random.choice(self._shapes.keys()))[self._rotation]
        for x, y in shape:
            self._shape.append((x, y))

    def get(self):
        return self._shape

    def move(self, direction):
        """
        Move the blocks in a specific direction.
        :param direction:
        :return:
        """

    def record(self, pos):
        self._record.append(pos)

    def display(self):
        for i in self._record:
            yield i

    def clear(self):
        self._shape = []

if __name__ == "__main__":
    fpb = Game()
    fpb.loop(30)