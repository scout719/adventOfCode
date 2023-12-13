import json
import os
import time
from datetime import datetime, timedelta
import traceback
import requests
from win11toast import notify

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

def process_board(id_, last_check, year, session):
    res = requests.get(
        f"https://adventofcode.com/{year}/leaderboard/private/view/{id_}.json",
        cookies={"session": session}, timeout=None).text
    obj = json.loads(res)
    l = []
    for u_ in obj["members"]:
        u = obj["members"][u_]
        for d_ in u['completion_day_level']:
            d = u['completion_day_level'][d_]
            for s_ in d:
                s = d[s_]
                ts = datetime.fromtimestamp(int(s['get_star_ts']))
                msg = f"{ts.time()} [Day {d_} star {s_}] {u['name']}"
                l.append((ts, msg))

    for ts, msg in sorted(l):
        if not last_check or ts > last_check:
            print(msg)
            notify(f"AoC {year}", msg, icon=f"{FILE_DIR}\\AoC.png")

def main():
    year = datetime.now().year
    sleep = 20
    session = open("session", encoding="ascii").readline()
    last_check = datetime.now() - timedelta(hours=6)
    boards = [321349, 194943]
    while True:
        try:
            for id_ in boards:
                process_board(id_, last_check, year, session)
            last_check = datetime.now()
        except Exception:  # pylint: disable=broad-exception-caught
            traceback.print_exc()
        time.sleep(sleep)


if __name__ == "__main__":
    main()
