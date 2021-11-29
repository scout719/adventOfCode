day=$(date +'%d')
year=$(date +'%Y')
session=$(cat session)
curl https://adventofcode.com/$year/day/$day/input --cookie "session=$session" > $year/input/day$day