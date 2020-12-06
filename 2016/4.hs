import           Debug.Trace
import           Data.Char
import           Data.List

loadInput = readFile "./4.in"

wordsWhen p s = case dropWhile p s of
  "" -> []
  s' -> w : wordsWhen p s'' where (w, s'') = break p s'

extractChecksum (x : xs) = if x == ']' then "" else x : (extractChecksum xs)

extractRoomInfo :: String -> (String, String, String)
extractRoomInfo []       = ("", "", "")
extractRoomInfo (x : xs) = if x == '['
  then ("", "", extractChecksum xs)
  else
    let (room, id, checksum) = extractRoomInfo xs
    in  if x == '-'
          then (x : room, id, checksum)
          else if isDigit x
            then (room, x : id, checksum)
            else (x : room, id, checksum)

updateFrequencyMap [] c = if c == '-' then [] else [(-1, c)]
updateFrequencyMap ((count, x) : xs) c =
  if c == x then (count - 1, x) : xs else (count, x) : (updateFrequencyMap xs c)

validateChecksum []       freq_map = True
validateChecksum (x : xs) []       = False
validateChecksum (x : xs) ((count, c) : fs) =
  if c == x then validateChecksum xs fs else False


solve1 :: [(String, String, String)] -> Int
solve1 [] = 0
solve1 ((x, id, checksum) : xs) =
  let freq_map = sort (countOccurrences x [])
      rest     = solve1 xs
  in  if validateChecksum checksum freq_map then (read id) + rest else rest

countOccurrences :: String -> [(Int, Char)] -> [(Int, Char)]
countOccurrences [] freq_map = freq_map
countOccurrences (x : xs) freq_map =
  countOccurrences xs (updateFrequencyMap freq_map x)

hasNorth [] = False
hasNorth ('n' : 'o' : 'r' : 't' : 'h' : xs) = True
hasNorth (x : xs) = hasNorth xs

decryptRoomName :: (String, String, String) -> String
decryptRoomName ([], id, __) = ""
decryptRoomName (x : xs, id, checksum) =
  let base_a  = ord 'a'
      base_z  = ord 'z'
      range   = base_z - base_a + 1
      base_x  = ord x
      start   = base_x - base_a
      rotated = mod (start + (read id)) range
      new_x   = if x == '-' then ' ' else chr (base_a + rotated)
  in  new_x : (decryptRoomName (xs, id, checksum))

solve2 ((room, id, checksum) : xs) =
  let phrase = decryptRoomName (room, id, checksum)
  in  if hasNorth phrase then id else solve2 xs

main = do
  contents <- loadInput
  let rooms      = lines contents
  let rooms_info = map extractRoomInfo rooms
  print ("Part 1 " ++ show (solve1 rooms_info))
  print ("Part 2 " ++ (solve2 rooms_info))
