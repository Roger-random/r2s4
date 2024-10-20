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
wedge_size = 30

show_object(
    r2s4.build_base(
        inner_radius,
        spool_height,
        wedge_size),
    options = {"alpha":0.5, "color":"green"})

show_object(
    r2s4.build_placeholder(
        inner_radius,
        spool_height,
        wedge_size)
    .translate((0,0,-15)),
    options = {"alpha":0.5, "color":"aquamarine"})

show_object(r2s4.build_tray(
        inner_radius,
        spool_height,
        wedge_size),
    options = {"alpha":0.5, "color":"red"})
