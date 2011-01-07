Paint by Numbers
==

This is a basic solver for "paint by numbers" type puzzles (also known as
Griddlers, Picross, [etc.](http://en.wikipedia.org/wiki/Nonogram)).

Puzzles are entered into YAML formatted file (see one of the examples here).

You'll need [PyYaml](http://pyyaml.org/wiki/PyYAML) installed:

    $ easy_install pyyaml

Usage
==

Usage: paint.py [-h | -t | -f <file>]

Options

-h      : help
-f <file>   : Solve Paint by Numbers in file
-t      : Run Unit tests
-d      : Print debug information during solve

Example
==
    $ ./paint.py -f 024.yaml

    Row  1: ...XXXX.............
    Row  2: ..XXXXXX............
    Row  3: ..X..X.X..XX...XX...
    Row  4: .XX.X.XX.XXXX.XXXX..
    Row  5: XX...XXX.X.XX.XXXX..
    Row  6: X..XXXXXXX.XXXX.XXX.
    Row  7: .XXX.XXXX...XX..XXXX
    Row  8: ....XXXX....XX...XXX
    Row  9: ...XXXXX.....X...XXX
    Row 10: ...XXXX...........XX
    Row 11: ..XXXXX...........XX
    Row 12: ..XXXX........X..XXX
    Row 13: ..XXX.....X..XX..X.X
    Row 14: ..XXXX....X.XX...X.X
    Row 15: ..XXXX...XXXXX..XX.X
    Row 16: ...X.XX.XXXXXXX.XX..
    Row 17: ...X.XXXXXX..XXXXX..
    Row 18: ......XXXXX..X.XX...
    Row 19: ......X.XX...X.XX...
    Row 20: ......X.XX...X.XX...
