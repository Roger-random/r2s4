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
Spent Spool Storage System

Reuse empty 3D printing filament spools as the core for a storage system for
small parts. This script generates wedge-shaped storage trays that sit in a
matching base. Bases for all wedges (plus any placeholders) snap-fit
together into a ring to hold everything together.

Since different filament vendors use different spools, this script adapts to
parameters specifying spool dimensions:
    1. Inner radius
    2. Outer radius
    3. Height (distance between two sides)

The fourth critical parameter is the size of the desired storage wedge
specified in degrees. A full spool storage system can be assembled out of any
number of wedges (or placeholders) as long as they add up to 360 degrees.

Works best in the range of 30-60 degrees.
Minimum size is roughly 15 degrees depending on spool outer radius.
Maximum size is 120 degrees as the geometry starts failing beyond that.

For the adventurous experimenters, more parameters are present as constants
and can be adjusted but interactions can be unpredictable.

Written in CQ-Editor 0.3.0dev

"""
import cadquery as cq

nozzle_diameter = 0.4

#######################################################################
#
#  Dimensions of storage system components
#

# Tray actually extends beyond edge of spool
beyond_edge = 10

ring_depth = 6
ring_height = 4
ring_chamfer = 2 # Because spool inner corner is probably not perfectly square

# Tray dimensions
tray_edge_fillet = 2
tray_top_chamfer = ring_chamfer

latch_depth = 5
latch_protrude = 0.5

handle_sphere_size=15
handle_cut_depth=5

#######################################################################
#
#  Profile for inner ring segments that clicks together
#
def ring_root_profile(inner_radius):
    return (
        cq.Workplane("XZ")
        .lineTo(0,ring_height)
        .lineTo(inner_radius + ring_depth, ring_height)
        .lineTo(inner_radius + ring_depth + ring_height, 0)
        .close()
        )

#######################################################################
#
# Given a ring root profile, add left and right side rails
#
def add_side_rails(base, inner_radius, outer_radius, height, wedge_size):
    for rail_index in (0,1):
        if rail_index == 0:
            mirror = 1
        else:
            mirror = -1

        rail = (
            cq.Workplane("YZ")
            .transformed(rotate=cq.Vector(0,wedge_size*rail_index,0))
            .lineTo(0,ring_height)
            .lineTo((ring_height*mirror)/2,0)
            .close()
            .extrude(outer_radius)
            )
        base = base + rail

    # Clean up the extraneous guilde rail segments
    cleanup = (
        cq.Workplane("XY")
        .circle(outer_radius)
        .circle(inner_radius)
        .extrude(height*2,both=True)
        )
    base = base.intersect(cleanup)

    return base

#######################################################################
#
# Generate the outer fence which keeps the tray from falling out.
# Intended to be added to a base with side rails.
#
def build_outer_fence(outer_radius, wedge_size, additional_clearance):
    latch_gap = latch_protrude+additional_clearance

    # Add a short fence to keep tray from falling out too easily
    fence = (
        cq.Workplane("XZ")
        .lineTo(outer_radius-latch_depth+latch_protrude+latch_gap,0,True)
        .lineTo(outer_radius-latch_depth+latch_gap,ring_height)
        .lineTo(outer_radius                      ,ring_height)
        .lineTo(outer_radius                      ,0)
        .close()
        .revolve(wedge_size, (0,0,0), (0,1,0))
        )

    # Tab for holding down the fence during tray removal
    fence_tab_ball = (
        cq.Workplane("XZ")
        .transformed(rotate=cq.Vector(0,wedge_size/2,0))
        .transformed(offset = cq.Vector(
            outer_radius-handle_sphere_size+handle_cut_depth/2, ring_height/2, 0))
        .sphere(handle_sphere_size)
        )
    fence_tab_keep = (
        cq.Workplane("XZ")
        .lineTo(outer_radius,0,True)
        .lineTo(outer_radius,ring_height)
        .lineTo(outer_radius + handle_sphere_size,ring_height)
        .lineTo(outer_radius + handle_sphere_size,0)
        .close()
        .revolve(wedge_size, (0,0,0), (0,1,0))
        )
    return fence + fence_tab_ball.intersect(fence_tab_keep)

#######################################################################
#
# Modify base with linkage to connect multiple units together
#
def add_links(base, inner_radius, wedge_size, additional_clearance):
    ring_tab_radius = (ring_depth+ring_height-ring_chamfer)/2 - nozzle_diameter*4
    ring_tab_distance = 3 # Degrees
    ring_tab_arm_half = ring_tab_radius * 0.5
    ring_tab_slot_half = ring_tab_arm_half + nozzle_diameter + additional_clearance*2
    tab_position_radius = inner_radius+ring_depth/2+ring_chamfer/2-ring_height/2

    # Add tab and arm
    tab = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0,0,wedge_size+ring_tab_distance))
        .transformed(offset = cq.Vector(tab_position_radius+ring_height, 0, 0))
        .circle(ring_tab_radius-additional_clearance)
        .workplane(offset=ring_height)
        .transformed(offset = cq.Vector(-ring_height, 0, 0))
        .circle(ring_tab_radius-additional_clearance)
        .loft()
    )
    base = base+tab

    tab_arm = (
        cq.Workplane("XZ")
        .transformed(rotate=cq.Vector(0,wedge_size-2,0))
        .lineTo(tab_position_radius-ring_tab_arm_half+ring_height, 0, True)
        .lineTo(tab_position_radius-ring_tab_arm_half,             ring_height)
        .lineTo(tab_position_radius+ring_tab_arm_half,             ring_height)
        .lineTo(tab_position_radius+ring_tab_arm_half+ring_height, 0)
        .close()
        .revolve(ring_tab_distance+2)
    )
    base = base+tab_arm

    # Result of extrusion pokes into spool cylinder volume. Cut that off.
    cleanup = (
        cq.Workplane("XY")
        .circle(inner_radius)
        .extrude(ring_height)
        )
    base = base - cleanup

    # Cut a slot for the above tab to fit into
    slot = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0,0,ring_tab_distance))
        .transformed(offset = cq.Vector(tab_position_radius+ring_height, 0, 0))
        .circle(ring_tab_radius)
        .workplane(offset=ring_height)
        .transformed(offset = cq.Vector(-ring_height, 0, 0))
        .circle(ring_tab_radius)
        .loft()
    )
    slot_arm = (
        cq.Workplane("XZ")
        .lineTo(tab_position_radius-ring_tab_slot_half+ring_height, 0, True)
        .lineTo(tab_position_radius-ring_tab_slot_half,             ring_height)
        .lineTo(tab_position_radius+ring_tab_slot_half,             ring_height)
        .lineTo(tab_position_radius+ring_tab_slot_half+ring_height, 0)
        .close()
        .revolve(ring_tab_distance)
        )
    base = base - (slot+slot_arm)

    return base

#######################################################################
#
# Build a base for the tray
#
def build_base(inner_radius, spool_outer_radius, spool_height, wedge_size, additional_clearance = 0):
    outer_radius = spool_outer_radius + beyond_edge
    height = spool_height - ring_height

    base = ring_root_profile(inner_radius).revolve(wedge_size, (0,0,0), (0,1,0))
    base = add_side_rails(base, inner_radius, outer_radius, height, wedge_size)
    base = base + build_outer_fence(outer_radius, wedge_size, additional_clearance)
    base = add_links(base, inner_radius, wedge_size, additional_clearance)

    # Chamfer the inner bottom corner because corresponding spool interior is not perfectly square
    ring_chamfer_cut = (
        cq.Workplane("XZ")
        .lineTo(inner_radius+ring_chamfer, 0)
        .lineTo(inner_radius             , ring_chamfer)
        .close()
        .revolve(wedge_size)
        )
    base = base - ring_chamfer_cut

    return base

#######################################################################
#
# A placeholder segment is the base but with side # rails and fence
# cut off. Used to hold the ring together in absence of tray+base
#
def build_placeholder(inner_radius, spool_outer_radius, spool_height, wedge_size, additional_clearance = 0):
    return (
        build_base(inner_radius, spool_outer_radius, spool_height,wedge_size,additional_clearance)
        .intersect(ring_root_profile(inner_radius).revolve(360, (0,0,0), (0,1,0)))
    )

#######################################################################
#
# Cut a chamfer on the radial (straight edges from inner to outer curves)
# tray edges. The top edge adds a bit of structural strength and the bottom
# edge is required to accommodate base rails.
#
def chamfer_tray_radial_edges(tray, outer_radius, height, wedge_size):
    for edge_index in (0,1):
        if edge_index == 0:
            mirror = 1
        else:
            mirror = -1

        top_edge = (
            cq.Workplane("YZ")
            .transformed(rotate=cq.Vector(0,wedge_size*edge_index,0))
            .lineTo(0,height-tray_top_chamfer,True)
            .lineTo(0,height)
            .lineTo(mirror*tray_top_chamfer/2,height)
            .close()
            .extrude(outer_radius)
            )
        tray = tray - top_edge

        bottom_edge = (
            cq.Workplane("YZ")
            .transformed(rotate=cq.Vector(0,wedge_size*edge_index,0))
            .lineTo(0,ring_height)
            .lineTo((ring_height*mirror/2),0)
            .close()
            .extrude(outer_radius)
            )
        tray = tray - bottom_edge

    return tray

#######################################################################
#
# Add handle to tray
#
def add_handle(tray, outer_radius, height, wedge_size):
    # Constant parameters
    handle_width_half = 2

    handle_cutout = (
        cq.Workplane("XZ")
        .transformed(rotate=cq.Vector(0,wedge_size/2,0))
        .transformed(offset = cq.Vector(outer_radius+handle_sphere_size-handle_cut_depth, height/2, 0))
        .sphere(handle_sphere_size)
        )
    handle_keep = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0,0, wedge_size/2))
        .lineTo(outer_radius - handle_cut_depth,    handle_width_half, True)
        .lineTo(outer_radius + handle_sphere_size,  handle_width_half)
        .lineTo(outer_radius + handle_sphere_size, -handle_width_half)
        .lineTo(outer_radius - handle_cut_depth,   -handle_width_half)
        .close()
        .extrude(height)
        )
    tray = tray - (handle_cutout - handle_keep)

    handle_add = (
        cq.Workplane("XZ")
        .transformed(rotate=cq.Vector(0,wedge_size/2,0))
        .transformed(offset = cq.Vector(outer_radius-handle_sphere_size+handle_cut_depth, height/2, 0))
        .sphere(handle_sphere_size)
        )
    handle_add = handle_add.intersect(handle_keep)
    tray = tray+handle_add

    return tray

#######################################################################
#
# Cut small ribs in the side of the tray as reinforcement
# Critical to prevent flat sides warping under vase mode printing.
#
def cut_reinforcement_ribs(tray, inner_radius, outer_radius, height, wedge_size):
    # Constant parameters
    rib_spacing_target=7.5
    rib_size_bottom = 3
    rib_size_top = 1

    # Derived parameters
    rib_span = int(outer_radius-beyond_edge-inner_radius)
    rib_count = int(rib_span / rib_spacing_target)
    rib_spacing = int(rib_span / rib_count)

    for rib_angle in (0,wedge_size):
        for rib_radius in range(rib_spacing, rib_span, rib_spacing):
            rib = (
                cq.Workplane("XY")
                .transformed(rotate=cq.Vector(0,0,rib_angle))
                .transformed(offset = cq.Vector(inner_radius + rib_radius, 0, 0))
                .polygon(6, rib_size_bottom, circumscribed=True)
                .workplane(offset=height)
                .polygon(6, rib_size_top, circumscribed=True)
                .loft()
                )
            tray = tray-rib

    return tray

#######################################################################
#
# Create the text label to be embossed on the bottom of the tray
#
def build_label(inner_radius, spool_outer_radius, outer_radius, spool_height, wedge_size):
    inner_edge = inner_radius + ring_depth + ring_height
    outer_edge = outer_radius - latch_depth
    text_center = inner_edge + (outer_edge-inner_edge)/2
    return (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(180, 0, -wedge_size/2))
        .transformed(offset = cq.Vector(text_center, 0, 0))
        .text("R2S4 1.0\n{} {} {} {}"
              .format(
                  int(inner_radius),
                  int(spool_outer_radius),
                  int(spool_height),
                  int(wedge_size)),
              4,-0.25, kind='bold')
        )

#######################################################################
#
# A placeholder segment is the base but with side # rails and fence
# cut off. Used to hold the ring together in absence of tray+base
#
def build_tray(inner_radius, spool_outer_radius, spool_height, wedge_size, wall_thickness=0, label = True):
    outer_radius = spool_outer_radius + beyond_edge
    height = spool_height - ring_height
    tray = (
        cq.Workplane("XZ")
        .lineTo(inner_radius,height-tray_top_chamfer,True)
        .lineTo(inner_radius+tray_top_chamfer,height)
        .lineTo(outer_radius-beyond_edge,height)
        .lineTo(outer_radius,height-beyond_edge)
        .lineTo(outer_radius,ring_height + latch_depth)
        .lineTo(outer_radius-latch_depth, ring_height)
        .lineTo(outer_radius-latch_depth+latch_protrude, 0)
        .lineTo(inner_radius + ring_depth + ring_height, 0)
        .lineTo(inner_radius, ring_depth+ring_height)
        .close()
        .revolve(wedge_size, (0,0,0), (0,1,0))
        )

    tray = tray.edges("|Z").fillet(tray_edge_fillet)
    tray = chamfer_tray_radial_edges(tray, outer_radius, height, wedge_size)
    tray = add_handle(tray, outer_radius, height, wedge_size)
    tray = cut_reinforcement_ribs(tray, inner_radius, outer_radius, height, wedge_size)
    # Thickness zero generates a solid for printing in vase mode. Otherwise
    # generates a tray with specified wall thickness that is printed normally
    if wall_thickness > 0:
        tray = tray.faces("+Z").shell(-wall_thickness)
    # Label causes MatterControl slicer to create phantom first layer. PrusaSlicer OK.
    if label:
        tray = tray - build_label(inner_radius, spool_outer_radius, outer_radius, spool_height, wedge_size)

    return tray
