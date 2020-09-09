"""Default geo_model data. """
import os
import uuid
from pathlib import Path
import project.data.data as geo_data
from project.api.data import geo_model_data_blueprint

import pandas as pd  # type: ignore

import project.functions.data as geo_data_func
import project.types.typed_dicts as td

PROJECT_PATH = str(Path(os.path.dirname(
    os.path.realpath(__file__))).parent)


def setup_default_model_small():
    """Sets up a small fault model.

    Operates directly on the server geo_model object;
    """
    # meta-data ---------------------------------------------------------------
    # geo-model-extent
    geo_data_func.mutate_geo_model_extent(
        new_geo_model_extent={
            "x_min": 0,
            "x_max": 650,
            "y_min": 0,
            "y_max": 650,
            "z_min": 0,
            "z_max": 435,
        })

    # geo-model-section
    geo_data_func.mutate_section(new_section={
        'p1': [0, 200],
        'p2': [650, 200],
        'resolution': [650, 435]
    })

    # topology ----------------------------------------------------------------
    # get currently existing series in df & drop them inplace
    geo_data.series_df.drop(geo_data.series_df.index.values, inplace=True)
    # add new series
    geo_data_func.mutate_geo_model_serie(serie={
        'name': 'Strat_Series',
        'isfault': False,
        'order_series': 1
    })
    geo_data_func.mutate_geo_model_serie(serie={
        'name': 'Basement_Series',
        'isfault': False,
        'order_series': 0
    })

    # get current surfaces in df & drop them inplace
    geo_data.surfaces_df.drop(geo_data.surfaces_df.index.values, inplace=True)
    # add new surfaces
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'basement',
        'serie': 'Basement_Series',
        'order_surface': 0
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'rock1',
        'serie': 'Strat_Series',
        'order_surface': 1
    })

    # geo-data ----------------------------------------------------------------
    # get current surfaces-points in df & drop them inplace
    geo_data.surface_points_df.drop(
        geo_data.surface_points_df.index.values,
        inplace=True
    )
    # load surface-points from .csv
    input_data_surface_points = pd.read_csv(
        PROJECT_PATH + "/data/DATA/model2_surface_points.csv"
    )
    # add surface-points one by one
    for index, row in input_data_surface_points.iterrows():

        new_surface_point: td.SurfacePoint = {
            'id': str(uuid.uuid4()),
            'x': row['X'],
            'y': row['Y'],
            'z': row['Z'],
            'surface': row['formation'],
            'probdist': 'normal',
            'param1': 10,
            'param2': 1,
            'active': True,
            'locstr': f"{row['X']}{row['Y']}{row['Z']}"
        }
        geo_data_func.mutate_geo_model_surface_point(
            surface_point=new_surface_point)

    # get current orientations in df & drop them inplace
    geo_data.orientations_df.drop(
        geo_data.orientations_df.index.values,
        inplace=True
    )
    # load orientations from .csv
    input_data_orientations = pd.read_csv(
        PROJECT_PATH + "/data/DATA/model2_orientations.csv")
    # add orientations one by one  # HOTFIX
    print('HOTFIX: orientation bug in default model')
    geo_data.orientations_df.loc[0] = {
        'id': f"0",
        'x': 0,
        'y': 0,
        'z': 0,
        'azimuth': 0,
        'dip': 0,
        'polarity': 1,
        'surface': "x",
        'probdist': 'normal',
        'param1': 10,
        'param2': 1,
        'active': True,
        'loc-str': '000'
    }
    for index, row in input_data_orientations.iterrows():

        new_orientation: td.Orientation = {
            'id': str(uuid.uuid4()),
            'x': row['X'],
            'y': row['Y'],
            'z': row['Z'],
            'azimuth': row['azimuth'],
            'dip': row['dip'],
            'polarity': row['polarity'],
            'surface': row['formation'],
            'probdist': 'normal',
            'param1': 10,
            'param2': 1,
            'active': True,
            'locstr': f"{row['X']}{row['Y']}{row['Z']}"
        }
        geo_data_func.mutate_geo_model_orientation(orientation=new_orientation)

    geo_data.orientations_df.drop(0, inplace=True)


