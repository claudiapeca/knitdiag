# knitdiag
A python+cairo code for drawing knitting diagrams. 

It is not user-friendly: no front-end, only runs at the command line.

For now it is meant to draw _cable patterns_ only, no colour work, no increases and decreases (these will be added in the future). Standard row numbering and optional repetition marks are also included.

There is a good set of pre-programmed stitches (for example, knit-through-the-back-loop, and cross-stitches including those involving purl stitches).

There is also a couple of pre-programmed pattern examples, which make it easy to add new ones for anyone with basic programming skills. Patterns are simply a single string that lists the stitches, for example, "k5 p5 rc55 p5 k5", other necessary data such as the number of columns and lines of the diagram are kept on a tuple.
