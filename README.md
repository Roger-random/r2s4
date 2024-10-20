# R2S4: Roger Random's Spent Spool Storage System

Every 3D printing hobbyist using up a spool of filament has thought about
what to do with the empty spool. It is quite sturdy and just FEELS useful
for something more than just thrown away.

This repository has my suggestion on what to do with them: use an empty spool
as the chassis to hold 3D-printed trays organizing small parts. The concept
is not new and has been done many times, now I am contributing my take on
the idea.

The challenge is to make trays that fit a spool. Dimensions vary between
filament manufacturers, and even within the same company's filament product line
they may change their spool supplier for any reason. So there's no one size
fits all, thus an ideal situation for parametric CAD system such as
[CadQuery](https://github.com/CadQuery/cadquery). It is parametric CAD
using the Python programming language. This storage system started as a
CadQuery learning/practice exercise but it turned out well enough to have
graduated to its dedicated project repository here.

## Files

`r2s4.py` generates CadQuery geometry based on provided dimensions.

`single_wedge.py` uses `r2s4.py` to generate a single tray. This file was used
for interactive development using CadQuery's
[CQ-Editor](https://github.com/CadQuery/CQ-editor).

`geenerate_all.py` uses `r2s4.py` to generate a large number of STL files based
on lists of parameters defined within. This file is intended for command line
execution.

## Usage

The expect usage pattern is for you to clone this repository and edit
`generate_all.py` replacing my spindle spool dimensions with yours. Then run
`python generate_all.py` in order to generate organizer trays that fit your
spool. (CadQuery installation required.)

## Pre-generated STL

If you happen to have the same filament spools I do, pre-generated STL files
are available under `docs\stl`

### Version Information

This repository is originally created with CadQuery version 2.4.0.
Interactively created with CQ-Editor version 0.3.0dev.
CadQuery was running under Python 3.12.2
CadQuery was installed with mamba 1.5.9 via conda 24.9.2
Running within a Ubuntu 22.04.5 LTS virtual machine