def setup_default_model_large():
    """Sets up a large fault model.

    Operates directly on the server geo_model object;
    """
    # meta-data ---------------------------------------------------------------
    # geo-model-extent
    geo_data_func.mutate_geo_model_extent(
        new_geo_model_extent={
            "x_min": 0,
            "x_max": 2000,
            "y_min": 0,
            "y_max": 2000,
            "z_min": 0,
            "z_max": 2000,
        })

    # geo-model-section
    geo_data_func.mutate_section(new_section={
        'p1': [0, 1000],
        'p2': [2000, 1000],
        'resolution': [200, 200]
    })

    # topology ----------------------------------------------------------------
    # get currently existing series in df & drop them inplace
    geo_data.series_df.drop(geo_data.series_df.index.values, inplace=True)
    # add new series

    geo_data_func.mutate_geo_model_serie(serie={
        'name': 'Strat_Series',
        'isfault': False,
        'order_series': 1
    })
    geo_data_func.mutate_geo_model_serie(serie={
        'name': 'Fault_Series',
        'isfault': True,
        'order_series': 0
    })

    # get current surfaces in df & drop them inplace
    geo_data.surfaces_df.drop(geo_data.surfaces_df.index.values, inplace=True)
    # add new surfaces
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'Main_Fault',
        'serie': 'Fault_Series',
        'order_surface': 0
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'Sandstone_2',
        'serie': 'Strat_Series',
        'order_surface': 1
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'Siltstone',
        'serie': 'Strat_Series',
        'order_surface': 2
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'Shale',
        'serie': 'Strat_Series',
        'order_surface': 3
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'Sandstone_1',
        'serie': 'Strat_Series',
        'order_surface': 4
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'basement',
        'serie': 'Strat_Series',
        'order_surface': 5
    })

    # geo-data ----------------------------------------------------------------
    # get current surfaces-points in df & drop them inplace
    geo_data.surface_points_df.drop(
        geo_data.surface_points_df.index.values,
        inplace=True
    )
    # load surface-points from .csv
    input_data_surface_points = pd.read_csv(
        PROJECT_PATH + "/data/DATA/simple_fault_model_points.csv"
    )
    # add surface-points one by one
    for index, row in input_data_surface_points.iterrows():

        new_surface_point: td.SurfacePoint = {
            'id': str(uuid.uuid4()),
            'x': row['X'],
            'y': row['Y'],
            'z': row['Z'],
            'surface': row['formation'],
            'probdist': 'normal',
            'param1': 10,
            'param2': 1,
            'active': True,
            'locstr': f"{row['X']}{row['Y']}{row['Z']}"
        }
        geo_data_func.mutate_geo_model_surface_point(
            surface_point=new_surface_point)

    # get current orientations in df & drop them inplace
    geo_data.orientations_df.drop(
        geo_data.orientations_df.index.values,
        inplace=True
    )

    # get current orientations in df & drop them inplace
    geo_data.orientations_df.drop(
        geo_data.orientations_df.index.values,
        inplace=True
    )
    # load orientations from .csv
    input_data_orientations = pd.read_csv(
        PROJECT_PATH + "/data/DATA/simple_fault_model_orientations.csv")
    # add orientations one by one  # HOTFIX
    print('HOTFIX: orientation bug in default model')
    geo_data.orientations_df.loc[0] = {
        'id': f"0",
        'x': 0,
        'y': 0,
        'z': 0,
        'azimuth': 0,
        'dip': 0,
        'polarity': 1,
        'surface': "x",
        'probdist': 'normal',
        'param1': 10,
        'param2': 1,
        'active': True,
        'loc-str': '000'
    }
    for index, row in input_data_orientations.iterrows():

        new_orientation: td.Orientation = {
            'id': str(uuid.uuid4()),
            'x': row['X'],
            'y': row['Y'],
            'z': row['Z'],
            'azimuth': row['azimuth'],
            'dip': row['dip'],
            'polarity': row['polarity'],
            'surface': row['formation'],
            'probdist': 'normal',
            'param1': 10,
            'param2': 1,
            'active': True,
            'locstr': f"{row['X']}{row['Y']}{row['Z']}"
        }
        geo_data_func.mutate_geo_model_orientation(orientation=new_orientation)

    geo_data.orientations_df.drop(0, inplace=True)


