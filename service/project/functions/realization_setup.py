import gempy as gp  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

import project.types.typed_dicts as td
import project.functions.pre_processing as pre_pro


def set_congiguration(
        geo_model: gp.Model,
        geo_model_extent: td.GeoModelExtent,
        section: td.Section
) -> None:
    """Sets geo_model extent, resolution and section.

    Args:
        geo_model = app geo_model object
        geo_model_extent = model extent stored in data
        section = only model section stored in data
    """

    # process input
    extent = list(geo_model_extent.values())

    # Set extent
    # Fix for Bug  # Replace with geo_model.set_extent(extent=extent)
    gp.init_data(
        geo_model,
        extent=extent,
        resolution=[10, 10, 10]
    )

    # Set grids
    section_dict = {'section': (
        section['p1'],
        section['p2'],
        section['resolution']
    )}
    geo_model.set_section_grid(section_dict=section_dict)


def update_series(
        geo_model: gp.Model,
        series_df: pd.DataFrame
) -> None:
    """Updates series of the geo-model to the one stored in data.

    Deletes currently existing series in geo_model, sets series passed in
    series_df and sets faults.
    Note: TO_DELETE added as empty series throw an error;

    Args:
        geo_model = The geo_model
        series_df = series
    """

    # remove old state  # gempy does not allow emtpy sereies
    old_series = geo_model.series.df.index.to_list()

    try:
        geo_model.add_series(series_list=['TO_DELETE'])
    except:
        pass  

    try:
        geo_model.add_series(series_list=['TO_DELETE'])
    except:
        pass

    try:
        geo_model.delete_series(old_series)
    except:
        pass

    # set new state  # sort by order
    series_df.sort_index()
    series_df.sort_values(by=['order_series'], inplace=True)
    new_series = series_df['name'].to_list()
    geo_model.add_series(new_series)

    # HOTFIX
    try:
        geo_model.delete_series(['TO_DELETE'])
    except:
        pass

    print('HOTFIX in update_series()')


def update_surfaces(
        geo_model: gp.Model,
        surfaces_df: pd.DataFrame
) -> None:
    """Updates surfaces of the geo-model to the one stored in data.

    Deletes currently existing surfaces in geo_model and sets surfaces passed
    in surfaces_df.
    Loops over surfaces to map them to series.

    Args:
        geo_model = The geo_model
        series_df = surfaces
    """

    # remove old state
    old_surfaces = geo_model.surfaces.df['surface'].to_list()
    try:
        geo_model.delete_surfaces(old_surfaces)
    except:
        print('HOTFIX in update_surfaces()')

    # set new state
    surfaces_df.sort_values(by=['order_surface'], inplace=True)
    new_surfaces = surfaces_df['name'].to_list()
    geo_model.add_surfaces(new_surfaces)


def creat_mapping_object(
        surfaces_df: pd.DataFrame,
        series_df: pd.DataFrame
) -> object:
    """Creates an object maping series to surfaces.

    Important as it also sets the surface order of the geo_model.

    Args:
        surfaces_df = surfaces
        series_df = series
    """

    surfaces_df.sort_values(by=['order_surface'])
    mapping_object = {}
    for index, row in series_df.iterrows():

        series_name = row['name']
        categories = surfaces_df[surfaces_df['serie']
                                 == series_name]['name'].astype('category')
        mapping_object[series_name] = categories

    return mapping_object


def setup_realization(
        geo_model: gp.Model,
        geo_model_extent: td.GeoModelExtent,
        section: td.Section,
        series_df: pd.DataFrame,
        surfaces_df: pd.DataFrame,
        surface_points_original_df: pd.DataFrame,
        orientations_original_df: pd.DataFrame
) -> None:
    """Configur the geo_model for a realization based on current data in
    memory.

    # _original as during UQ runs a copy is created that gets maniplated;

    Args:
        geo_model = app geo_model object
        geo_model_extent = model extent stored in data
        section = only model section stored in data
        surfaces_df = surfaces
        series_df = series
        surface_points_original_df = surface points
        orientations_original_df = orientations
    """

    # set extent and section
    set_congiguration(geo_model, geo_model_extent, section)

    # update stored series
    update_series(geo_model, series_df)
    # update stored surfaces
    update_surfaces(geo_model, surfaces_df)

    # process geo-data-input
    table_surface_points, table_orientations = pre_pro.format_geological_input_data(
        surface_points_df=surface_points_original_df,
        orientations_df=orientations_original_df
    )
    # set surface points
    geo_model.set_surface_points(
        table=table_surface_points,
        update_surfaces=False
    )
    # set orientations
    geo_model.set_orientations(
        table=table_orientations,
        update_surfaces=False
    )

    # set series to surface relations as well as thier order
    mapping_object = creat_mapping_object(surfaces_df, series_df)
    gp.map_series_to_surfaces(
        geo_model=geo_model,
        mapping_object=mapping_object
    )

    # set fault if any
    if np.any(series_df['isfault']):

        fault_series = series_df[series_df['isfault']]['name']
        geo_model.set_is_fault(fault_series)

    # update new data to interpolator
    geo_model.update_to_interpolator()
