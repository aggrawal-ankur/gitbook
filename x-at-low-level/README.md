# How X Exist At Low Level?

_**August 13, 2025; 10:00 PM**_

***

To improve my low level understanding of compiled binaries, and organize that knowledge, I am writing a new series of articles, named "_How X exist at low level?_"

A compiled binary is made up of those simple, harmless artifacts of C. What makes them daunting is how they are used throughout the project and how they actually exist at low level.

This is my attempt to understand how these artifacts actually exist at low level.

* What is their shape?
* How they are interpreted by assembly?

This would help me a lot when I would be exploring binaries for reverse engineering. I am laying down the foundation here.

The scope of this series is limited to compiled binaries, for the time being. The language would be **C**.

Later on we can explore interpreted languages like python as well. Not now.
