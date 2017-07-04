#!/usr/bin/env python3

"""The main module that brings everything together."""

from database import Database
from filters import Filter
import filters
import random
import scripter
import sys
import time
import argparse


def print_list(list_of_items):
    """Print all the items in a list. Used for printing each Pokemon from a
    particular region."""
    print("\n".join(str(item) for item in list_of_items))


def print_columns(items):
    """Print a list as multiple columns instead of just one."""
    rows = []
    items_per_column = int(len(items) / 4) + 1
    for index, pokemon in enumerate(items):
        if not pokemon.is_extra():
            name = pokemon.get_id() + " " + str(pokemon.get_name()).title()
        else:
            name = "--- " + pokemon.get_name()
        name = name.ljust(20)
        if len(rows) < items_per_column:
            rows.append(name)
        else:
            rows[index % items_per_column] += name
    print_list(rows)


def slideshow(db, start, end, seconds="0.25", rand=False):
    delay = 0.25
    if seconds is not None:
        delay = float(seconds)

    # Show each Pokemon, one by one.
    r = list(range(start, end))
    if rand:
        random.shuffle(r)
    try:
        for x in r:
            pokemon = db.get_pokemon(x)
            scripter.change_terminal(pokemon.get_path())
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Program was terminated.")
        sys.exit()


def main(argv):
    """Entrance to the program."""
    parser = argparse.ArgumentParser(
        description='Set a pokemon to the current terminal background or '
                    'wallpaper',
        epilog='Not setting any filters will get a completly random pokemon'
    )
    filtersGroup = parser.add_argument_group(
        'Filters', 'Arguments used to filter the list of pokemons with '
                   'various conditions'
    )
    filtersGroup.add_argument(
        '-n', '--name', help='Filter by pokemon which '
        'name contains NAME', action=filters.NameFilter)
    filtersGroup.add_argument(
        '-reg', '--region', help='Filter the pokemons by region',
        action=filters.RegionFilter, choices=Database.REGIONS
    )
    filtersGroup.add_argument(
        '-l', '--light', help='Filter out the pokemons darker then 0.xx',
        default=0.7, const=0.7, metavar='0.xx', nargs='?', type=float,
        action=filters.LightFilter
    )
    filtersGroup.add_argument(
        '-d', '--dark', help='Filter out the pokemons lighter then 0.xx',
        default=0.37, const=0.37, metavar='0.xx', nargs='?', type=float,
        action=filters.DarkFilter
    )
    filtersGroup.add_argument(
        '-t', '--type', help='Filter the pokemons by type.',
        action=filters.TypeFilter, choices=Database.POKEMON_TYPES
    )
    filtersGroup.add_argument(
        '-e', '--no-extras', help='Excludes extra pokemons',
        nargs=0, action=filters.ExtrasFilter
    )

    miscGroup = parser.add_argument_group("Misc")
    miscGroup.add_argument(
        '-w', '--wallpaper',
        help='Changes the desktop wallpapper instead of the terminal '
             'background',
        action='store_true'
    )
    miscGroup.add_argument(
        '-v', '--verbose', help='Enables verbose output',
        action='store_true'
    )
    options = parser.parse_args()
    size = len(Filter.POKEMON_LIST)

    if size == 0:
        print("No pokemon matches the specified filters")
        return

    target = random.choice(Filter.POKEMON_LIST)

    if options.verbose:
        if size == 1:
            print('The only one mathing these filters is: ')
        if size > Database.MAX_ID:
            print('Choosing between all of the pokemons...')
        else:
            # Print the list of filtered pokemon
            [print("#%s - %s" % (pkmn.get_id(), pkmn.get_name().title()))
                for pkmn in Filter.POKEMON_LIST]
        print("Total of %d pokemon matched the filters. Chose %s" %
              (size, target.get_name().title()))

    if options.wallpaper:
        scripter.change_wallpaper(target.get_path())
    else:
        scripter.change_terminal(target.get_path())


if __name__ == "__main__":
    # Entrance to the program.
    main(sys.argv)
