# service/project/gpmodel/__init__.py
"""  Gempy model instance. """

import gempy as gp  # type: ignore
from project.gpmodel.default_model import setup_default_model_small
# instantiate the geo_model
geo_model = gp.create_model("BaseModel")

# defautl data
geo_model = gp.init_data(
    geo_model,
    extent=[0, 1000, 0, 1000, 0, 1000],
    resolution=[10, 10, 10]
)

# setup interpolator
gp.set_interpolation_data(
    geo_model,
    compile_theano=True,
    theano_optimizer='fast_run',
)

# setup default model
setup_default_model_small()