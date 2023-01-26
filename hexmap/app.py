import argparse
import random
from mapgenerator.cartographer import builder
from mapgenerator.math import hexgrid
from mapgenerator.features import terrain

VERSION = '0.0.1'


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Build a map for a TTRPG"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version {VERSION}"
    )
    # parser.add_argument(
    #     'config',
    #     help='JSON format config defining map elements')
    return parser


def place_lake_in_random_position(positions, steps):
    builder.place_terrain_hex_shape_randomly(terrain.default_terrain["water"],
                                             positions,
                                             steps)


def place_town_in_random_position(positions):
    builder.place_terrain_in_random_valid_position(terrain.default_terrain["town"], positions)


def complete_map(positions, grid):
    while not grid.is_complete():
        builder.set_terrain_for_tile(None, positions, None)


def run():
    # args = init_argparse().parse_args()

    seed = None
    if seed:
        random.seed(seed)
    height = 23
    width = 17
    town_count = 5
    lake_count = 2
    positions = builder.create_positions(height, width, terrain.get_default_terrain())
    grid = builder.Grid(positions, height, width)

    builder.place_terrain_staggered_wall_shape(terrain.default_terrain["mountains"], positions, 5,
                                               hexgrid.directions["NE"], 0.5, 1, None)

    for _ in range(0, town_count):
        place_town_in_random_position(positions)

    for _ in range(0, lake_count):
        place_lake_in_random_position(positions, 2)

    complete_map(positions, grid)
    print(grid)

