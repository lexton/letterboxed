
from typing import Any, Dict
import json

import requests


def nyt_lb_game_data_today() -> Dict[str, Any]:
    """
    Fetch Gamedata from NYT.
    
    This was the only directly copied code, it just works (today at least) - is fragile since we are just ripping it from page.

    # https://github.com/aliceyliang/letter-boxed-solver/blob/2c83828014c1b93b121635c867ffd668f7c61b52/main.py#L13
    
    """

    r = requests.get("https://www.nytimes.com/puzzles/letter-boxed")

    # identify gameData
    start = r.text.index("window.gameData")

    # find index of first '{' after gamedata
    left = start + r.text[start:].index("{")

    # find index of next stanza directly following '}'
    right = left + r.text[left:].index(",\"dictionary")

    # extract the metadata in json format and close the bloc
    return json.loads(r.text[left:right]+"}")
