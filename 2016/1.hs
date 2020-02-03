loadInput = readFile "./1.in"

main = do 
    contents <- loadInput
    let ls = lines contents
    parse ls

parse (ls:xs) = putStrLn ls