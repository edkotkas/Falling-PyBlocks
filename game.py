import pygame
import random
import sys
import time

GRID_ENABLED = False


class Game:
    def __init__(self):
        """
        Falling PyBlocks, a clone of Tetris.
        :return:
        """
        pygame.init()

        # grid divider
        self.grid_x = 10
        self.grid_y = 20

        # game speed
        self.game_speed = 0.5

        # colours
        self.colour_clear = (25,) * 3

        # window setup
        self.window_width = 460
        self.window_height = 460

        # playable area sizes
        self.display_width = 320
        self.display_height = 440

        # grid box sizes
        self.grid_real_x = self.display_width / self.grid_x
        self.grid_real_y = self.display_height / self.grid_y

        # score text box sizes
        self.score_width = 100
        self.score_height = 40

        self.score = 0

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.blocks = Blocks(
            (self.grid_x, self.grid_y),
            (self.display_width, self.display_height),
            (4, 0)
        )

    def loop(self, frames):
        """
        Main game loop.
        :param frames: integer to represent how many frames to display per second
        :return: main game loop
        """
        current_shape = None
        direction = None
        rotation = False
        start_time = time.time()
        while True:

            # fps
            pygame.time.Clock().tick(frames)

            # clear screen
            self.screen.fill(self.colour_clear)

            for event in pygame.event.get():

                # exit if X is pressed
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    # key presses listener
                    if event.key == pygame.K_SPACE or event.key == pygame.K_DOWN:
                        self.game_speed = 0.1
                    if event.key == pygame.K_RIGHT:
                        direction = self.blocks.MOVE_RIGHT
                    if event.key == pygame.K_LEFT:
                        direction = self.blocks.MOVE_LEFT
                    if event.key == pygame.K_UP:
                        # rotate the block shape clockwise
                        self.blocks.rotate()

                # if any key released set the game speed to normal
                if event.type == pygame.KEYUP:
                    self.game_speed = 0.5

                    rotation = False

                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        direction = None

            # bottom bar for score
            pygame.draw.rect(self.screen, (20,) * 3, (0, 0, self.display_width, self.display_height))

            # the score text
            score = pygame.font.SysFont("monospace", 18)
            score = score.render("Score: %d" % self.score, 1, (200,) * 3)
            self.screen.blit(score, (10, self.display_height))

            # if no shape, make one
            if current_shape is None:
                self.blocks.new()
                current_shape = self.blocks.get()
            else:
                # if direction is set, move
                if direction is not None:
                    self.blocks.move(direction)

                # if rotation is true, rotate
                if rotation is True:
                    self.blocks.rotate()

                # make the blocks fall after a fraction of a second
                if time.time() - start_time > self.game_speed:
                    self.blocks.move(self.blocks.MOVE_DOWN)
                    start_time = time.time()

                # render the block shape to the screen
                for shape in self.blocks.get():
                    # convert the grid coordinates to pixel location
                    shape_x, shape_y = self.pixel(*shape)

                    pygame.draw.rect(self.screen, (100,) * 3, (
                        shape_x, shape_y,
                        self.grid_real_x, self.grid_real_y), 3)

            # render the block collection
            the_blocks = [i for i in self.blocks.display()]
            if len(the_blocks) > 0:
                for block_x, block_y in the_blocks:
                    block_x, block_y = self.pixel(block_x, block_y)
                    pygame.draw.rect(self.screen, (100,) * 3, (
                        block_x, block_y,
                        self.grid_real_x, self.grid_real_y))

            # if the bottom line is full, add score
            if self.blocks.line():
                self.score += 1

            # update screen
            pygame.display.flip()

    def grid(self, enabled=True):
        """
        Displays the grid on the playable area.
        :param enabled: boolean
        :return:
        """
        if enabled:
            for column in range(self.grid_x):
                for row in range(self.grid_y):
                    pygame.draw.rect(self.screen, (10,) * 3, (
                        self.grid_real_x * column, self.grid_real_y * row,
                        self.grid_real_x, self.grid_real_y), 1)

    def pixel(self, x=0, y=0):
        """
        Converts grid coordinates to pixel coordinates.
        :param x: int between 0 and 10
        :param y: int between 0 and 20
        :return: converted coordinates
        """
        return x * (self.display_width / 10), y * (self.display_height / 20)


