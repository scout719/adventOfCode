import           Debug.Trace
-- max_ [] = (0, 'a')
-- max_ ((count, char):[]) = (count, char)
-- max_ ((count, char):cs) =
--     let (max_count, max_c) = max_ cs
--     in if max_count > count then (max_count, max_c)
--     else (count, char)

-- min_ [] = (0, 'a')
-- min_ ((count, char):[]) = (count, char)
-- min_ ((count, char):cs) =
--     let (max_count, max_c) = min_ cs
--     in if max_count < count then (max_count, max_c)
--     else (count, char)

-- value :: (Int, Char) -> Char
-- value (count, c) = c

-- updateFrequencyMap [] c = [(1, c)]
-- updateFrequencyMap ((count, x) : xs) c =
--   if c == x then (count + 1, x) : xs else (count, x) : (updateFrequencyMap xs c)

-- countOccurrences :: String -> [(Int, Char)] -> [(Int, Char)]
-- countOccurrences [] freq_map = freq_map
-- countOccurrences (x : xs) freq_map =
--   countOccurrences xs (updateFrequencyMap freq_map x)

-- solve1 :: [String] -> [[(Int, Char)]]-> [[(Int, Char)]]
-- solve1 [] freqMap = freqMap
-- solve1 (m:ms) freqMap = 
--     let rest_freqMap = solve1 ms freqMap
--         (a:b:c:d:e:f:g:h:_) = m
--         (a_m:b_m:c_m:d_m:e_m:f_m:g_m:h_m:_) = rest_freqMap
--         a_m2 = updateFrequencyMap a_m a
--         b_m2 = updateFrequencyMap b_m b
--         c_m2 = updateFrequencyMap c_m c
--         d_m2 = updateFrequencyMap d_m d
--         e_m2 = updateFrequencyMap e_m e
--         f_m2 = updateFrequencyMap f_m f
--         g_m2 = updateFrequencyMap g_m g
--         h_m2 = updateFrequencyMap h_m h
--     in [a_m2,b_m2,c_m2,d_m2,e_m2,f_m2,g_m2,h_m2]

-- invalid (a:b:c:d:rest) outside = 

-- extractHypernet (x:xs) = 
  
-- extractLastPart (x:xs) = 
--   if x == "]" then 

-- extractParts (x:xs) =
--   if x == "[" then 

findCloseBracket [] _ =
  -1
findCloseBracket (x:xs) i = 
  if x == ']' then
    i
  else
    findCloseBracket xs (i+1)

skipAhead [] _ = []
skipAhead (x:xs) count = 
  if count == 0 then
    x:xs
  else
    skipAhead xs (count-1)

findIdx _ [] = 
  []
findIdx i (x:xs)= 
  if x == '[' then
    let close = findCloseBracket xs (i+1)
        rest = skipAhead xs (close-i)
    in
      (i, close):(findIdx (close+1) rest)
  else
    findIdx (i+1) xs

crop (x:xs) ri i = 
  if i == ri then
    []
  else
    x:(crop xs ri (i+1))

valid (a:b:c:[]) _ _ =
  False
valid (a:b:c:d:xs) [] i =
  let rest_valid = valid (b:c:d:xs) [] (i+1) in
    (a == d && b == c && a /= b) || rest_valid
valid (a:b:c:d:xs) ((le,ri):idxs) i =
  if i < le then
    let rest_valid = valid (b:c:d:xs) ((le,ri):idxs) (i+1) in 
      -- trace (show (i,(le,ri):idxs,a:b:c:d:[], (a == d && b == c && a /= b)))
      ((a == d && b == c && a /= b) || rest_valid)
  else if i == le then
    let rest = skipAhead (a:b:c:d:xs) (ri-le+1)
        rest_valid = valid rest idxs (ri+1) in
        -- trace (show ("CENAS: " ++ rest))
        rest_valid
  else
    trace "assert" False
    
valid2 (a:b:c:[]) _ _ =
  True
valid2 (a:b:c:d:xs) [] i =
  True
valid2 (a:b:c:d:xs) ((le,ri):idxs) i =
  if i < le then
    valid2 (b:c:d:xs) ((le,ri):idxs) (i+1)
  else if i == le then
    let rest = skipAhead (a:b:c:d:xs) (ri-le+1)
        rest_valid = valid2 rest idxs (ri+1) in
      -- trace (show (valid (crop (b:c:d:xs) ri (i+1)) [] (i+1),rest_valid, (crop (b:c:d:xs) ri (i+1))))
      (
      if valid (crop (b:c:d:xs) ri (i+1)) [] (i+1) then
        False
      else
        rest_valid
      )
  else
    trace "assert" False

gather [] =
  []
gather (x:xs) = 
  case gather xs of (rest:rests) -> if x =='[' then
                                      ([]:rest:rests)
                                    else if x == ']' then
                                      ([]:rest:rests)
                                    else
                                      ((x:rest):rests)
                    [] -> if x =='[' then
                            ([])
                          else if x == ']' then
                            ([])
                          else
                            ([[x]])
  
solve2 ((a:b:c:xs):rs) 


solve1 [] [] = []
solve1 (ip:ips) (idx:idxs) = 
  let rest = solve1 ips idxs
      is_valid = (valid ip idx 0) && (valid2 ip idx 0)
  in 
    -- trace (show (ip, is_valid))  
    (if is_valid then ip:rest
    else rest) 

trim (x:[]) = []
trim (x:xs) = x:(trim xs)
loadInput = readFile "./7.sample"
main = do
  contents <- loadInput
  let raw_ips = lines contents
  let ips = map trim raw_ips
  --let freqMap = solve1 messages [[],[],[],[],[],[],[],[]]
  -- putStrLn (show ips)
  let idxs = map (findIdx 0) ips
  let (ip:_) = ips
  let (idx:_) = idxs
  -- putStrLn ip
  -- putStrLn (show (solve1 [ip] [idx]))
  -- putStrLn (show (length (solve1 ips idxs)))
  putStrLn (show (gather ip))
  --putStrLn ("Part 1: " ++ (map (value . max_) freqMap))
  --putStrLn ("Part 2: " ++ (map (value . min_) freqMap))


