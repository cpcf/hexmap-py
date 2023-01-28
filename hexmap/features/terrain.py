from dataclasses import dataclass
from hexmap.cli.colors import Colors


@dataclass()
class Terrain:
    name: str
    possible_neighbours: list[str]
    colour_code: str

    def __len__(self):
        return len(self.name)

    def __repr__(self):
        return f"Terrain: {self.name}"

    def __str__(self):
        return self.colour_code + self.name + Colors.END
        # return self.name

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.name == other.name
            and self.possible_neighbours == other.possible_neighbours
        )


default_terrain = {
    "plains": Terrain("plains", ["plains", "mountains", "water", "valley", "town"], Colors.GREEN),
    "mountains": Terrain("mountains", ["plains", "mountains"], Colors.LIGHT_WHITE),
    "valley": Terrain("valley", ["plains", "valley"], Colors.BROWN),
    "water": Terrain("water", ["plains", "water"], Colors.LIGHT_BLUE),
    "town": Terrain("town", ["plains"], Colors.PURPLE),
}


def get_default_terrain():
    """
    Gets a list of the default Terrain types
    :return: List of the default Terrain types
    :rtype: list[Terrain]
    """
    terrains = []
    for terrain in list(default_terrain.values()):
        terrains.append(terrain)
    return terrains


def valid_neighbour(possible_neighbours, neighbours_options):
    """
    Checks if the terrain is possible based on what the neighbours' options are
    :param possible_neighbours: Possible neighbours for this terrain
    :type possible_neighbours: list[Terrain]
    :param neighbours_options: What terrain the neighbour could be
    :type neighbours_options: list[Terrain]
    :return: True if this terrain can exist next to this neighbour
    """
    neighbours_options = [option.name for option in neighbours_options]
    return len(set(possible_neighbours).intersection(neighbours_options)) > 0
