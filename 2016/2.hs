import           Debug.Trace

loadInput = readFile "./2.in"

wordsWhen p s = case dropWhile p s of
  "" -> []
  s' -> w : wordsWhen p s'' where (w, s'') = break p s'

config1 = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

config2 =
  [ ['0', '0', '1', '0', '0']
  , ['0', '2', '3', '4', '0']
  , ['5', '6', '7', '8', '9']
  , ['0', 'A', 'B', 'C', '0']
  , ['0', '0', 'D', '0', '0']
  ]

keyAt (x, y) config =
  if (x < 0) || (x >= (length config)) || (y < 0) || (y >= (length config))
    then '0'
    else (config !! y) !! x

allowed p config = (keyAt p config) /= '0'

move (x, y) d config =
  let new_p = if d == 'U'
        then (x, y - 1)
        else if d == 'L'
          then (x - 1, y)
          else if d == 'R'
            then (x + 1, y)
            else if d == 'D' then (x, y + 1) else (x, y)
  in  if (allowed new_p config) then new_p else (x, y)

followInstruction [] p config = p
followInstruction (i : is) p config =
  let new_p = move p i config in followInstruction is new_p config

solve [] p config = ""
solve (instruction : rest) p config =
  let new_p  = followInstruction instruction p config
      next_k = keyAt new_p config
  in  next_k : (solve rest new_p config)

main = do
  contents <- loadInput
  let instructions = lines contents
  --print instructions
  let s1           = solve instructions (1, 1) config1
  print ("Part 1 " ++ s1)
  let s2 = solve instructions (0, 2) config2
  print ("Part 2 " ++ s2)
