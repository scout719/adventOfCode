max_ [] = (0, 'a')
max_ ((count, char):[]) = (count, char)
max_ ((count, char):cs) =
    let (max_count, max_c) = max_ cs
    in if max_count > count then (max_count, max_c)
    else (count, char)

min_ [] = (0, 'a')
min_ ((count, char):[]) = (count, char)
min_ ((count, char):cs) =
    let (max_count, max_c) = min_ cs
    in if max_count < count then (max_count, max_c)
    else (count, char)

value :: (Int, Char) -> Char
value (count, c) = c

updateFrequencyMap [] c = [(1, c)]
updateFrequencyMap ((count, x) : xs) c =
  if c == x then (count + 1, x) : xs else (count, x) : (updateFrequencyMap xs c)

countOccurrences :: String -> [(Int, Char)] -> [(Int, Char)]
countOccurrences [] freq_map = freq_map
countOccurrences (x : xs) freq_map =
  countOccurrences xs (updateFrequencyMap freq_map x)

solve1 :: [String] -> [[(Int, Char)]]-> [[(Int, Char)]]
solve1 [] freqMap = freqMap
solve1 (m:ms) freqMap = 
    let rest_freqMap = solve1 ms freqMap
        (a:b:c:d:e:f:g:h:_) = m
        (a_m:b_m:c_m:d_m:e_m:f_m:g_m:h_m:_) = rest_freqMap
        a_m2 = updateFrequencyMap a_m a
        b_m2 = updateFrequencyMap b_m b
        c_m2 = updateFrequencyMap c_m c
        d_m2 = updateFrequencyMap d_m d
        e_m2 = updateFrequencyMap e_m e
        f_m2 = updateFrequencyMap f_m f
        g_m2 = updateFrequencyMap g_m g
        h_m2 = updateFrequencyMap h_m h
    in [a_m2,b_m2,c_m2,d_m2,e_m2,f_m2,g_m2,h_m2]

trim (x:[]) = []
trim (x:xs) = x:(trim xs)

loadInput = readFile "./6.in"

main = do
  contents <- loadInput
  let messages1 = lines contents
  let messages = map trim messages1
  let freqMap = solve1 messages [[],[],[],[],[],[],[],[]]
  putStrLn ("Part 1: " ++ (map (value . max_) freqMap))
  putStrLn ("Part 2: " ++ (map (value . min_) freqMap))
