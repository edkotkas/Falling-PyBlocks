import pygame
import sys
import time
import webbrowser

import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

from blocks import Blocks

GRID_ENABLED = True


class Game:
    def __init__(self):
        """
        Falling PyBlocks, a clone of Tetris.
        :return:
        """
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        # sound file downloaded from (https://archive.org/details/TetrisThemeMusic)
        pygame.mixer.music.load('tetris.ogg')

        # grid divider
        self.grid_x = 10
        self.grid_y = 20

        # game speed
        self.game_speed = 0.5
        self.fps = 30

        # game status
        self.over = False

        # colours
        self.colour_clear = (25,) * 3
        self.colour_grid = (50,) * 3

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
        self.player_name = ""

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.blocks = Blocks(
            (self.grid_x, self.grid_y),
            (self.display_width, self.display_height),
            (4, 0)
        )

        self.top_players = []

    def loop(self):
        """
        Main game loop.
        :return: main game loop
        """
        shape_current = None
        direction = None
        start_time = time.time()
        move_time = 0
        paused = False
        music_on = True
        creator = None

        while True:

            if music_on is True:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()

            while paused is True:

                for event in pygame.event.get():

                    # exit if X is pressed
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:
                            sys.exit()

                        if event.key == pygame.K_p or event.key == pygame.K_r:
                            paused = False

            # fps
            pygame.time.Clock().tick(self.fps)

            # clear screen
            self.screen.fill(self.colour_clear)

            for event in pygame.event.get():

                # exit if window X is pressed
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                    # key presses listener
                    if event.key == pygame.K_SPACE or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.game_speed = 0.05
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        move_time = time.time()
                        direction = self.blocks.MOVE_RIGHT
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        move_time = time.time()
                        direction = self.blocks.MOVE_LEFT
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        # rotate the block shape clockwise
                        self.blocks.rotate()

                    if event.key == pygame.K_m:
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                            music_on = False
                        else:
                            pygame.mixer.music.play()
                            music_on = True

                    if event.key == pygame.K_r:
                        self.reset()
                        self.blocks.reset()

                    if event.key == pygame.K_p:
                        paused = True

                # if any key released set the game speed to normal
                if event.type == pygame.KEYUP:
                    self.game_speed = 0.5
                    direction = None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if creator.collidepoint(mouse_pos):
                        webbrowser.open("https://github.com/edkotkas")

            # play area background
            pygame.draw.rect(self.screen, (22,) * 3, (0, 0, self.display_width, self.display_height))

            # side panel background
            pygame.draw.rect(self.screen, (20,) * 3, (
                self.display_width, 0,
                self.window_width - self.display_width, self.window_height))

            # next shape panel
            self.screen.blit(self.make_text("Next Shape:", 16, font="arial"), (self.display_width + 5, 10))

            # top players panel
            self.screen.blit(self.make_text("Top 5:", 20, font="arial"), (self.display_width + 5, 180))
            for i, (score, player) in enumerate(self.top_players):
                multiplier = 20 * i
                count = i + 1

                self.screen.blit(self.make_text("%d.%s - %d" % (count, player, score)),
                                 (self.display_width + 10, 220 + multiplier))

            # controls texts
            self.screen.blit(self.make_text("Controls:", font="arial"), (self.display_width + 5, 335))
            self.screen.blit(self.make_text("Arrows - move", font="arial"), (self.display_width + 5, 355))
            self.screen.blit(self.make_text("M - music off/on", font="arial"), (self.display_width + 5, 375))
            self.screen.blit(self.make_text("R - reset", font="arial"), (self.display_width + 5, 395))
            self.screen.blit(self.make_text("P - pause", font="arial"), (self.display_width + 5, 415))

            # the score text
            pygame.draw.rect(self.screen, (20,) * 3, (
                0, self.display_height,
                self.display_width, self.window_height - self.display_width))

            creator = self.screen.blit(
                self.make_text("Falling PyBlocks by Eduard Kotkas (GitHub - @edkotkas)",
                               colour=(255,) * 3
                               ), (5, self.window_height - 18))

            self.screen.blit(self.make_text("SCORE: %d" % self.score, 18, font="arial"), (self.display_width + 5, 140))

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

                    pygame.draw.rect(self.screen, colour, (
                        shape_x, shape_y,
                        self.grid_real_x, self.grid_real_y))

                    pygame.draw.rect(self.screen, (50,) * 3, (
                        shape_x, shape_y,
                        self.grid_real_x, self.grid_real_y), 3)

            else:
                if self.over is False:
                    self.get_player()
                self.over = True

            # display the next shape on the panel
            self.next_shape_panel()

            # render the block collection
            the_blocks = [shape for shape in self.blocks.display()]

            if len(the_blocks) > 0:
                for shape, colour in the_blocks:
                    block_x, block_y = self.pixel(*shape)

                    pygame.draw.rect(self.screen, colour, (
                        block_x, block_y,
                        self.grid_real_x, self.grid_real_y))

                    pygame.draw.rect(self.screen, (50,) * 3, (
                        block_x, block_y,
                        self.grid_real_x, self.grid_real_y), 3)

            # if the bottom line is full, add score
            if self.blocks.line():
                self.score += 1

            if self.over:
                self.screen.blit(self.make_text("GAME OVER", 32, (255,) * 3, font="arial"),
                                 ((self.display_width / 2) - 96, self.display_height / 2))

            if paused is True:
                self.screen.blit(self.make_text("PAUSED", 32, (255,) * 3, font="arial"),
                                 ((self.display_width / 2) - 64, self.display_height / 2))

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

            pygame.draw.rect(self.screen, (50,) * 3, (
                self.display_width + 12 + (25 * x), 35 + (25 * y), 25, 25
            ), 3)

    def grid(self):
        """
        Displays the grid on the playable area.
        :return:
        """
        for column in range(self.grid_x):
            for row in range(self.grid_y):
                pygame.draw.rect(self.screen, (21,) * 3, (
                    self.grid_real_x * column, self.grid_real_y * row,
                    self.grid_real_x, self.grid_real_y), 1)

    def pixel(self, x, y):
        """
        Converts grid coordinates to pixel coordinates.
        :param x: int between 0 and 10
        :param y: int between 0 and 20
        :return: converted coordinates
        """
        return x * (self.display_width / 10), y * (self.display_height / 20)

    def start_screen(self):
        """
        Display the startup screen.
        :return:
        """
        button = None
        creator = None
        player_name = None
        default = "Enter Your Name Here."
        self.player_name = default
        while True:

            # fps
            pygame.time.Clock().tick(self.fps)

            # clear screen
            self.screen.fill(self.colour_clear)

            for event in pygame.event.get():

                # exit if X is pressed
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    else:
                        if event.key == pygame.K_RETURN and self.player_name != default and self.player_name != "":
                            return False
                        if event.key == pygame.K_BACKSPACE and self.player_name != "" and event.key != pygame.K_RETURN:
                            self.player_name = self.player_name[:-1]
                        else:
                            self.player_name += str(event.unicode)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if player_name.collidepoint(mouse_pos):
                        if self.player_name == default:
                            self.player_name = ""

                    if button.collidepoint(mouse_pos) \
                            and self.player_name != "" and self.player_name != default:
                        return False

                    if creator.collidepoint(mouse_pos):
                        webbrowser.open("https://github.com/edkotkas")

            self.screen.blit(self.make_text("Falling PyBlocks", 32, (255,) * 3),
                             ((self.window_width / 2) - 150, self.window_height / 8))

            # play button, with rectangle
            self.screen.blit(self.make_text("PLAY", 32, (255, ) * 3),
                             ((self.window_width / 2) - 40, self.window_height / 2))
            button = pygame.draw.rect(self.screen, (255,) * 3, (
                (self.window_width / 2) - 50, self.window_height / 2, 95, 35
            ), 2)

            # player name
            self.screen.blit(self.make_text(self.player_name, 24, (100, ) * 3),
                             ((self.window_width / 2) - 150, self.window_height / 3))
            player_name = pygame.draw.rect(self.screen, (255,) * 3, (
                (self.window_width / 2) - 160, (self.window_height / 3) - 5, (self.window_width / 2) + 80, 35
            ), 2)

            creator = self.screen.blit(
                self.make_text("Falling PyBlocks by Eduard Kotkas (GitHub - @edkotkas)",
                               colour=(255,) * 3
                               ), (5, self.window_height - 18))

            pygame.display.flip()

    def reset(self):
        """
        Reset the game.
        :return:
        """
        self.over = False
        self.score = 0

    def make_text(self, string, size=14, colour=(200,)*3, font="monospace"):
        """
        Creates text for blit.
        :param string: text to be shown
        :param size: font size
        :param colour: font colour
        :param font: font family
        :return:
        """
        return pygame.font.SysFont(font, size).render(string, 1, colour)

    def get_player(self):
        """
        Gets the players name to be added to the top 5.
        :return:
        """
        self.top_players.append((self.score, self.player_name))

        if len(self.top_players) > 1:
            for i in range(len(self.top_players)-1):
                if self.top_players[i + 1][0] > self.top_players[i][0]:
                    self.top_players[i + 1], self.top_players[i] = self.top_players[i], self.top_players[i + 1]


if __name__ == "__main__":
    fpb = Game()
    fpb.start_screen()
    fpb.loop()