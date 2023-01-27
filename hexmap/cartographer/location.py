import random

from hexmap.features import terrain


class Location:
    def __init__(self, terrain_options):
        self.terrain_options = terrain_options
        self.longest = len(max(terrain_options, key=len))
        self.determined = len(self.terrain_options) == 1

    def __repr__(self):
        if self.determined:
            return f"({str(self.terrain_options[0]):^{self.longest}})"
        else:
            return f"({'?':^{self.longest}})"

    def __str__(self):
        if self.determined:
            return f"({str(self.terrain_options[0]):^{self.longest}})"
        else:
            return f"({'?':^{self.longest}})"

    def determin_terrain_options(self, terrain_option):
        """
        Sets the terrain_options to a single option
        If option specified is None, select the option from available options
        :param terrain_option: The terrain to set for this location
        :type terrain_option: Terrain or None
        :return:
        """
        if terrain_option is None and self.terrain_options:
            terrain_option = random.choice(self.terrain_options)
        self.terrain_options = [terrain_option]
        self.determined = True

    def set_terrain_options(self, terrain_options):
        """
        Set the terrain options for this Location
        :param list[Terrain] terrain_options: The Terrain Types to set for this Location
        """
        self.terrain_options = terrain_options
        self.determined = len(self.terrain_options) == 1

    def update_terrain_options(self, neighbour):
        """
        Update the possible terrain options based on the neighbour's options
        :param Location neighbour: The neighbour to compare to
        """
        # If it's already determined, don't update it
        if self.determined:
            return False
        old_options = self.terrain_options
        new_options = []
        for option in old_options:
            possible = option.possible_neighbours
            if terrain.valid_neighbour(possible, neighbour.terrain_options):
                new_options.append(option)
        self.set_terrain_options(new_options)
        self.determined = len(self.terrain_options) == 1
        return old_options != new_options
