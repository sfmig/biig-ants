"""Synthetic tracking data"""

# TODO
# - make fns
# - scale not working?

import argparse
import math
import sys
from pathlib import Path

import addon_utils
import bpy


def main():
    ###########################
    # Enable landscape add-on
    ###########################
    landscape_addon = "ant_landscape"
    addon = bpy.context.preferences.addons.get(landscape_addon)

    if not addon:
        addon_utils.enable(landscape_addon, default_set=True)

    ###########################
    # Remove default objects
    ###########################
    # https://blender.stackexchange.com/questions/27234/python-how-to-completely-remove-an-object
    objs = list(bpy.context.scene.objects)
    with bpy.context.temp_override(selected_objects=objs):
        bpy.ops.object.delete()

    ###########################
    # Create random landscape
    ###########################
    bpy.ops.mesh.landscape_add(
        ant_terrain_name="Landscape",
        land_material="",
        water_material="",
        texture_block="",
        at_cursor=True,
        smooth_mesh=True,
        tri_face=False,
        sphere_mesh=False,
        subdivision_x=128,
        subdivision_y=128,
        mesh_size=2,
        mesh_size_x=2,
        mesh_size_y=2,
        random_seed=args.landscape_seed,
        noise_offset_x=0,
        noise_offset_y=0,
        noise_offset_z=0,
        noise_size_x=1,
        noise_size_y=1,
        noise_size_z=1,
        noise_size=1,
        noise_type="ridged_multi_fractal",
        basis_type="BLENDER",
        vl_basis_type="VORONOI_F1",
        distortion=1,
        hard_noise="1",
        noise_depth=8,
        amplitude=0.5,
        frequency=1.75,
        dimension=0.94,
        lacunarity=2.33,
        offset=0.9,
        gain=2.1,
        marble_bias="2",
        marble_sharp="0",
        marble_shape="0",
        height=0.3,
        height_invert=False,
        height_offset=0,
        fx_mixfactor=0,
        fx_mix_mode="0",
        fx_type="0",
        fx_bias="0",
        fx_turb=0,
        fx_depth=0,
        fx_amplitude=0.5,
        fx_frequency=1.5,
        fx_size=1,
        fx_loc_x=0,
        fx_loc_y=0,
        fx_height=0.5,
        fx_invert=False,
        fx_offset=0,
        edge_falloff="0",
        falloff_x=8,
        falloff_y=8,
        edge_level=0,
        maximum=0.5,
        minimum=-1,
        vert_group="",
        strata=11,
        strata_type="0",
        water_plane=False,
        water_level=0.04,
        remove_double=False,
        show_main_settings=True,
        show_noise_settings=True,
        show_displace_settings=True,
        refresh=True,
        auto_refresh=True,
    )

    ###########################
    # Make a sphere lord
    ###########################
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1,
        enter_editmode=False,
        align="WORLD",
        location=(1, 1, 0.25),  # m
        scale=(0.1, 0.1, 0.1),
    )

    ###########################
    # Add emitter plane
    ###########################
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        enter_editmode=False,
        align="WORLD",
        scale=(0.5, 0.5, 0.5),  # ---why ignored?
        location=(-1, 0, 1),  # m
        rotation=(0, math.pi / 2, 0),  # rad
    )

    ###########################
    # Add particle system
    ###########################
    bpy.ops.object.particle_system_add()  # assumes emitter object is selected
    bpy.data.particles["ParticleSettings"].physics_type = "BOIDS"

    # make this CLI / config params?
    bpy.data.particles["ParticleSettings"].count = 10
    bpy.data.particles["ParticleSettings"].lifetime = 200
    bpy.context.object.particle_systems["ParticleSystem"].seed = 42

    bpy.data.particles["ParticleSettings"].boids.use_land = True
    bpy.data.particles["ParticleSettings"].boids.use_flight = False

    # delete existing rules of boid brain
    particle_settings = bpy.data.particles["ParticleSettings"]
    with bpy.context.temp_override(particle_settings=particle_settings):
        bpy.ops.boid.rule_del()  # probs there is a better way to do this
        bpy.ops.boid.rule_del()
        bpy.ops.boid.rule_add(type="FOLLOW_LEADER")

    follow_rule = particle_settings.boids.states["State"].rules[
        "Follow Leader"
    ]
    follow_rule.use_in_air = False
    # set sphere as leader
    follow_rule.object = bpy.data.objects["Sphere"]

    ###########################
    # Add collision modifier to the landscape
    ###########################
    # bpy.ops.object.select_all(action='DESELECT')
    # bpy.data.objects["Landscape"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Landscape"]
    with bpy.context.temp_override(context="PHYSICS"):
        bpy.ops.object.modifier_add(type="COLLISION")

    ###########################
    # Make boids be insects
    ###########################
    eleodes_path = str(
        Path(__file__).parents[2] / "data" / "Eleodes_spec_cleaned.fbx"
    )
    bpy.ops.import_scene.fbx(filepath=eleodes_path)

    # rotate (hack to make bugs be upside down!)
    bpy.data.objects["Eleodes_spec"].location = [0.0, 0.0, 0.0]
    bpy.data.objects["Eleodes_spec"].rotation_euler = [
        0.0,
        math.pi,
        -math.pi / 2,
    ]

    with bpy.context.temp_override(context="PARTICLES"):
        bpy.data.particles["ParticleSettings"].render_type = "OBJECT"
        bpy.data.particles[
            "ParticleSettings"
        ].instance_object = bpy.data.objects["Eleodes_spec"]
        bpy.data.particles["ParticleSettings"].use_rotation_instance = True

    # Set up camera

    # Define render settings


if __name__ == "__main__":
    # get all arguments after '--' (all after -- are not read by blender)
    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1 :]

    # Create parser object
    usage_text = (
        "Run blender in background mode with this script:"
        "  blender --background --python " + __file__ + " -- [landscape_seed]"
    )
    parser = argparse.ArgumentParser(description=usage_text)

    # Add optional argument: modules_path
    parser.add_argument(
        "--landscape_seed",
        dest="landscape_seed",
        metavar="LANDSCAPE_SEED",
        default=42,
        help="Seed to generate a random ridge landscape",
    )

    ## Parse arguments
    args = parser.parse_args(argv)

    main()
