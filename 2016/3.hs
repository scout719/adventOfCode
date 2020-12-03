import Debug.Trace

loadInput = readFile "./3.in"

wordsWhen p s =  case dropWhile p s of
                      "" -> []
                      s' -> w : wordsWhen p s''
                            where (w, s'') = break p s'

trim [] = []
trim (c:cs) = 
    if c == ' ' || c == '\r' then
        trim cs
    else
        c:cs

parseFirst [] = ([], [])
parseFirst (c:cs) = 
    if c == ' ' || c == '\r' then
        ([], trim cs)
    else
        let (t, rest) = parseFirst cs
        in (c:t, rest)

parseTriangle [] = []
parseTriangle s = 
    let (t, rest) = parseFirst s
    in (read t):(parseTriangle rest)

extractInfo :: [String] -> [[Int]]
extractInfo [] = []
extractInfo (t:ts) = (parseTriangle (trim t)):(extractInfo ts)

extractFromGrid ((a1:a2:a3:[]):(b1:b2:b3:[]):(c1:c2:c3:[]):[]) = 
    [[a1,b1,c1],
    [a2,b2,c2],
    [a3,b3,c3]]

convert2 :: [[Int]] -> [[Int]]
convert2 [] = []
convert2 (a:b:c:ts) = 
    (extractFromGrid (a:b:c:[])) ++ (convert2 ts)

impossible (a:b:c:[]) =
    (a+b > c) && (b+c > a) && (c+a > b)

solve [] = 0
solve (t:ts) = 
    if impossible t then
        1 + (solve ts)
    else
        solve ts

main = do 
    contents <- loadInput
    let triangles = lines contents
    let ts = extractInfo triangles
    print ("Part 1 " ++ show (solve ts))
    print ("Part 2 " ++ show (solve (convert2 ts)))