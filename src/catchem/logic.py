import json
from fuzzywuzzy import fuzz, process
from catchem.consts import pokestats, colors, lib_path, gen_map, catchem_config
from tabulate import tabulate
from pprint import pprint


def catch_em_all(pokemon, config):
    """Get base stats, moves, and evolutions of a pokemon
    :param pokemon: The name of the pokemon
    :param config: The config holding the game version and other data
    """
    gen = config.get("gen")
    show_stats = not config.get("hide_stats")
    show_moves = not config.get("hide_moves")
    show_evos = not config.get("hide_evos")

    poke_choices = list(pokestats.keys())
    pokemon, score = fuzzy_search(pokemon, poke_choices)
    if score < 70:  # If the score is less than 70, the match is too weak
        print(f"Error: {pokemon.title()} not found")
        pokemon = input("Try again: ")
        catch_em_all(pokemon)
        return
    
    if all([not show_stats, not show_moves, not show_evos]):
        print(f"I guess you and {pokemon.title()} haven't reached 255 friendship yet? 🤔")
        print("If you didn't use '-hs', '-hm', and '-he' all at once, use catchem-how to update your global config")
        print(f"current global config: {catchem_config}")
        return


    stats = pokestats[pokemon]
    # Show Base Stats
    stats_table = make_stats_table(stats)
    print(stats_table)
    # Show Moves


def make_stats_table(stats):
    pokemon = stats["name"]
    dex_no = stats["dex_no"]
    poke_types = stats["types"]
    stat_names = zip(
        ["hp", "attack", "defense", "spatt", "spdef", "speed", "total"],
        ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed", "Total"],
    )
    stat_rows = []
    for stat_tag, stat_name in stat_names:
        stat_value = stats[stat_tag]
        if stat_tag == "total":
            rgb_info = _total_stat_code(stat_value)
            color_bar = rgb_text(*rgb_info)
            stat_rows.append([stat_name, stat_value, color_bar])
            continue
        color = _base_stat_code(stat_value)
        stat_bar = "|" * (stat_value // 2)
        color_bar = rgb_text(stat_bar, color)
        stat_rows.append([stat_name, stat_value, color_bar])
    type_header_string = " ".join(
        [rgb_text(f" {type_.title()} ", type_) for type_ in poke_types]
    )
    header = [f"No: {dex_no}", pokemon.title(), type_header_string]
    return tabulate(stat_rows, headers=header, tablefmt="mixed_grid")


## Catchem How Functions


def _update_catchem_config(game, hide_stats, hide_moves, hide_evos):
    config_file = lib_path / "config.json"
    game_choices = list(gen_map.keys())
    new_game, score = fuzzy_search(game, game_choices)
    if score < 70:
        print(f"Error: {game.title()} not found")
        game = input("Enter a valid Pokemon game: ")
        _update_catchem_config(game, hide_stats, hide_moves, hide_evos)
        return
    game_gen = gen_map[new_game]
    new_config = {
        "game": new_game,
        "gen": game_gen,
        "hide_stats": hide_stats,
        "hide_moves": hide_moves,
        "hide_evos": hide_evos,
    }
    print("New Config:")
    pprint(new_config)
    with config_file.open("w") as f:
        json.dump(new_config, f, indent=4)


## Utility Functions


def rgb_text(text, color, background=True):
    color_type = 48 if background else 38  # 48 for background, 38 for foreground
    r, g, b = colors.get(color)
    return f"\033[{color_type};2;{r};{g};{b}m{text}\033[0m"


def _base_stat_code(stat_val):
    if stat_val < 50:
        return "red"
    elif stat_val < 90:
        return "yellow"
    elif stat_val < 125:
        return "green"
    else:
        return "blue"


def _total_stat_code(stat_val) -> tuple[str, str]:
    if stat_val < 350:
        return " Bad ", "red"
    elif stat_val < 450:
        return " Mid ", "yellow"
    elif stat_val < 500:
        return " Good ", "green"
    elif stat_val < 600:
        return " Great ", "grass"
    else:
        return " Legend/Pseudo ", "blue"


def _is_regional(name_list):
    regions = ["alolan", "hisuian", "galarian", "paldean"]
    return any(region in name_list for region in regions)


def fuzzy_search(query, choices):
    return process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
