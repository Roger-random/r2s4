# R2S4: Roger Random's Spent Spool Storage System

Every 3D printing hobbyist using up a spool of filament has thought about
what to do with the empty spool. It is quite sturdy and just FEELS useful
for something more than just thrown away.

This repository has my suggestion on what to do with them: use an empty spool
as the chassis to hold 3D-printed trays organizing small parts. The concept
is not new and has been done many times. But this particular take on the idea
is mine and shared with everyone under MIT license.

![Trays installed](./img/r2s4%20fully%20populated%20mh%20build%20spool.jpg)

![Trays removed](./img/r2s4%20trays%20in%20common%20sizes.jpg)

The challenge is to make trays that fit a spool. Dimensions vary between
filament manufacturers, and even within the same company's filament product line
they may change their spool supplier for any reason. So there's no one size
fits all, thus an ideal situation for parametric CAD system such as
[CadQuery](https://github.com/CadQuery/cadquery). It is parametric CAD
using the Python programming language. This storage system started as a
CadQuery learning/practice exercise but it turned out well enough to have
graduated to its dedicated project repository here.

# Files

`r2s4.py` generates CadQuery geometry based on provided dimensions.

`single_wedge.py` uses `r2s4.py` to generate a single tray. This file was used
for interactive development using CadQuery's
[CQ-Editor](https://github.com/CadQuery/CQ-editor).

`geenerate_all.py` uses `r2s4.py` to generate a large number of STL files based
on lists of parameters defined within. This file is intended for command line
execution.

# STL generation

The expect usage pattern is for the user to clone this repository and edit
`generate_all.py` replacing my spindle spool dimensions. Then in a Python
environment with CadQuery installed, run `python generate_all.py` to generate
organizer trays with specified dimensions.

## What if I don't want to install CadQuery on my computer?

If you prefer not to run CadQuery on your own computer, use someone else's
computer a.k.a. cloud computing. As of this writing the easiest way to go is
to use Google Colab, which is a web-based Python interface very similar to
(derived from?) Jupyter notebooks. Process is very similar to running the
sibling project Storage Grid so I won't duplicate information here. See
[Storage Grid README](https://github.com/Roger-random/storage_grid)
for a walkthrough and adjust as needed for R2S4.

# It doesn't work on my machine. What did you use?

* This repository is originally created with CadQuery version 2.4.0.
* Interactively created with CQ-Editor version 0.3.0dev.
* Running under Python 3.12.2
* CadQuery was installed with mamba 1.5.9 via conda 24.9.2
* Running within an x86-64 virtual machine running Ubuntu 22.04.5 LTS

# More details about how this project came to be

See my online project notebook
[New Screwdriver entries tagged with 'r2s4'](https://newscrewdriver.com/tag/r2s4/)
