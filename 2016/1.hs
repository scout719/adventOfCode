import           Debug.Trace

loadInput = readFile "./1.in"

wordsWhen p s = case dropWhile p s of
  "" -> []
  s' -> w : wordsWhen p s'' where (w, s'') = break p s'

--Right
--0, -1 -> 1, 0 -> 0, 1 -> -1, 0
--x = y * -1
--y = x

--Left
--0, -1 -> -1, 0 -> 0, 1 -> 1, 0
--x = y
--y = x * -1

new_dir d (dx, dy) = if d == 'R' then (dy * (-1), dx) else (dy, dx * (-1))
move (x, y) (dx, dy) steps = (x + dx * steps, y + dy * steps)

solve [] (x, y) (dx, dy) = (x, y)
solve ((d : steps) : ls) (x, y) (dx, dy) =
  let new_d   = new_dir d (dx, dy)
      new_pos = move (x, y) new_d (read steps)
  in  solve ls new_pos new_d

result (x, y) = (abs x) + (abs y)

twice (x, y) [] = False
twice (x1, y1) ((x2, y2) : ps) =
  if ((x1 == x2) && (y1 == y2)) then True else twice (x1, y1) ps

move2 (x, y) (dx, dy) 0 visited = ((x, y), visited)
move2 (x, y) (dx, dy) steps visited =
  if ((steps == 0) || (twice (x, y) visited))
    then ((x, y), visited)
    else (move2 (x + dx, y + dy) (dx, dy) (steps - 1) ((x, y) : visited))

solve2 [] (x, y) (dx, dy) visited = (x, y)
solve2 ((d : steps) : ls) (x, y) (dx, dy) visited =
  let new_d                  = new_dir d (dx, dy)
      (new_pos, new_visited) = (move2 (x, y) new_d (read steps) visited)
  in  solve2 ls new_pos new_d new_visited

main = do
  contents <- loadInput
  let x : xs = (lines contents)
  let l      = wordsWhen (== ',') x
  let pos    = solve l (0, 0) (0, -1)
  print ("Part 1 " ++ (show (result pos)))
  let pos2 = solve2 l (0, 0) (0, -1) []
  print ("Part 2 " ++ (show (result pos2)))
