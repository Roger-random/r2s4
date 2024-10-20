# R2S4: Roger Random's Spent Spool Storage System

Every 3D printing hobbyist using up a spool of filament has thought about
what to do with the empty spool. It is quite sturdy and just FEELS useful
for something more than just thrown away.

This repository has my suggestion on what to do with them: use an empty spool
as the chassis to hold 3D-printed trays organizing small parts. The concept
is not new and has been done many times. But this particular take on the idea
is mine and shared with everyone under MIT license.

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

## Ugh, install CadQuery?

Well, if the filament spool dimensions are already in `generate_all.py`,
then corresponding STL files are available under `docs\stl` subdirectory.

## What if none of those fit?

Fork this repository and add desired spool simensions to the existing list in
`generate_all.py`. Create a pull request with those dimensions. If they look
reasonable to me, I will accept the change. Then I will manually run
`generate_all.py` on my machine and add resulting STLs to the list of
pre-generated STLs in this repository.

Service Level Agreement: None. I may be busy and not get around to it for some
time. If you are unsatisfied you will be refunded the full service payment of
$0.00. Offer expire when I delete this section from the latest version of
this README file, or when I expire, whichever comes first.

I would prefer to automate this process (see below) but that has yet to happen.

# Is there an easier way?

Installing CadQuery is probably more work than most people would want to
deal with. I have ideas on how to make it easier, but I haven't put time
into executing these ideas. If you look at one of these and say "Oh I can
do that easily" or "That looks like an interesting project" consider this
your invitation!

### Web service

CadQuery installed and running alongside a simple web server. Somebody can
fill in their spindle spool dimensions on a form, hit "Submit", and get their
custom generated STLs available for download.

### Build automation

CadQuery incoproated into an automated pipeline. For example, maybe some
[GitHub Actions](https://docs.github.com/en/actions)
magic can handle automatically generating STL when someone generates a
pull request with updated `generate_all.py`

# It doesn't work on my machine. What did you use?

* This repository is originally created with CadQuery version 2.4.0.
* Interactively created with CQ-Editor version 0.3.0dev.
* Running under Python 3.12.2
* CadQuery was installed with mamba 1.5.9 via conda 24.9.2
* Running within an x86-\zv64 virtual machine running Ubuntu 22.04.5 LTS
