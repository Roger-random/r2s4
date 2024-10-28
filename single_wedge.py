"""
MIT License

Copyright (c) 2024 Roger Cheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Single Wedge

This file is intended for use in CQ-Editor and visualize a single wedge of
the spent spool storage system with given parameters.
"""
import math
import r2s4

# Calculate spool inner radius from measuring circumference of spool center
#spool_inner_circumference = 283 # MH Build
spool_inner_circumference = 347 # Filament PM
inner_radius = spool_inner_circumference / (math.pi*2)

# Outer spool diameter is easier to measure directly
spool_outer_diameter = 200 # MH Build, Filament PM
spool_outer_radius = spool_outer_diameter / 2

#######################################################################
#
#  Dimensions of target spent spool spindle
#
#spool_height = 55 # MH Build
spool_height = 70 # Filament PM

#######################################################################
#
#  How big of a wedge we want in degrees
#
wedge_size = 15

#######################################################################
#
#  Additional space between mating surfaces due to 3D printing inaccuracy.
#  May require adjustment to fit specific combinations of printer,
#  filment, print profile, etc.
#
#  Dimensionally perfect printes will generate pieces that fit together
#  snugly with this value set to zero. This is rare. Due to layer-to-
#  layer variations, nozzle erosion, etc. Most 3D printers will need a
#  little extra clearance to fit well.
#
#  If base segments don't fit into each other, increase this value.
#  If they fit too loosely, decrease this value.
#
#  Recommend increasing/decreasing in increments of 0.05mm
#
#  If fit is still loose at no additional clearance, the printer has an
#  under-extrusion issue that needs to be investigated.
#
#  If fit is still tight at 0.4mm... that's the diameter of the nozzle!
#  the printer has an accuracy issue that needs to be resolved.
#
additional_clearance = 0.1 # mm

#######################################################################
#
#  Build and show
#
show_object(
    r2s4.build_base(
        inner_radius,
        spool_outer_radius,
        spool_height,
        wedge_size,
        additional_clearance
        ).rotate((0,0,0),(0,0,1),-wedge_size/2),
    options = {"alpha":0.5, "color":"green"})

show_object(
    r2s4.build_placeholder(
        inner_radius,
        spool_outer_radius,
        spool_height,
        wedge_size,
        additional_clearance
        ).rotate((0,0,0),(0,0,1),-wedge_size/2)
    .translate((0,0,-15)),
    options = {"alpha":0.5, "color":"aquamarine"})

show_object(r2s4.build_tray(
        inner_radius,
        spool_outer_radius,
        spool_height,
        wedge_size
        ).rotate((0,0,0),(0,0,1),-wedge_size/2),
    options = {"alpha":0.5, "color":"red"})
