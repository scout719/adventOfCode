from os import path
from datetime import datetime
import sys
import requests

year = str(datetime.now().year)
day = str(datetime.now().day)

if len(sys.argv) > 1:
    day = int(sys.argv[1])
url = f"https://adventofcode.com/{year}/day/{day}/input"
session = open("session").readline()
data = requests.get(url, cookies={
    "session": session
})
with open(path.join(year, "input", f"day{day}"), mode="w+") as f:
    f.write(data.text)
