import pygame
import sys
import time

from blocks import Blocks

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
                        self.game_speed = 0.05
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

                if direction is not None:
                    self.blocks.move(direction)

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

if __name__ == "__main__":
    fpb = Game()
    fpb.loop(30)