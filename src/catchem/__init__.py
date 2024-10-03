import argparse
from catchem.logic import catch_em_all


def catchem() -> None:
    """Main function for the catchem command line tool
    Will display the base stats of a pokemon in a tabulated format with color
    """
    parser = argparse.ArgumentParser(description="Display the base stats of a Pokémon")
    parser.add_argument("pokemon", nargs='+', action=OneToThreeArgAction, help="The pokemon to display")
    parser.add_argument("-g", "--game", help="The game version to display the moves for", default=None)
    args = parser.parse_args()
    pokemon = ' '.join(args.pokemon).lower()
    catch_em_all(pokemon)



class OneToThreeArgAction(argparse.Action):
    """Custom action for argparse to handle 1-3 arguments"""
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) < 3:
            values += [''] * (3 - len(values))
        elif len(values) > 3:
            raise argparse.ArgumentError(self, "Woah there trainer! A pokemon's name can only be 1-3 words long.")
        setattr(namespace, self.dest, values)