import random


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
                    (self._x, self._y + 2), (self._x + 1, self._y + 2), (self._x + 1, self._y + 1),
                    (self._x + 1, self._y)),
                ((self._x, self._y), (self._x, self._y + 1), (self._x + 1, self._y + 1), (self._x + 2, self._y + 1)),
                ((self._x, self._y), (self._x + 1, self._y), (self._x, self._y + 2), (self._x, self._y + 1)),
                ((self._x, self._y), (self._x + 1, self._y), (self._x + 2, self._y), (self._x + 2, self._y + 1))
            ),
            'T': (
                ((self._x, self._y), (self._x + 1, self._y), (self._x + 1, self._y + 1), (self._x + 2, self._y)),
                (
                    (self._x, self._y + 1), (self._x + 1, self._y), (self._x + 1, self._y + 1),
                    (self._x + 1, self._y + 2)),
                (
                    (self._x, self._y + 1), (self._x + 1, self._y), (self._x + 1, self._y + 1),
                    (self._x + 2, self._y + 1)),
                ((self._x, self._y), (self._x, self._y + 1), (self._x + 1, self._y + 1), (self._x, self._y + 2))
            )
        }

    def new(self, shape=None, rotation=None):
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

        if rotation is not None:
            self._rotation = rotation
        else:
            self._rotation = random.choice([i for i in range(0, len(self._shapes.get(self._current_shape)))])

        # apply shape to the self._shape list with current rotation
        shape = self._shapes.get(self._current_shape)[self._rotation]
        for x, y in shape:
            x, y = x + self._x_pos, y + self._y_pos
            self._shape.append((x, y))

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

        left = True
        right = True
        for current_x, current_y in self._shape:

            # collision with play field
            if current_x - 1 < 0:
                left = False
            if current_x > self._grid_x - 2:
                right = False
            if current_y == self._grid_y - 1:
                self.record()

            # collision with other blocks
            if len(self._record) > 0:
                for block_x, block_y in self._record:
                    if current_x + 1 == block_x and current_y == block_y:
                        right = False
                    if current_x - 1 == block_x and current_y == block_y:
                        left = False
                    if current_y + 1 == block_y and current_x == block_x:
                        self.record()

        # check for direction and if it's in the inbound
        if direction is self.MOVE_DOWN:
            self._y_pos += 1

        if direction is self.MOVE_LEFT and left:
            self._x_pos -= 1

        if direction is self.MOVE_RIGHT and right:
            self._x_pos += 1

        # make the new shape
        self.new(self._current_shape, self._rotation)

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
        self.new(self._current_shape, self._rotation)

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

