from os import path
from datetime import datetime
import sys

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
import http.client as http_client
import logging
import requests

http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
year = str(datetime.now().year)
day = str(datetime.now().day)

if len(sys.argv) > 1:
    day = int(sys.argv[1])
url = f"https://adventofcode.com/{year}/day/{day}/input"
session = open("session").readline()
data = requests.get(url, cookies={
    "session": session
}, headers={
    "User-Agent":
    "https://github.com/scout719/adventOfCode/blob/master/get_input.py by scout719"
})
with open(path.join(year, "input", f"day{day}"), mode="w+") as f:
    f.write(data.text)
