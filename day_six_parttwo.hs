--Advent of Code Day 6 https://adventofcode.com/2018/day/6

import System.IO
import Data.Char
import qualified Data.Set as Set
import Data.List.Split
import Data.List
import qualified Data.Text as T
import Data.Char (isSpace)

--This is baby's first haskell program...please be gentle...
trim :: String -> String
trim = f . f
   where f = reverse . dropWhile isSpace

assignVals coords = 
    do
        let nameDesignations = [ (show x) ++ "X" | x <- [0..(length coords)-1]]
        nameDesignations
                
qsort :: Ord a => [a] -> [a]
qsort [] = []
qsort (p:xs) = (qsort lesser) ++ [p] ++ (qsort greater)
    where
        lesser = filter(<p) xs
        greater = filter(>=p) xs

        
hasDupes :: (Ord a) => [a] -> Bool
hasDupes l = length l /= length set
        where set = Set.fromList l

lowerString str = [ toLower loweredString | loweredString <- str]

rowMaker n y  = [ ((x, y), -1) |  x <- [0..n]]
arrayMaker m n = [ (rowMaker n y) | y <- [0..m]]

gridMaker m n = [((x, y), -1) | x <- [0..n], y <- [0..m]]

manhatDist (p1, p2) (q1, q2) =
    abs(p1 - q1) + abs(p2 - q2)

detMinClose c_coord points = 
   --don't forget your dos!!
   do
       let sortl = qsort [ ( (manhatDist c_coord (fst this_coord)), (snd this_coord))| this_coord <- points]
       let min_of_sortl = minimum sortl
       let min_val = if (fst min_of_sortl) /= 0 then ((fst min_of_sortl), lowerString (snd min_of_sortl)) else min_of_sortl
       let min_val_num = fst min_val
       let tot_dists = detUniqueDists sortl

       if (length(filter((==min_val_num).fst) sortl) == 1) then min_val else (-1, ".")
       --if not (hasDupes tot_dists) then min_val else (-1, ".")

getDists c_coord points = 
    do
        let sortl = qsort [ (manhatDist c_coord (fst this_coord)) | this_coord <- points]
        sum sortl

detUniqueDists l = 
    do
        let tot_dists = [(fst x) | x <- l]
        tot_dists

detClosest inp points =
    [(((fst(fst x)), (snd(fst x))), (detMinClose (fst x) points)) | x <- inp]

detDists inp points =
    [(((fst(fst x)), (snd(fst x))), (getDists (fst x) points)) | x <- inp]

getDisplayGrid grid =
    do
        [(snd (snd c)) | c <- grid]

genGridBorders m n = 
    do
        let partone = [(0, x) | x <- [0..n]]
        let parttwo = [(x, 0) | x <- [0..m]]
        let partthree = [(x, n) | x <- [0..m]]
        let partfour = [(m, x) | x <- [0..n]]

        partone ++ parttwo ++ partthree ++ partfour

detBorder coord borderCoords =
    elem coord borderCoords

shapeIsInf grid nameDesignations gridBorders = 
    do
        let borderSymbols = [((snd (snd item)), (detBorder (fst item) gridBorders)) | item <- grid]
        let trueOnly = filter ((==True).snd) borderSymbols
        let rDots = filter ((/=".").fst) trueOnly
        let sorted = qsort rDots
        let grouped = group sorted
        let fres = [fst (head item) | item <- grouped]
        let lowered = [lowerString item | item <- fres]
        let snd_grouped = group lowered
        let final = [head item | item <- snd_grouped]
        final

stripToString grid = 
    do
        let ret_grid = [lowerString( snd(snd item) )| item <- grid]
        let no_points = filter (/=".") ret_grid
        no_points

accumulateCounts grid symbols = 
    do
        let countlist = [filter (==c_symb) grid | c_symb <- symbols]

        let finalAggregate = [((head c_group), (length c_group)) | c_group <- countlist]
        finalAggregate


breakDownGrid grid =
    [snd item | item <- grid]

detLessThan l =
    do
        let filteredList = filter (<10000) l
        length filteredList

main = do 
    let m = 1000
    let n = 1000

    --Step 0: Parse the file!
    handle <- openFile ".\\inp\\day_six.txt" ReadMode
    contents <- hGetContents handle
    let linesOfFile = lines contents
    let coord_pairs = [(splitOn "," ln) | ln <- linesOfFile]
    let coords = [(read(trim (c !! 1)), read(c !! 0)) | c <- coord_pairs]

    --Step 1: Generate Name Designations for the coordinates
    let nameDesignations = assignVals coords
    let nameSeekerDesignations = [lowerString x | x <- nameDesignations]
    let points = zip coords nameDesignations

    --Step 2: Generate the grid!
    let grid = gridMaker m n
    let ngrid = detDists grid points
    let lenOnly = breakDownGrid ngrid
    print("Determining counts..")
    let lessThanCount = detLessThan lenOnly

    print(lessThanCount)
    hClose handle

    --print(concat (getDisplayGrid ngrid))
        