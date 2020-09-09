""" Geo-model-server data. """

import pandas as pd  # type: ignore
import project.types.typed_dicts as td


###############################################################################
###                             Configuration                               ###
###############################################################################
# geo_model_extent
geo_model_extent: td.GeoModelExtent = {
    "x_min": 0,
    "x_max": 1000,
    "y_min": 0,
    "y_max": 1000,
    "z_min": 0,
    "z_max": 1000,
}

# section-dictionary
section: td.Section = {
    'p1': [0, 500],
    'p2': [1000, 500],
    'resolution': [100, 100]
}

###############################################################################
###                             Topology data                               ###
###############################################################################
# Series
series_df = pd.DataFrame(columns=['name', 'isfault', 'order_series'])

# Surfaces
surfaces_df = pd.DataFrame(columns=['name', 'serie', 'order_surface'])


###############################################################################
###                         Geological input data                           ###
###############################################################################
# SurfacePoints
surface_points_df = pd.DataFrame(
    columns=[
        'id',
        'x',
        'y',
        'z',
        'surface',
        'probdist',
        'param1',
        'param2',
        'active',
        'locstr'
    ]
)

# Orientations
orientations_df = pd.DataFrame(
    columns=[
        'id',
        'x',
        'y',
        'z',
        'azimuth',
        'dip',
        'polarity',
        'surface',
        'probdist',
        'param1',
        'param2',
        'active',
        'locstr'
    ]
)
