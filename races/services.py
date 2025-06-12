# races/services.py
import requests

LAST_RESULTS_URL = "https://api.jolpi.ca/ergast/f1/current/last/results.json"

def fetch_last_race_results():
    resp = requests.get(LAST_RESULTS_URL, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    races = data["MRData"]["RaceTable"]["Races"]
    if not races:
        return {"race": None, "results": []}

    race = races[0]
    return {
        "race": {
            "name": race["raceName"],
            "circuit": race["Circuit"]["circuitName"],
            "date": race["date"],
        },
        "results": race["Results"],
    }
