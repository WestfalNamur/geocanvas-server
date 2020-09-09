# service/project/data_types/typed_dicts.py
"""Typed dictionaries."""


from typing import List
from typing_extensions import TypedDict


# configuration ---------------------------------------------------------------
GeoModelExtent = TypedDict(
    'GeoModelExtent',
    {
        "x_min": int,
        "x_max": int,
        "y_min": int,
        "y_max": int,
        "z_min": int,
        "z_max": int,
    }
)

Section = TypedDict(
    'Section',
    {
        'p1': List[int],
        'p2': List[int],
        'resolution': List[int]
    }
)

# topological data ------------------------------------------------------------
Serie = TypedDict(
    'Serie',
    {
        'name': str,
        'isfault': bool,
        'order_series': int
    }
)

Surface = TypedDict(
    'Surface',
    {
        'name': str,
        'serie': str,
        'order_surface': int
    }
)

# data ------------------------------------------------------------------------
SurfacePointNew = TypedDict(
    'SurfacePointNew',
    {
        'x': int,
        'y': int,
        'z': int,
        'surface': str,
        'probdist': str,
        'param1': float,
        'param2': float,
        'active': bool,
        'locstr': str
    }
)

SurfacePoint = TypedDict(
    'SurfacePoint',
    {
        'id': str,
        'x': int,
        'y': int,
        'z': int,
        'surface': str,
        'probdist': str,
        'param1': float,
        'param2': float,
        'active': bool,
        'locstr': str
    }
)

OrientationNew = TypedDict(
    'OrientationNew',
    {
        'id': str,
        'x': int,
        'y': int,
        'z': int,
        'azimuth': float,
        'dip': float,
        'polarity': float,
        'surface': str,
        'probdist': str,
        'param1': float,
        'param2': float,
        'active': bool,
        'locstr': str
    }
)

Orientation = TypedDict(
    'Orientation',
    {
        'id': str,
        'x': int,
        'y': int,
        'z': int,
        'azimuth': float,
        'dip': float,
        'polarity': float,
        'surface': str,
        'probdist': str,
        'param1': float,
        'param2': float,
        'active': bool,
        'locstr': str
    }
)
