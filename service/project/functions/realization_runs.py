import gempy as gp  # type: ignore
import numpy as np  # type: ignore

import project.functions.realization_setup as real_setup
import project.data.data as geo_data
from project.gpmodel import geo_model
import project.functions.post_processing as post_pro


def check_setup_single_realization(geo_model):

    print('Run realizations setup checks until stable workflow.')

    # check if surface_points are within geo-model-extent
    current_extent = geo_model.grid.regular_grid.extent
    if not (
        current_extent[0] <= np.min(geo_model.surface_points.df['X'].values) and
        current_extent[1] >= np.max(geo_model.surface_points.df['X'].values) and
        current_extent[2] <= np.min(geo_model.surface_points.df['Y'].values) and
        current_extent[3] >= np.max(geo_model.surface_points.df['Y'].values) and
        current_extent[4] <= np.min(geo_model.surface_points.df['Z'].values) and
        current_extent[5] >= np.max(geo_model.surface_points.df['Z'].values)
    ):
        raise ValueError(
            f'Some surface-poins are not within geo-model-extent-bounds')

    # check if orientations are within geo-model-extent
    if not (
        current_extent[0] <= np.min(geo_model.orientations.df['X'].values) and
        current_extent[1] >= np.max(geo_model.orientations.df['X'].values) and
        current_extent[2] <= np.min(geo_model.orientations.df['Y'].values) and
        current_extent[3] >= np.max(geo_model.orientations.df['Y'].values) and
        current_extent[4] <= np.min(geo_model.orientations.df['Z'].values) and
        current_extent[5] >= np.max(geo_model.orientations.df['Z'].values)
    ):
        raise ValueError(
            f'Some orientations are not within geo-model-extent-bounds')

    # check if at least one orientaion per series
    orientation_series = geo_model.orientations.df['series'].unique()
    geo_model_series = list(geo_model.series.df.index)
    if not all([serie in geo_model_series for serie in orientation_series]):

        raise ValueError(f'Some series have no orientaion')

    # check if at least two surface-points per surface
    surfaces_surface_points = geo_model.surface_points.df
    surfaces_geo_model = list(geo_model.surfaces.df['surface'])
    for surface in surfaces_geo_model:

        if not surface == 'basement':
            len_df = len(
                surfaces_surface_points[surfaces_surface_points['surface'] == surface])
            if len_df < 2:

                raise ValueError(
                    f'Each surface needs at least 2 surface points.')

    return True


def calculate_surface_tops_coordinates():
    """Sets up, runs and process a realization based on current state of data.

    Args are direct references to and scoped within script;
    """

    # setup realization with current data in memory
    real_setup.setup_realization(
        geo_model=geo_model,
        geo_model_extent=geo_data.geo_model_extent,
        section=geo_data.section,
        series_df=geo_data.series_df,
        surfaces_df=geo_data.surfaces_df,
        surface_points_original_df=geo_data.surface_points_df,
        orientations_original_df=geo_data.orientations_df
    )

    # check setup and run realization if checks pass
    if check_setup_single_realization(geo_model):

        gp.compute_model(model=geo_model, sort_surfaces=False)

    # compute boolan matrices makring surface tops in section
    B_tops = post_pro.compute_boolean_matrix_for_section_surface_top()

    # compute sectiono grid coordinates
    extent = list(geo_data.geo_model_extent.values())
    section_grid_coordinates = post_pro.compute_setction_grid_coordinates()

    # extract surface-tops as dictionary
    tops_dict = post_pro.get_tops_coordinates(
        boolen_matrix_of_tops=B_tops,
        section_coordinates=section_grid_coordinates)

    # create and save figure for quality control
    post_pro.plot_tops(
        tops_coordinates=tops_dict,
        name='section-tops',
        xmin=0,
        xmax=geo_data.section['resolution'][0],
        ymin=0,
        ymax=geo_data.section['resolution'][1])

    # return
    return tops_dict


def run_realization():

    real_setup.setup_realization(
        geo_model=geo_model,
        geo_model_extent=geo_data.geo_model_extent,
        section=geo_data.section,
        series_df=geo_data.series_df,
        surfaces_df=geo_data.surfaces_df,
        surface_points_original_df=geo_data.surface_points_df,
        orientations_original_df=geo_data.orientations_df
    )

    if check_setup_single_realization(geo_model):
        gp.compute_model(model=geo_model, sort_surfaces=False)