def setup_default_model():
    """Sets up a small fault model.

    Operates directly on the server geo_model object;
    """
    # meta-data ---------------------------------------------------------------
    # geo-model-extent
    geo_data_func.mutate_geo_model_extent(
        new_geo_model_extent={
            "x_min": 0,
            "x_max": 800,
            "y_min": 0,
            "y_max": 800,
            "z_min": 0,
            "z_max": 1000,
        })

    # geo-model-section
    geo_data_func.mutate_section(new_section={
        'p1': [0, 400],
        'p2': [800, 400],
        'resolution': [200, 200]
    })

    # topology ----------------------------------------------------------------
    # get currently existing series in df & drop them inplace
    geo_data.series_df.drop(geo_data.series_df.index.values, inplace=True)
    # add new series
    geo_data_func.mutate_geo_model_serie(serie={
        'name': 'Strat_Series',
        'isfault': False,
        'order_series': 1
    })
    geo_data_func.mutate_geo_model_serie(serie={
        'name': 'Basement_Series',
        'isfault': False,
        'order_series': 0
    })

    # get current surfaces in df & drop them inplace
    geo_data.surfaces_df.drop(geo_data.surfaces_df.index.values, inplace=True)
    # add new surfaces
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'basement',
        'serie': 'Basement_Series',
        'order_surface': 0
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'rock1',
        'serie': 'Strat_Series',
        'order_surface': 1
    })
    geo_data_func.mutate_geo_model_surface(surface={
        'name': 'rock2',
        'serie': 'Strat_Series',
        'order_surface': 2
    })

    # geo-data ----------------------------------------------------------------
    # get current surfaces-points in df & drop them inplace
    geo_data.surface_points_df.drop(
        geo_data.surface_points_df.index.values,
        inplace=True
    )
    # load surface-points from .csv
    input_data_surface_points = pd.read_csv(
        PROJECT_PATH + "/data/DATA/own_model_surface_points.csv"
    )
    # add surface-points one by one
    for index, row in input_data_surface_points.iterrows():

        new_surface_point: td.SurfacePoint = {
            'id': str(uuid.uuid4()),
            'x': row['X'],
            'y': row['Y'],
            'z': row['Z'],
            'surface': row['formation'],
            'probdist': 'normal',
            'param1': 10,
            'param2': 1,
            'active': True,
            'locstr': f"{row['X']}{row['Y']}{row['Z']}"
        }
        geo_data_func.mutate_geo_model_surface_point(
            surface_point=new_surface_point)

    # get current orientations in df & drop them inplace
    geo_data.orientations_df.drop(
        geo_data.orientations_df.index.values,
        inplace=True
    )
    # load orientations from .csv
    input_data_orientations = pd.read_csv(
        PROJECT_PATH + "/data/DATA/model2_orientations.csv")
    # add orientations one by one  # HOTFIX
    print('HOTFIX: orientation bug in default model')
    geo_data.orientations_df.loc[0] = {
        'id': f"0",
        'x': 0,
        'y': 0,
        'z': 0,
        'azimuth': 0,
        'dip': 0,
        'polarity': 1,
        'surface': "x",
        'probdist': 'normal',
        'param1': 10,
        'param2': 1,
        'active': True,
        'loc-str': '000'
    }
    for index, row in input_data_orientations.iterrows():

        new_orientation: td.Orientation = {
            'id': str(uuid.uuid4()),
            'x': row['X'],
            'y': row['Y'],
            'z': row['Z'],
            'azimuth': row['azimuth'],
            'dip': row['dip'],
            'polarity': row['polarity'],
            'surface': row['formation'],
            'probdist': 'normal',
            'param1': 10,
            'param2': 1,
            'active': True,
            'locstr': f"{row['X']}{row['Y']}{row['Z']}"
        }
        geo_data_func.mutate_geo_model_orientation(orientation=new_orientation)

    geo_data.orientations_df.drop(0, inplace=True)