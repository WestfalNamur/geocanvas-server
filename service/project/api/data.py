"""Geo-model-data-pai."""


import jsonschema  # type: ignore
from flask import Blueprint, request
from flask_restful import Resource, Api  # type: ignore

import project.data.data as geo_model_data
import project.functions.data as geo_data_func
import project.types.json_schemes as schemes
import project.api.helper_functions as hfunc


# Setup blueprints
geo_model_data_blueprint = Blueprint("geo_mode_data", __name__)
api = Api(geo_model_data_blueprint)

###############################################################################
###                             Configuration                               ###
###############################################################################


class GeoModelExtent(Resource):

    def get(self):

        data = geo_model_data.geo_model_extent
        message = "Meta data: geo-model-extent"
        return hfunc.success_response(
            data=data,
            message=message,
            code=200)

    def put(self):

        put_data = request.get_json()
        if put_data:

            try:

                jsonschema.validate(
                    instance=put_data,
                    schema=schemes.geo_model_extent
                )

                try:

                    data, message = geo_data_func.mutate_geo_model_extent(
                        new_geo_model_extent=put_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=put_data
                )

        else:

            return hfunc.no_data()


class GeoModeSection(Resource):

    def get(self):

        data = geo_model_data.section
        message = "Meta data: geo-model-section"
        return hfunc.success_response(
            message=message,
            data=data,
            code=200)

    def put(self):

        put_data = request.get_json()
        if put_data:

            try:

                jsonschema.validate(
                    instance=put_data,
                    schema=schemes.geo_model_section
                )

                try:

                    data, message = geo_data_func.mutate_section(
                        new_section=put_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=put_data
                )

        else:

            return hfunc.no_data()


###############################################################################
###                             Topology data                               ###
###############################################################################

class GeoModelSereis(Resource):

    def get(self):

        data = geo_model_data.series_df.to_dict('records')
        return hfunc.success_response(
            data=data,
            message='Geo-model-series',
            code=200)

    def put(self):

        put_data = request.get_json()
        if put_data:

            try:

                jsonschema.validate(
                    instance=put_data,
                    schema=schemes.geo_model_serie
                )

                try:

                    data, message = geo_data_func.mutate_geo_model_serie(
                        serie=put_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=put_data
                )

        else:

            return hfunc.no_data()

    def delete(self):

        delete_data = request.get_json()
        if delete_data:

            try:

                jsonschema.validate(
                    instance=delete_data,
                    schema=schemes.geo_model_serie
                )

                try:

                    data, message = geo_data_func.delete_geo_model_sereie(
                        serie=delete_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=delete_data
                )

        else:

            return hfunc.no_data()


class GeoModelSurfaces(Resource):

    def get(self):

        data = geo_model_data.surfaces_df.to_dict('records')
        return hfunc.success_response(
            data=data,
            message='Geo-model-surfaces',
            code=200)

    def put(self):

        put_data = request.get_json()
        if put_data:

            try:

                jsonschema.validate(
                    instance=put_data,
                    schema=schemes.geo_model_surface
                )

                try:

                    data, message = geo_data_func.mutate_geo_model_surface(
                        surface=put_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=put_data
                )

        else:

            return hfunc.no_data()

    def delete(self):

        delete_data = request.get_json()
        if delete_data:

            try:

                jsonschema.validate(
                    instance=delete_data,
                    schema=schemes.geo_model_surface
                )

                try:

                    data, message = geo_data_func.delete_geo_model_surface(
                        surface=delete_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=delete_data
                )

        else:

            return hfunc.no_data()


###############################################################################
###                         Geological input data                           ###
###############################################################################

class GeoModelSurfacesPoints(Resource):

    def get(self):

        data = geo_model_data.surface_points_df.to_dict('records')
        return hfunc.success_response(
            data=data,
            message='Geo-model-surfaces-points',
            code=200)

    def post(self):

        post_data = request.get_json()
        if post_data:

            try:

                jsonschema.validate(
                    instance=post_data,
                    schema=schemes.geo_model_surface_point_new
                )

                try:

                    data, message = geo_data_func.add_geo_model_surface_point(
                        surface_point_new=post_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=post_data
                )

        else:

            return hfunc.no_data()

    def put(self):

        put_data = request.get_json()
        if put_data:

            try:

                jsonschema.validate(
                    instance=put_data,
                    schema=schemes.geo_model_surface_point
                )

                try:

                    data, message = geo_data_func.mutate_geo_model_surface_point(
                        surface_point=put_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=put_data
                )

        else:

            return hfunc.no_data()

    def delete(self):

        delete_data = request.get_json()
        if delete_data:

            try:

                jsonschema.validate(
                    instance=delete_data,
                    schema=schemes.geo_model_surface_point
                )

                try:

                    data, message = geo_data_func.delete_geo_model_surface_point(
                        surface_point=delete_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=delete_data
                )

        else:

            return hfunc.no_data()


class GeoModelOrientations(Resource):

    def get(self):

        data = geo_model_data.orientations_df.to_dict('records')
        return hfunc.success_response(
            data=data,
            message='Geo-model-sorientations',
            code=200)

    def post(self):

        post_data = request.get_json()
        if post_data:

            try:

                jsonschema.validate(
                    instance=post_data,
                    schema=schemes.geo_model_orientation_new
                )

                try:

                    data, message = geo_data_func.add_geo_model_orientation(
                        orientation_new=post_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=post_data
                )

        else:

            return hfunc.no_data()

    def put(self):

        put_data = request.get_json()
        if put_data:

            try:

                jsonschema.validate(
                    instance=put_data,
                    schema=schemes.geo_model_orientation
                )

                try:

                    data, message = geo_data_func.mutate_geo_model_orientation(
                        orientation=put_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=put_data
                )

        else:

            return hfunc.no_data()

    def delete(self):

        delete_data = request.get_json()
        if delete_data:

            try:

                jsonschema.validate(
                    instance=delete_data,
                    schema=schemes.geo_model_orientation
                )

                try:

                    data, message = geo_data_func.delete_geo_model_orientation(
                        orientation=delete_data
                    )

                    return hfunc.success_response(
                        message=message,
                        data=data,
                        code=200
                    )

                except Exception as err:

                    return hfunc.value_err_response(err=err)

            except jsonschema.exceptions.ValidationError as err:

                return hfunc.schema_error_response(
                    err=err,
                    data=delete_data
                )

        else:

            return hfunc.no_data()


###############################################################################
###                             Register Ressources                         ###
###############################################################################
api.add_resource(
    GeoModelExtent,
    '/geo-model/data/geo-model-extent'
)
api.add_resource(
    GeoModeSection,
    '/geo-model/data/geo-model-section'
)

api.add_resource(
    GeoModelSereis,
    '/geo-model/data/geo-model-series'
)
api.add_resource(
    GeoModelSurfaces,
    '/geo-model/data/geo-model-surfaces'
)

api.add_resource(
    GeoModelSurfacesPoints,
    '/geo-model/data/geo-model-surface-points'
)
api.add_resource(
    GeoModelOrientations,
    '/geo-model/data/geo-model-orientations'
)
