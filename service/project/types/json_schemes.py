# service/project/api/jsonschemes.py
""" JSON schemas for RESTapi. """

# config schemes --------------------------------------------------------------
geo_model_extent = {
    'type': 'object',
    'properties': {
        'x_min': {'type': 'integer'},
        'x_max': {'type': 'integer'},
        'y_min': {'type': 'integer'},
        'y_max': {'type': 'integer'},
        'z_min': {'type': 'integer'},
        'z_max': {'type': 'integer'},
    },
    'required': ['x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max'],
}

geo_model_section = {
    'type': 'object',
    'properties': {
        'p1': {'type': 'array', 'items': {'type': 'number'}},
        'p2': {'type': 'array', 'items': {'type': 'number'}},
        'resolution': {'type': 'array', 'items': {'type': 'number'}},
    },
    'required': ['p1', 'p2', 'resolution'],
}

# topological data ------------------------------------------------------------
geo_model_serie = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'isfault': {'type': 'boolean'},
        'order_series': {'type': 'integer'}
    },
    'required': ['name', 'isfault'],
}

geo_model_surface = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'serie': {'type': 'string'},
        'order_surface': {'type': 'integer'}
    },
    'required': ['name', 'serie'],
}


# geological input data -------------------------------------------------------
geo_model_surface_point_new = {
    'type': 'object',
    'properties': {
        'x': {'type': 'number'},
        'y': {'type': 'number'},
        'z': {'type': 'number'},
        'surface': {'type': 'string'},
        'probdist': {'type': 'string'},
        'param1': {'type': 'number'},
        'param2': {'type': 'number'},
        'active': {'type': 'boolean'},
        'locstr': {'type': 'string'}
    },
    'required': [
        'x',
        'y',
        'z',
        'surface',
        'probdist',
        'param1',
        'param2',
        'active',
        'locstr'
    ],
}

geo_model_surface_point = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'x': {'type': 'number'},
        'y': {'type': 'number'},
        'z': {'type': 'number'},
        'surface': {'type': 'string'},
        'probdist': {'type': 'string'},
        'param1': {'type': 'number'},
        'param2': {'type': 'number'},
        'active': {'type': 'boolean'},
        'locstr': {'type': 'string'}
    },
    'required': [
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
    ],
}

geo_model_orientation_new = {
    'type': 'object',
    'properties': {
        'x': {'type': 'number'},
        'y': {'type': 'number'},
        'z': {'type': 'number'},
        'azimuth': {'type': 'number'},
        'dip': {'type': 'number'},
        'polarity': {'type': 'number'},
        'surface': {'type': 'string'},
        'probdist': {'type': 'string'},
        'param1': {'type': 'number'},
        'param2': {'type': 'number'},
        'active': {'type': 'boolean'},
        'locstr': {'type': 'string'}
    },
    'required': [
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
    ],
}

geo_model_orientation = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'x': {'type': 'number'},
        'y': {'type': 'number'},
        'z': {'type': 'number'},
        'azimuth': {'type': 'number'},
        'dip': {'type': 'number'},
        'polarity': {'type': 'number'},
        'surface': {'type': 'string'},
        'probdist': {'type': 'string'},
        'param1': {'type': 'number'},
        'param2': {'type': 'number'},
        'active': {'type': 'boolean'},
        'locstr': {'type': 'string'}
    },
    'required': [
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
    ],
}
