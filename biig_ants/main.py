"""Synthetic tracking data"""

# TODO
# - make fns
# - add landscape seed as CLI argument

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
        random_seed=13,  # --------------- make this CLI argument
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


if __name__ == "__main__":
    main()
