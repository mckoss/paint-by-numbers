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
