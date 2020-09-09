"""Geo-model-data-functions."""

import uuid
from typing import Dict, Tuple

import project.data.data as geo_model_data
import project.types.typed_dicts as td

###############################################################################
###                             Configuration                               ###
###############################################################################


def mutate_geo_model_extent(
        new_geo_model_extent: td.GeoModelExtent
) -> Tuple[td.GeoModelExtent, str]:
    """Mutates geo-model-extent."""
    geo_model_data.geo_model_extent = new_geo_model_extent
    data = geo_model_data.geo_model_extent
    message = 'Geo-model-extent mutated.'
    # print(geo_model_data.geo_model_extent)
    return data, message


def mutate_section(new_section: td.Section) -> Tuple[td.Section, str]:
    """Mutates the geo-model-section."""
    geo_model_data.section = new_section
    data = geo_model_data.section
    message = 'Geo-model-section mutated.'
    # print(geo_model_data.section)
    return data, message


###############################################################################
###                             Topology data                               ###
###############################################################################


def mutate_geo_model_serie(serie: td.Serie) -> Tuple[Dict, str]:
    """Mutates a geo-model-series-df."""
    geo_model_data.series_df.loc[serie['name']] = serie
    data = geo_model_data.series_df.to_dict('records')
    message = f'New Serie added.'
    # print(geo_model_data.series_df)
    return data, message


def delete_geo_model_sereie(serie: td.Serie) -> Tuple[Dict, str]:
    """Delete a serie from geo-model-series-series-df."""
    geo_model_data.series_df.drop(serie['name'], inplace=True)
    data = geo_model_data.series_df.to_dict('records')
    message = 'Serie deleted.'
    # print(geo_model_data.series_df)
    return data, message


def mutate_geo_model_surface(surface: td.Surface) -> Tuple[Dict, str]:
    """Mutates a geo-model-surfaces-df."""
    geo_model_data.surfaces_df.loc[surface['name']] = surface
    data = geo_model_data.surfaces_df.to_dict('records')
    message = 'New surface added.'
    # print(geo_model_data.surfaces_df)
    return data, message


def delete_geo_model_surface(surface: td.Surface) -> Tuple[Dict, str]:
    """Delete a serie from geo-model-series-surfaces-df."""
    geo_model_data.surfaces_df.drop(surface['name'], inplace=True)
    data = geo_model_data.surfaces_df.to_dict('records')
    message = 'Surface deleted.'
    # print(geo_model_data.surfaces_df)
    return data, message


###############################################################################
###                         Geological input data                           ###
###############################################################################

def add_geo_model_surface_point(
        surface_point_new: td.SurfacePointNew) -> Tuple[Dict, str]:
    """Adds a surface point."""
    new_rand_id = str(uuid.uuid4())
    xs = {'id': new_rand_id}
    surface_point: td.SurfacePoint = dict(**surface_point_new, **xs)  # type: ignore
    geo_model_data.surface_points_df.loc[new_rand_id] = surface_point
    data = geo_model_data.surface_points_df.loc[new_rand_id].to_dict()
    message = 'Geo-model-surface-point added.'
    # print(geo_model_data.surface_points_df)
    return data, message


def mutate_geo_model_surface_point(
        surface_point: td.SurfacePoint) -> Tuple[Dict, str]:
    """Mutates geo-model-surface-point."""
    geo_model_data.surface_points_df.loc[surface_point['id']] = surface_point
    data = geo_model_data.surface_points_df.loc[surface_point['id']].to_dict()
    message = 'Geo-model-surface-point changed.'
    # print(geo_model_data.surface_points_df)
    return data, message


def delete_geo_model_surface_point(
        surface_point: td.SurfacePoint) -> Tuple[Dict, str]:
    """Delete a geo-model-surface-point."""
    geo_model_data.surface_points_df.drop(surface_point['id'], inplace=True)
    data = geo_model_data.surface_points_df.to_dict('records')
    message = 'Geo-model-surface-point deleted.'
    # print(geo_model_data.surface_points_df)
    return data, message


def add_geo_model_orientation(
        orientation_new: td.OrientationNew) -> Tuple[Dict, str]:
    """Adds a new orientation."""
    new_rand_id = str(uuid.uuid4())
    xs = {'id': new_rand_id}
    orientation: td.Orientation = dict(**orientation_new, **xs)  # type: ignore
    geo_model_data.orientations_df.loc[new_rand_id] = orientation
    data = geo_model_data.orientations_df.loc[new_rand_id].to_dict()
    message = 'Orientation added.'
    # print(geo_model_data.surface_points_df)
    return data, message


def mutate_geo_model_orientation(
        orientation: td.Orientation) -> Tuple[Dict, str]:
    """Mutates geo-model-orientation."""
    geo_model_data.orientations_df.loc[orientation['id']] = orientation
    data = geo_model_data.orientations_df.to_dict('records')
    message = 'Geo-model-orientaions'
    # print(geo_model_data.orientations_df)
    return data, message


def delete_geo_model_orientation(
        orientation: td.Orientation) -> Tuple[Dict, str]:
    """Delete a geo-model-orientaions."""
    geo_model_data.orientations_df.drop(orientation['id'], inplace=True)
    data = geo_model_data.orientations_df.to_dict('records')
    message = 'Geo-model-orientation deleted.'
    # print(geo_model_data.orientations_df)
    return data, message
