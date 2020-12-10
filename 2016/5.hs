import           Debug.Trace
import           Data.Char
import           Data.List
import qualified Crypto.Hash.MD5 as MD5
import           Data.ByteString.Base16 (encode)
import           Data.ByteString.Char8 (pack, unpack)

-- |The 'hash' takes a string and returns the hexadecimal representation of its MD5 checksum
hash :: String -> String
hash = unpack . encode . MD5.hash . pack

valid (a:b:c:d:e:f:_) =
    a == '0' &&
    b == '0' &&
    c == '0' &&
    d == '0' &&
    e == '0'

getNext (a:b:c:d:e:f:g:hash) = f

generateHash input counter =
    let value = input ++ (show counter)
    in (hash value)

solve1 input counter password =
    if (length password) == 8 then
        password
    else 
        let hash1 = generateHash input counter
        in if valid hash1  then
            trace password
            (solve1 input (counter+1) (password ++ [getNext hash1]))
        else
            solve1 input (counter+1) password

fillPassword pos char password = 
    if (pos < 8) && (password !! pos) == '_' then
        let (x,_:ys) = splitAt pos password
        in x ++ char : ys
    else
        password

solve2 input counter password =
    let hash1 = generateHash input counter
    in if valid hash1  then
        let pos = digitToInt (hash1 !! 5)
            char = hash1 !! 6
            newPass = fillPassword pos char password
        in 
            if not (elem '_' newPass) then
                newPass
            else
                trace newPass (solve2 input (counter+1) newPass)
    else
        solve2 input (counter+1) password

main = do
  let input = "wtnhxymk"
  print ("Part 1 " ++ (solve1 input 0 ""))
  print ("Part 2 " ++ (solve2 input 0 "________"))
