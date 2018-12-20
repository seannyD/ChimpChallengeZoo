# QHIMP Challenge

These are the results from a museum exhibit. [Living links](http://www.living-links.org/chimp-challenge-memory-test/), 
[some details on the experiment](http://www.replicatedtypo.com/the-qhimp-qhallenge-working-memory-in-humans-and-chimpanzees/4947.html).


## chimp-869990b

These are the original program files for running the game.

## results

### rounds.csv

This is the main data file that tracks all rounds played.  

-  latency: The amount of time the numerals are shown before being masked
-  numerals: The number of numerals shown
-  selected:  the order of buttons selected. Values represent the numeral that is displayed
-  correct:  the correct order of buttons (this is always just in numeric order). Separated by "_"_.
-  roundTime: Not meaningful.
-  time:  date and time for round end
-  name:  Player's selected 3-letter name (not guaranteed to be unique)
-  age:  Age selected by the participant.
-  grid:  The location of numerals in the grid.  For each numeral in "correct", the x and y position are seperated by a "-", and each position is seperated by a "_"
