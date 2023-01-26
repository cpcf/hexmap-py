import math


class Hex:
    def __init__(self, q, r, s=None):
        if s is None:
            s = -q - r
        assert not (round(q + r + s) != 0), "q + r + s must be 0"
        self.q = q
        self.r = r
        self.s = s

    def __hash__(self):
        return hash((self.q, self.r))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.q == other.q
            and self.r == other.r
            and self.s == other.s
        )

    def __repr__(self):
        return f'Hex({self.q}, {self.r}, {self.s})'

    def __str__(self):
        return f'{self.q, self.r, self.s}'

    def axial_string(self, offset):
        """
        Gets a string with the q and r values in brackets, with an optional offset to the brackets
        :param int offset: The offset from the values to the brackets
        :return: Axial Formatted string, e.g. '( 0, 0 )'
        :rtype: str
        """
        return f"({f'{self.q}, {self.r}':^{offset}})"


def hex_add(a, b):
    """
    :param Hex a:
    :param Hex b:
    """
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)


def hex_subtract(a, b):
    """
    :param Hex a:
    :param Hex b:
    """
    return Hex(a.q - b.q, a.r - b.r, a.s - b.s)


def hex_scale(a, k):
    """
    :param Hex a:
    :param int k:
    """
    return Hex(a.q * k, a.r * k, a.s * k)


def hex_rotate_left(a):
    """
    :param Hex a:
    """
    return Hex(-a.s, -a.q, -a.r)


def hex_rotate_right(a):
    """
    :param Hex a:
    """
    return Hex(-a.r, -a.s, -a.q)


hex_directions = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1),
                  Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]

directions = {
    'NW': 2,
    'NE': 1,
    'E': 0,
    'SE': 5,
    'SW': 4,
    'W': 3
}


def hex_direction(direction):
    """
    Looks up direction in hex_directions list
    :param int direction:
    :return:
    """
    return hex_directions[direction]


def hex_neighbor(position, direction):
    """
    Gets the neighbour of the specified position in the specified direction
    :param Hex position: The position to get the neighbour of
    :param int direction: Direction to get the neighbour in
    :return: The neighbour of position in the specified direction
    :rtype: Hex
    """
    return hex_add(position, hex_direction(direction))


def hex_neighbors(position):
    """
    Gets all the neighbours of the specified position
    :param Hex position: The position to get the neighbours of
    :return: The neighbours of position
    :rtype: list[Hex]
    """
    neighbours = []
    for direction in hex_directions:
        neighbours.append(hex_add(position, direction))
    return neighbours


hex_diagonals = [Hex(2, -1), Hex(1, -2), Hex(-1, -1),
                 Hex(-2, 1), Hex(-1, 2), Hex(1, 1)]


diagonal_directions = {
    'N': 1,
    'NE': 0,
    'SE': 5,
    'S': 4,
    'SW': 3,
    'NW': 2
}


def hex_diagonal_neighbor(position, direction):
    """
    Gets the diagonal neighbour of the specified position in the specified direction
    :param Hex position: The position to get the neighbour of
    :param int direction: Direction to get the neighbour in
    :return: The diagonal neighbour of position in the specified direction
    :rtype: Hex
    """
    return hex_add(position, hex_diagonals[direction])


def hex_length(position):
    """
    :param position:
    :return: The distance as measured by a Hex
    """
    return (abs(position.q) + abs(position.r) + abs(position.s)) // 2


def hex_distance(a, b):
    """
    Gets the distance between two hexes
    :param Hex a:
    :param Hex b:
    :return: Distance between a and b
    :rtype: int
    """
    return hex_length(hex_subtract(a, b))


def hex_round(h):
    """
    Used to find the closest Hex
    :param Hex h:
    :return: Closest hex to h
    """
    qi = int(round(h.q))
    ri = int(round(h.r))
    si = int(round(h.s))
    q_diff = abs(qi - h.q)
    r_diff = abs(ri - h.r)
    s_diff = abs(si - h.s)
    if q_diff > r_diff and q_diff > s_diff:
        qi = -ri - si
    else:
        if r_diff > s_diff:
            ri = -qi - si
    return Hex(qi, ri)


def hex_lerp(a, b, t):
    """
    Lerp between two hexes
    :param Hex a:
    :param Hex b:
    :param float t:
    :return: Hex calculated from lerp
    :rtype: Hex
    """
    return Hex(a.q * (1.0 - t) + b.q * t,
               a.r * (1.0 - t) + b.r * t,
               a.s * (1.0 - t) + b.s * t)


def hex_linedraw(a, b):
    """
    Draw a line between two hexes
    :param Hex a:
    :param Hex b:
    :return: List of Hex in line between a and b
    :rtype: list[Hex]
    """
    steps = hex_distance(a, b)
    a_nudge = Hex(a.q + 1e-06, a.r + 1e-06, a.s - 2e-06)
    b_nudge = Hex(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
    results = []
    step = 1.0 / max(steps, 1)
    for i in range(0, steps + 1):
        results.append(hex_round(hex_lerp(a_nudge, b_nudge, step * i)))
    return results


def build_rectangle(top, bottom, left, right):
    """
    Build a rectangle of hexes
    :param int top: Top limit of the rectangle
    :param int bottom: Bottom limit of the rectangle
    :param int left: Left limit of the rectangle
    :param int right: Right limit of the rectangle
    :return: List of hexes in the specified rectangle
    :rtype: list[Hex]
    """
    rectangle = []
    for r in range(top, bottom + 1):
        r_offset = math.floor(r / 2.0)
        for q in range(left - r_offset, right - r_offset + 1):
            rectangle.append(Hex(q, r))
    return rectangle


def build_rectangle_of_size(height, width):
    """
    Build a rectangle of hexes of specified height and width
    :param int height: Height of the rectangle
    :param int width: Width of the rectangle
    :return: List of hexes in the specified rectangle
    :rtype: list[Hex]
    """
    # bottom = height // 2
    # top = -bottom - height % 2
    top = -height // 2
    bottom = height // 2
    left = -width // 2
    right = width // 2
    return build_rectangle(top + 1, bottom, left + 1, right)


def get_all_hexes_within_range(center, steps):
    """
    Gets all the hexes in the specified range of the specified center
    :param Hex center: The center of the range to search
    :param int steps: Steps to take from the center to find hexes
    :return: List of Hexs within range of center
    :rtype: list[Hex]
    """
    results = []
    for q in range(-steps, steps + 1):
        for r in range(max(-steps, -q - steps), min(steps + 1, -q + steps + 1)):
            results.append(hex_add(center, Hex(q, r)))
    return results
