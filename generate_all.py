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
Generate All

This file is intended for command line execution and will generate a large set
of STL files by iterating through provided parameters to generate a variety
of sizes (specified as degrees in units of angles) for each spool type.

Note: cadquery.exporters.export() seems to silently fail if the output
subdirectory does not already exist. So if nothing seems to happen, double
check the directory structure.
"""
import math
import os

from cadquery import exporters
import r2s4

output_root = './docs/stl'

# Parameters required to specify spindle dimensions
# 1. Name to identify spool, used in subdirectory name
# 2. Inner radius in mm
# 3. Outer radius in mm
# 4. Height in mm
spools = (
    {
        "name"   : "filament_pm",
        "inner"  : 347 / (math.pi*2),
        "outer"  : 200 / 2,
        "height" : 70
    },
    {
        "name"   : "matterhackers",
        "inner"  : 283 / (math.pi*2),
        "outer"  : 200 / 2,
        "height" : 55
    },
)

# Sizes to generate for each type of spool
sizes = (15, 30, 45, 60, 90, 120)

# Create output directory if not already exist (should be rare)
if not os.path.exists(output_root):
    os.mkdir(output_root)

#
for spool in spools:
    subdirectory = "{:s}/{:d}_{:d}_{:d}_{:s}".format(
        output_root,
        int(spool["inner"]),
        int(spool["outer"]),
        int(spool["height"]),
        spool["name"]
    )

    print(subdirectory)
    if not os.path.exists(subdirectory):
        # Expected to happen when a new spool is added
        os.mkdir(subdirectory)
    for size in sizes:
        filename = "{:s}/base_{:d}.stl".format(subdirectory, size)
        print(filename)
        test_tray = r2s4.build_base(
            spool["inner"],
            spool["outer"],
            spool["height"],
            size).rotate((0,0,0),(0,0,1),-90-size/2)
        exporters.export(test_tray,filename)

        filename = "{:s}/tray_{:d}.stl".format(subdirectory, size)
        print(filename)
        test_tray = r2s4.build_tray(
            spool["inner"],
            spool["outer"],
            spool["height"],
            size, label=False).rotate((0,0,0),(0,0,1),-90-size/2)
        exporters.export(test_tray,filename)

        filename = "{:s}/placeholder_{:d}.stl".format(subdirectory, size)
        print(filename)
        test_tray = r2s4.build_placeholder(
            spool["inner"],
            spool["outer"],
            spool["height"],
            size).rotate((0,0,0),(0,0,1),-90-size/2)
        exporters.export(test_tray,filename)
