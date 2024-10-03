import argparse
import json
from catchem.logic import catch_em_all, _update_catchem_config, fuzzy_search
from catchem.consts import lib_path, catchem_config, gen_map


def catchem() -> None:
    """Main function for the catchem command line tool
    Will display the base stats of a pokemon in a tabulated format with color
    """
    parser_desc = (
        """Catch'em will show you everything you need to know about a Pokémon"""
    )
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument(
        "pokemon", nargs="+", action=OneToThreeArgAction, help="The pokemon to display"
    )
    parser.add_argument(
        "-g", "--game", nargs='+', help="The game version to display the moves for", default=None
    )
    parser.add_argument(
        "-hs", "--hide-stats", help="Hide the stats table", action="store_true"
    )
    parser.add_argument(
        "-hm", "--hide-moves", help="Hide the moves table", action="store_true"
    )
    parser.add_argument(
        "-he", "--hide-evos", help="Hide evolutions", action="store_true"
    )
    parser.add_argument(
        "-ss", "--show-stats", help="Show the stats table", action="store_true"
    )
    parser.add_argument(
        "-sm", "--show-moves", help="Show the moves table", action="store_true"
    )
    parser.add_argument(
        "-se", "--show-evos", help="Show evolutions", action="store_true"
    )
    args = parser.parse_args()
    pokemon = " ".join(args.pokemon).lower()
    config = _temp_update_config(args)
    catch_em_all(pokemon, config)


def catchem_how() -> None:
    "Update the catchem config file"
    parser = argparse.ArgumentParser(description="Update the catchem config file")
    parser.add_argument(
        "-g",
        "--game",
        nargs="+",
        help="The game version to display the moves for",
        default='scarlet',
    )
    parser.add_argument(
        "-hs", "--hide-stats", help="Hide the stats table", action="store_true"
    )
    parser.add_argument(
        "-hm", "--hide-moves", help="Hide the moves table", action="store_true"
    )
    parser.add_argument(
        "-he", "--hide-evos", help="Hide evolutions", action="store_true"
    )
    parser.add_argument(
        "-ss", "--show-stats", help="Show the stats table", action="store_true"
    )
    parser.add_argument(
        "-sm", "--show-moves", help="Show the moves table", action="store_true"
    )
    parser.add_argument(
        "-se", "--show-evos", help="Show evolutions", action="store_true"
    )

    args = parser.parse_args()
    if isinstance(args.game, list):
        args.game = "-".join(args.game).lower()
    if args.show_stats:
        if args.hide_stats:
            raise argparse.ArgumentError(
                argument=None,
                message="You can't show (--show-stats) and hide (--hide-stats) at the same time"
            )
        args.hide_stats = not args.show_stats
    if args.show_moves:
        if args.hide_moves:
            raise argparse.ArgumentError(
                argument=None,
                message="You can't show (--show-moves) and hide (--hide-moves) at the same time"
            )
        args.hide_moves = not args.show_moves
    if args.show_evos:
        if args.hide_evos:
            raise argparse.ArgumentError(
                argument=None,
                message="You can't show (--show-evos) and hide (--hide-evos) at the same time"
            )
        args.hide_evos = not args.show_evos
    _update_catchem_config(
        args.game, args.hide_stats, args.hide_moves, args.hide_evos
    )


def _temp_update_config(args):
    temp_config = catchem_config.copy()
    if args.game is not None:
        if isinstance(args.game, list):
            args.game = "-".join(args.game).lower()
        game, score = fuzzy_search(args.game, list(gen_map.keys()))
        if score < 70:
            print("Error: Game could not be found")
            return
        
        game_gen = gen_map[game]
        temp_config["game"] = game
        temp_config["gen"] = game_gen
    else:
        game = temp_config["game"]
    print(f"Showing data for Pokémon {game.title()}")
    if args.hide_stats:
        temp_config["hide_stats"] = True
    if args.show_stats:
        temp_config["hide_stats"] = False
    if args.hide_moves:
        temp_config["hide_moves"] = True
    if args.show_moves:
        temp_config["hide_moves"] = False
    if args.hide_evos:
        temp_config["hide_evos"] = True
    if args.show_evos:
        temp_config["hide_evos"] = False
    return temp_config

class OneToThreeArgAction(argparse.Action):
    """Custom action for argparse to handle 1-3 arguments"""

    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) < 3:
            values += [""] * (3 - len(values))
        elif len(values) > 3:
            raise argparse.ArgumentError(
                self, "Woah there trainer! A pokemon's name can only be 1-3 words long."
            )
        setattr(namespace, self.dest, values)
