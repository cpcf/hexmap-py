import random
from hexmap.cartographer.location import Location
from hexmap.math import hexgrid
from hexmap.math.hexgrid import Hex
from hexmap.features.terrain import Terrain


class Grid:
    def __init__(self, grid, height, width):
        self.grid = grid
        self.height = height
        self.width = width
        self.count = height * width

    def is_complete(self):
        """
        Checks if every position in the grid has terrain determined
        :return: True if all positions on grid have their terrain determined, else false
        """
        for location in list(self.grid.values()):
            if not location.determined:
                return False
        return True

    def __str__(self):
        i = 0
        out, positions, locations = ("",) * 3
        offset = -self.height//2 % 2 == 0
        for position, location in self.grid.items():
            locations += str(location)
            positions += position.axial_string(location.longest)
            i += 1
            if i % self.width == 0:
                leading_whitespace = f" {'':^{location.longest/2 + location.longest%2}}" if offset else ''
                out += f"{leading_whitespace}{locations}\n{leading_whitespace}{positions}\n"
                positions, locations = ("",) * 2
                offset = not offset
        return out


def create_rectangle_hexmap(height, width, terrain_options):
    """
    Creates a grid of Hex positions to Terrain objects with
    the possible terrains passed in by terrain_options
    Parameters
    ----------
    :param int height: The position to place the terrain
    :param int width: The map of Hex positions to Locations
    :param list[Terrain] terrain_options: The possible Terrain Types
    :return: Hex Positions to Locations
    :rtype: dict[Hex, Location]
    """
    # Dicts are ordered, so we can turn a list of positions into a dict of
    # position to location, and know that the order will be maintained for printing later
    return {position: Location(terrain_options) for position in hexgrid.build_rectangle_of_size(height, width)}


def get_neighbours(position, positions):
    """
    Get the valid neighbour positions of the specified position
    :param position: The position to get the neighbours for
    :param positions: The map of positions to get the neighbours from
    :return: The neighbours of the specified position
    :rtype: list[Hex]
    """
    return [neighbour for neighbour in hexgrid.hex_neighbors(position) if neighbour in positions]


def update_positions(positions_to_update, positions):
    """
    Updates the specified positions
    :param positions_to_update: The positions to be updated
    :param positions: The whole collection of positions
    :return:
    """
    for position in positions_to_update:
        update_terrain_options_for_position(position, positions)


def update_neighbours(position, positions):
    """
    Updates the locations of the position's neighbours
    :param position: Position to get neighbours of
    :param positions: Positions to get the neighbours from
    """
    update_positions(get_neighbours(position, positions), positions)


def set_terrain_for_location(position, positions, terrain_option, update=True):
    """
    Places terrain at specified position
    Won't place if the position is already determined
    If position is None then it will be determined randomly
    If terrain_option is None then it will be determined randomly from the position's options
    :param position: The position to place the terrain
    :type position: Hex or None
    :param dict[Hex, Location] positions: The map of Hex positions to Locations
    :param Terrain terrain_option: The Terrain Type to set
    :type terrain_option: Terrain or None
    :param boolean update: If true update all after setting terrain
    :return: True if the location had its terrain set, false otherwise
    :rtype: bool
    """
    if position is None:
        position = random.choice(get_undetermined_positions(positions))
    if position not in positions:
        return False
    location = positions[position]
    if location.determined:
        return False
    location.determine_terrain_options(terrain_option)
    if update:
        update_neighbours(position, positions)
    return True


def update_terrain_options_for_position(position, positions):
    """
    Updates the terrain options for the specified position, removes any options that the neighbours prevent
    If the position is updated, updates neighbours
    :param Hex position: The position to place the terrain
    :param dict[Hex, Location] positions: The map of Hex positions to Locations
    """
    changed = False
    location = positions[position]
    neighbours = get_neighbours(position, positions)
    for neighbour in neighbours:
        if location.update_terrain_options(positions[neighbour]):
            changed = True
    if changed:
        update_positions(neighbours, positions)


def get_undetermined_positions(positions):
    """
    Gets all positions that do not have determined terrain
    :param dict[Hex, Location] positions: The map of Hex positions to Locations
    :return: positions that do not have determined terrain
    :rtype: dict[Hex, Location]
    """
    return [position for position in positions if not positions[position].determined]


def get_random_position_for_terrain(terrain_option, positions):
    """
    Gets random position that could have the terrain option
    :param Terrain terrain_option: The terrain option to find a position for
    :param dict[Hex, Location] positions: The map of Hex positions to Locations
    :return: position that could be specified terrain
    :rtype: Hex
    """
    undetermined = get_undetermined_positions(positions)
    terrain_positions = [position for position in undetermined if terrain_option in positions[position].terrain_options]
    return random.choice(terrain_positions)


def set_terrain_in_random_valid_position(terrain_option, positions):
    """
    Places the specified terrain in a random valid position
    :param Terrain terrain_option: The Terrain Type to set
    :param dict[Hex, Location] positions: The map of Hex positions to Locations
    """
    set_terrain_for_location(get_random_position_for_terrain(terrain_option, positions), positions, terrain_option)


def place_terrain_hex_shape(terrain_option, positions, radius, center=None):
    """
    Places a hex shaped pattern of terrain, starting at the specified center
    If no center is specified then a position will be chosen randomly
    :param Terrain terrain_option: The Terrain Type to set
    :param dict[Hex, Location] positions: The map of Hex positions to Locations
    :param int radius: The radius of the hex pattern
    :param center: The center of the pattern
    :type center: Hex or None
    :return:
    """
    if not center:
        center = get_random_position_for_terrain(terrain_option, positions)
    for position in hexgrid.get_all_hexes_within_range(center, radius):
        set_terrain_for_location(position, positions, terrain_option, False)


def place_terrain_staggered_wall_shape(terrain_option, positions, steps,
                                       direction, spawn_chance, turn_chance, start=None):
    """
    Places terrain in a line.
    Has a chance to take a step perpendicularly and start a new line, each step reduces the chance.
    Has a chance to change direction when starting a new line.
    :param Terrain terrain_option: The Terrain Type to set
    :param dict[Hex, Location] positions: The map of Hex positions to Locations
    :param int steps: Steps to take for each line
    :param int direction: Direction to start wall
    :param float spawn_chance: Chance to step perpendicularly and start a new line (min 0, max 1)
    :param float turn_chance: Chance to turn one step on creation of new line (min 0, max 1)
    :param start: The position to place location
    :type start: Hex or None
    """
    # Choose position randomly if no position is given
    if start is None:
        current_position = get_random_position_for_terrain(terrain_option, positions)
    else:
        current_position = start

    # Set the terrain for this position
    if not set_terrain_for_location(current_position, positions, terrain_option):
        return

    # For each step:
    #   Take step in direction
    #   Set the current position terrain
    #   Check for spawning new line
    #       Reduce spawn chance
    #       Check for direction change
    #       Start new line
    for _ in range(steps):
        current_position = hexgrid.hex_neighbor(current_position, direction)
        if not set_terrain_for_location(current_position, positions, terrain_option):
            return
        if random.random() <= spawn_chance:
            spawn_chance = spawn_chance / 2
            if random.random() <= turn_chance:
                new_direction = (direction + 1 if random.random() < 0.5 else -1) % 6
            else:
                new_direction = direction
            new_start = hexgrid.hex_neighbor(current_position, (direction + random.choice([1, 2, 4, 5])) % 6)
            place_terrain_staggered_wall_shape(terrain_option, positions, steps, new_direction, spawn_chance,
                                               turn_chance, new_start)
