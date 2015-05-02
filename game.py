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

        # game status
        self.over = False

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

        self.top_players = {1: ('Player', 1000)}

    def loop(self, frames):
        """
        Main game loop.
        :param frames: integer to represent how many frames to display per second
        :return: main game loop
        """
        shape_current = None
        direction = None
        start_time = time.time()
        move_time = 0
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
                        move_time = time.time()
                        direction = self.blocks.MOVE_RIGHT
                    if event.key == pygame.K_LEFT:
                        move_time = time.time()
                        direction = self.blocks.MOVE_LEFT
                    if event.key == pygame.K_UP:
                        # rotate the block shape clockwise
                        self.blocks.rotate()

                # if any key released set the game speed to normal
                if event.type == pygame.KEYUP:
                    self.game_speed = 0.5
                    direction = None

            # play area background
            pygame.draw.rect(self.screen, (20,) * 3, (0, 0, self.display_width, self.display_height))

            # side panel background
            pygame.draw.rect(self.screen, (25,) * 3, (
                self.display_width, 0,
                self.window_width - self.display_width, self.window_height))

            # next shape panel
            next_shape = pygame.font.SysFont("monospace", 16)
            next_shape = next_shape.render("Next shape:", 1, (200,) * 3)
            self.screen.blit(next_shape, (self.display_width+10, 10))

            # top players panel
            top = pygame.font.SysFont("monospace", 20)
            top = top.render("Top 10:", 1, (200,) * 3)
            self.screen.blit(top, (self.display_width + 5, 140))
            for i, player in enumerate(self.top_players.keys()):
                multiplier = 20 * i
                player_name = self.top_players.get(player)[0]
                player_score = self.top_players.get(player)[1]

                board = pygame.font.SysFont("monospace", 14)
                board = board.render("%d.%s - %s" % (i + 1, player_name, player_score), 1, (200,) * 3)
                self.screen.blit(board, (self.display_width + 5, 180 + multiplier))

            # the score text
            pygame.draw.rect(self.screen, (25,) * 3, (
                0, self.display_height,
                self.display_width, self.window_height - self.display_width))

            score = pygame.font.SysFont("monospace", 18)
            score = score.render("Score: %d" % self.score, 1, (200,) * 3)
            self.screen.blit(score, (10, self.display_height))

            if GRID_ENABLED is True:
                self.grid()

            # if no shape, make one
            if shape_current is None:
                self.blocks.new()
                shape_current = self.blocks.get_shape()

            elif not self.blocks.full():

                if time.time() - move_time > 0.025:
                    self.blocks.move(direction)

                # make the blocks fall after a fraction of a second
                if time.time() - start_time > self.game_speed:
                    self.blocks.move(self.blocks.MOVE_DOWN)
                    start_time = time.time()

                # render the block shape to the screen
                for shape, colour in self.blocks.get_shape():
                    # convert the grid coordinates to pixel location
                    shape_x, shape_y = self.pixel(*shape)

                    pygame.draw.rect(self.screen, (100,) * 3, (
                        shape_x, shape_y,
                        self.grid_real_x, self.grid_real_y), 3)

                    pygame.draw.rect(self.screen, colour, (
                        shape_x, shape_y,
                        self.grid_real_x, self.grid_real_y))

            else:
                self.over = True

            # display the next shape on the panel
            self.next_shape_panel()

            # render the block collection
            the_blocks = [shape for shape in self.blocks.display()]

            if len(the_blocks) > 0:
                for shape, colour in the_blocks:
                    block_x, block_y = self.pixel(*shape)
                    pygame.draw.rect(self.screen, (100,) * 3, (
                        block_x, block_y,
                        self.grid_real_x, self.grid_real_y), 3)

                    pygame.draw.rect(self.screen, colour, (
                        block_x, block_y,
                        self.grid_real_x, self.grid_real_y))

            # if the bottom line is full, add score
            if self.blocks.line():
                self.score += 1

            if self.over:
                self.game_over()

            # update screen
            pygame.display.flip()

    def next_shape_panel(self):
        """
        Displays the next shape on screen.
        """
        for (x, y), colour in self.blocks.get_shape_next():
            x, y = x - 3, y

            pygame.draw.rect(self.screen, colour, (
                self.display_width + 12 + (25 * x), 35 + (25 * y), 25, 25
            ))

            pygame.draw.rect(self.screen, (25,) * 3, (
                self.display_width + 12 + (25 * x), 35 + (25 * y), 25, 25
            ), 1)

    def grid(self):
        """
        Displays the grid on the playable area.
        :return:
        """
        for column in range(self.grid_x):
            for row in range(self.grid_y):
                pygame.draw.rect(self.screen, (10,) * 3, (
                    self.grid_real_x * column, self.grid_real_y * row,
                    self.grid_real_x, self.grid_real_y), 1)

    def game_over(self):
        """
        Game Over Title.
        :return:
        """
        game_over = pygame.font.SysFont("monospace", 32)
        game_over = game_over.render("Game Over!", 1, (0,) * 3)
        self.screen.blit(game_over, ((self.display_width / 2) - 32, self.display_height / 2))

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