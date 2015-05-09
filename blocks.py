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
        self._shape_static = None
        self._rotation_static = None
        self._shape_current = None
        self._shape_next = None
        self._rotation = 0

        self._red = None
        self._green = None
        self._blue = None

        # shape position
        self._x = start_x
        self._y = start_y
        self._x_pos = 0
        self._y_pos = 0

        self._full = False

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
        :param rotation: optional int available for shape
        :return:
        """
        self._shape = []

        if self._shape_current is None:
            self._red = random.randint(0, 255)
            self._green = random.randint(0, 255)
            self._blue = random.randint(0, 255)

        # check if any static shapes are in place
        if self._shape_next is True:
            self._shape_current = self._shape_static
            self._shape_next = False
            self._shape_static = random.choice(self._shapes.keys())
        elif shape is not None and shape in self._shapes.keys():
            self._shape_current = shape
        else:
            self._shape_current = random.choice(self._shapes.keys())
            self._shape_static = random.choice(self._shapes.keys())

        if rotation is not None:
            self._rotation = rotation
        else:
            self._rotation = random.choice([i for i in range(0, len(self._shapes.get(self._shape_current)))])

        # apply shape to the self._shape list with current rotation
        shape = self._shapes.get(self._shape_current)[self._rotation]
        for x, y in shape:
            x, y = x + self._x_pos, y + self._y_pos
            self._shape.append(((x, y), self.get_colour()))

        out_of_bounds = len([(x, y) for (x, y), _ in self._shape if x > self._grid_x-1])
        if out_of_bounds > 0:
            self._x_pos -= out_of_bounds

    def get_colour(self):
        """
        Returns the colour of the current shape.
        :return: RGB
        """
        return self._red, self._green, self._blue

    def get_shape(self):
        """
        Returns the shape in the form of a list for printing/rendering.
        :return: list of tuples
        """
        return self._shape

    def get_shape_next(self):
        """
        Returns the next shape in the queue.
        For the panel only.
        :return:
        """
        # apply shape to the self._shape list with current rotation
        for x, y in self._shapes.get(self._shape_static)[0]:
            yield ((x, y), (200, ) * 3)

    def move(self, direction):
        """
        Move the blocks in a specific direction.
        :param direction: string representing direction
        :return: change current shape position to a new one
        """

        left = True
        right = True
        top_y = self._grid_x

        for (current_x, current_y), _ in self._shape:

            if current_y < top_y:
                top_y = current_y

            # collision with play field
            if current_x - 1 < 0:
                left = False
            if current_x > self._grid_x - 2:
                right = False
            if current_y == self._grid_y - 1:
                self.record()

            # collision with other blocks
            if len(self._record) > 0:
                for (block_x, block_y), _ in self._record:

                    if top_y < 1 and current_y + 1 == block_y and current_x + 1 == block_x:
                        self._full = True
                        self.record()
                        break

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
        self.new(self._shape_current, self._rotation)

    def rotate(self):
        """
        Rotate the shape, select next available
        :return: change current shape rotation to a new one
        """

        # check if the next rotation is available, if not revert to original shape
        if self._rotation != len(self._shapes[self._shape_current]) - 1:
            self._rotation += 1
        else:
            self._rotation = 0

        # make the new shape
        self.new(self._shape_current, self._rotation)

    def record(self):
        """
        Record the previous shapes from their last position.
        :return:
        """
        self._shape_next = True
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
        self._shape_current = None
        self._rotation = 0

        self._x_pos = 0
        self._y_pos = 0

        self._red = None
        self._green = None
        self._blue = None

    def reset(self):
        """
        Reset the game.
        :return:
        """

        self._shape = []
        self._shape_static = None
        self._rotation_static = None
        self._shape_current = None
        self._shape_next = None
        self._rotation = 0

        self._red = None
        self._green = None
        self._blue = None

        self._x_pos = 0
        self._y_pos = 0

        self._full = False

        self._record = []

    def line(self):
        """
        Full line checker.
        :return: boolean
        """

        for grid_y in range(self._grid_y):
            line = [((x, y), colour) for (x, y), colour in self.display() if y is grid_y]

            if len(line) == self._grid_x:
                for shape in line:
                    self._record.remove(shape)

                for i, ((_, y), _) in enumerate(self._record):
                    if y < grid_y:
                        self._record[i] = (self._record[i][0][0], self._record[i][0][1] + 1), self._record[i][1]

                return True

    def full(self):
        """
        Returns whether the play field is full.
        :return: boolean
        """

        return self._full
