Requires Python version > 3.6

# Hexmap-py

## Simple Hexmap generator for TTRPG style maps
Generates a simple hexmap and outputs it in plaintext.
By default colourises the tiles for terminal outout.

Can save and load map in a binary format.

Usage:
```
python3 -m hexmap
optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s SAVE, --save SAVE
  -l LOAD, --load LOAD
```

Example Output:
```
(  water  )(  water  )(  water  )(mountains)( plains  )( plains  )( valley  )( plains  )( plains  )(  water  )
( -2, -4  )( -1, -4  )(  0, -4  )(  1, -4  )(  2, -4  )(  3, -4  )(  4, -4  )(  5, -4  )(  6, -4  )(  7, -4  )
      (  water  )(  water  )(  water  )(mountains)(mountains)( plains  )( plains  )(  town   )( plains  )( plains  )
      ( -2, -3  )( -1, -3  )(  0, -3  )(  1, -3  )(  2, -3  )(  3, -3  )(  4, -3  )(  5, -3  )(  6, -3  )(  7, -3  )
(  water  )(  water  )(  water  )(  water  )(mountains)( plains  )(  town   )( plains  )( plains  )(  town   )
( -3, -2  )( -2, -2  )( -1, -2  )(  0, -2  )(  1, -2  )(  2, -2  )(  3, -2  )(  4, -2  )(  5, -2  )(  6, -2  )
      (  water  )(  water  )(  water  )(  water  )(mountains)( plains  )( plains  )( plains  )( plains  )( plains  )
      ( -3, -1  )( -2, -1  )( -1, -1  )(  0, -1  )(  1, -1  )(  2, -1  )(  3, -1  )(  4, -1  )(  5, -1  )(  6, -1  )
(  water  )(  water  )(  water  )(  water  )(  water  )(mountains)( plains  )( plains  )( plains  )(  water  )
(  -4, 0  )(  -3, 0  )(  -2, 0  )(  -1, 0  )(  0, 0   )(  1, 0   )(  2, 0   )(  3, 0   )(  4, 0   )(  5, 0   )
      (  water  )(  water  )(  water  )(  water  )(mountains)(mountains)( plains  )(  town   )( plains  )( plains  )
      (  -4, 1  )(  -3, 1  )(  -2, 1  )(  -1, 1  )(  0, 1   )(  1, 1   )(  2, 1   )(  3, 1   )(  4, 1   )(  5, 1   )
(  water  )(  water  )(  water  )(  water  )(mountains)(mountains)(mountains)( plains  )( plains  )( plains  )
(  -5, 2  )(  -4, 2  )(  -3, 2  )(  -2, 2  )(  -1, 2  )(  0, 2   )(  1, 2   )(  2, 2   )(  3, 2   )(  4, 2   )
      ( plains  )( plains  )(mountains)(mountains)(mountains)( plains  )( plains  )(  town   )( plains  )(  town   )
      (  -5, 3  )(  -4, 3  )(  -3, 3  )(  -2, 3  )(  -1, 3  )(  0, 3   )(  1, 3   )(  2, 3   )(  3, 3   )(  4, 3   )
(mountains)( plains  )( plains  )(mountains)( plains  )( plains  )(  town   )( plains  )( plains  )( plains  )
(  -6, 4  )(  -5, 4  )(  -4, 4  )(  -3, 4  )(  -2, 4  )(  -1, 4  )(  0, 4   )(  1, 4   )(  2, 4   )(  3, 4   )
      ( plains  )( plains  )(mountains)(mountains)( plains  )( plains  )( plains  )(  water  )(  water  )( plains  )
      (  -6, 5  )(  -5, 5  )(  -4, 5  )(  -3, 5  )(  -2, 5  )(  -1, 5  )(  0, 5   )(  1, 5   )(  2, 5   )(  3, 5   )
```