class Blocks:
    def __init__(self, (grid_x, grid_y), (display_width, display_height), (start_x, start_y)=(0, 0)):
        """
        Game block manager.
        :return:
        """

        # helpers
        self.MOVE_DOWN = 0
        self.MOVE_RIGHT = 1
        self.MOVE_LEFT = 2

        # display properties
        self._grid_x = grid_x
        self._grid_y = grid_y
        self._display_width = display_width
        self._display_height = display_height
        self._grid_real_x = self._display_width / self._grid_x
        self._grid_real_y = self._display_height / self._grid_y

        # shape properties
        self._shape = []
        self._current_shape = None
        self._rotation = 0

        # shape position
        self._x = start_x
        self._y = start_y
        self._x_pos = 0
        self._y_pos = 0

        self._x_right = 0
        self._x_left = self._grid_x
        self._y_bottom = 0

        # shapes history
        self._record = []

        # block shapes
        self._shapes = {
            'O': (
                ((self._x, self._y), (self._x + 1, self._y + 1), (self._x + 1, self._y), (self._x, self._y + 1)),
            ),
            'I': (
                ((self._x, self._y), (self._x, self._y + 1), (self._x, self._y + 2), (self._x, self._y + 3)),
                ((self._x, self._y), (self._x + 1, self._y), (self._x + 2, self._y), (self._x + 3, self._y))
            ),
            'S': (
                ((self._x, self._y + 1), (self._x + 1, self._y + 1), (self._x + 1, self._y), (self._x + 2, self._y)),
                ((self._x, self._y), (self._x, self._y + 1), (self._x + 1, self._y + 1), (self._x + 1, self._y + 2))
            ),
            'Z': (
                ((self._x, self._y), (self._x + 1, self._y), (self._x + 1, self._y + 1), (self._x + 2, self._y + 1)),
                ((self._x, self._y + 1), (self._x, self._y + 2), (self._x + 1, self._y), (self._x + 1, self._y + 1))
            ),
            'L': (
                ((self._x, self._y), (self._x, self._y + 1), (self._x, self._y + 2), (self._x + 1, self._y + 2)),
                ((self._x, self._y), (self._x, self._y + 1), (self._x + 1, self._y), (self._x + 2, self._y)),
                ((self._x, self._y), (self._x + 1, self._y), (self._x + 1, self._y + 1), (self._x + 1, self._y + 2)),
                ((self._x, self._y + 1), (self._x + 1, self._y + 1), (self._x + 2, self._y + 1), (self._x + 2, self._y))
            ),
            'J': (
                (
                (self._x, self._y + 2), (self._x + 1, self._y + 2), (self._x + 1, self._y + 1), (self._x + 1, self._y)),
                ((self._x, self._y), (self._x, self._y + 1), (self._x + 1, self._y + 1), (self._x + 2, self._y + 1)),
                ((self._x, self._y), (self._x + 1, self._y), (self._x, self._y + 2), (self._x, self._y + 1)),
                ((self._x, self._y), (self._x + 1, self._y), (self._x + 2, self._y), (self._x + 2, self._y + 1))
            ),
            'T': (
                ((self._x, self._y), (self._x + 1, self._y), (self._x + 1, self._y + 1), (self._x + 2, self._y)),
                (
                (self._x, self._y + 1), (self._x + 1, self._y), (self._x + 1, self._y + 1), (self._x + 1, self._y + 2)),
                (
                (self._x, self._y + 1), (self._x + 1, self._y), (self._x + 1, self._y + 1), (self._x + 2, self._y + 1)),
                ((self._x, self._y), (self._x, self._y + 1), (self._x + 1, self._y + 1), (self._x, self._y + 2))
            )
        }

    def new(self, shape=None):
        """
        Creates a new shape.
        :param shape: optional string from self._shapes.keys()
        :return:
        """
        self._shape = []

        # check if we want a predefined shape to appear
        if shape is not None:
            self._current_shape = shape
        else:
            self._current_shape = random.choice(self._shapes.keys())

        # apply shape to the self._shape list with current rotation
        shape = self._shapes.get(self._current_shape)[self._rotation]
        for x, y in shape:
            x, y = x + self._x_pos, y + self._y_pos
            self._shape.append((x, y))

            # collision detection
            if self._x_right < x:
                self._x_right = x
            if self._x_left > x:
                self._x_left = x
            if self._y_bottom < y:
                self._y_bottom = y

    def get(self):
        """
        Returns the shape in the form of a list for printing/rendering.
        :return: list of tuples
        """
        return self._shape

    def move(self, direction):
        """
        Move the blocks in a specific direction.
        :param direction: string representing direction
        :return: change current shape position to a new one
        """

        # check if the block shape has reached the bottom of the screen
        if self._y_bottom + 1 > self._grid_y - 1:
            self.record()

        # check if the new shape touches a block from the collection
        for x, y in self._shape:
            for xx, yy in self.display():
                if x == xx and y + 1 == yy:
                    if y < 2:
                        print "game over"
                    else:
                        self.record()

        # check for direction and if it's in the inbound
        if direction is self.MOVE_DOWN:
            self._y_pos += 1
        if direction is self.MOVE_LEFT and self._x_left != 0:
            self._x_pos -= 1
        if direction is self.MOVE_RIGHT and self._x_right != self._grid_x-1:
            self._x_pos += 1

        # make the new shape
        self.new(self._current_shape)

    def rotate(self):
        """
        Rotate the shape, select next available
        :return: change current shape rotation to a new one
        """

        # check if the next rotation is available, if not revert to original shape
        if self._rotation != len(self._shapes[self._current_shape]) - 1:
            self._rotation += 1
        else:
            self._rotation = 0

        # make the new shape
        self.new(self._current_shape)

    def record(self):
        """
        Record the previous shapes from their last position.
        :return:
        """

        # used for saving position when the block has landed
        for block in self._shape:
            self._record.append(block)
        self.clear()

    def display(self):
        """
        Generator for the self._record list
        :return: list of tuples
        """
        for i in self._record:
            yield i

    def clear(self):
        """
        Clear the setup.
        :return:
        """

        self._shape = []
        self._current_shape = None
        self._rotation = 0

        self._x_pos = 0
        self._y_pos = 0

        self._x_right = 0
        self._x_left = self._grid_x
        self._y_bottom = 0

    def line(self):
        """
        Bottom line checker.
        :return: boolean whether there's a full line
        """

        for grid_y in range(self._grid_y):
            x_line = [(x, y) for x, y in self.display() if y is grid_y]

            if len(x_line) == self._grid_x:
                for line in x_line:
                    self._record.remove(line)

                for i, (_, y) in enumerate(self._record):
                    if y < grid_y:
                        self._record[i] = self._record[i][0], self._record[i][1] + 1

                return True


if __name__ == "__main__":
    fpb = Game()
    fpb.loop(30)