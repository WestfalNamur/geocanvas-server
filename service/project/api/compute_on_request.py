import base64
import io
import os
from pathlib import Path
import copy


import jsonschema  # type: ignore
from flask import Blueprint, request, send_file
from flask_restful import Resource, Api  # type: ignore
from PIL import Image  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

import project.api.helper_functions as hfunc
import project.functions.realization_runs as real_run
import project.functions.post_processing as post_pro
import project.functions.realization_setup as real_setup
import project.functions.uq_runs as uq_runs
import project.data.data as geo_data
from project.gpmodel import geo_model

# Setup blueprints
compute_on_request_blueprint = Blueprint("compute_on_request", __name__)
api = Api(compute_on_request_blueprint)


PROJECT_PATH = str(Path(os.path.dirname(
    os.path.realpath(__file__))).parent)

###############################################################################
###                             SECTION                                     ###
###############################################################################


class SectionTops(Resource):

    def get(self):

        # run realization
        real_run.run_realization()

        # run realization
        real_run.run_realization()

        # calucalte surface tops
        B_tops = post_pro.compute_boolean_matrix_for_section_surface_top()
        section_coordinates = post_pro.compute_setction_grid_coordinates()
        tops_dict = post_pro.get_tops_coordinates(
            boolen_matrix_of_tops=B_tops,
            section_coordinates=section_coordinates
        )

        data = tops_dict
        message = "Meta data: geo-model-extent"
        return hfunc.success_response(
            data=data,
            message=message,
            code=200)


class SectionContours(Resource):

    def get(self):

        # run realization
        real_run.run_realization()

        # run realization
        real_run.run_realization()

        # calucalte surface contours
        contours = post_pro.compute_section_contours()

        # process for Konca.js line api
        contours_konva = post_pro.process_section_contours_for_konva(contours)

        message = "Meta data: geo-model-extent"
        return hfunc.success_response(
            data=contours_konva,
            message=message,
            code=200)


class EntropyMap(Resource):

    def get(self):

        mapping_object = real_setup.creat_mapping_object(
            series_df=geo_data.series_df,
            surfaces_df=geo_data.surfaces_df
        )

        entropy_map = uq_runs.calulate_entropy_map(
            geo_model=geo_model,
            n_realization=10,
            surface_points_original_df=geo_data.surface_points_df,
            orientations_original_df=geo_data.orientations_df,
            section=geo_data.section,
            mapping_object=mapping_object
        )

        message = "Meta data: 200x200 entropy map, flatten "
        return hfunc.success_response(
            data=entropy_map.flatten().tolist(),
            message=message,
            code=200)


class EntropyMapImg(Resource):

    def get(self):

        mapping_object = real_setup.creat_mapping_object(
            series_df=geo_data.series_df,
            surfaces_df=geo_data.surfaces_df
        )

        entropy_map = uq_runs.calulate_entropy_map(
            geo_model=geo_model,
            n_realization=10,
            surface_points_original_df=geo_data.surface_points_df,
            orientations_original_df=geo_data.orientations_df,
            section=geo_data.section,
            mapping_object=mapping_object
        )

        im = Image.fromarray(entropy_map * 255).rotate(270)
        im_bytes = im.tobytes()
        im_bytes_64 = base64.b64encode(im_bytes)
        im_bytes_64_str = str(im_bytes_64, 'utf8')

        im.convert('L').save(
            PROJECT_PATH
            + '/../../../geo-canvas_/src/utils/'
            + 'ie.jpg'
        )

        im.convert('L').save(PROJECT_PATH + 'ie.jpg')

        message = "Meta data: 200x200 entropy map, flatten "
        return hfunc.success_response(
            data=im_bytes_64_str,
            message=message,
            code=200)


class EntropyMapImage(Resource):

    def get(self):

        filename = PROJECT_PATH + 'ie.jpg'
        return send_file(filename, mimetype='image/jpg')


class OutcropImg(Resource):

    def get(self):

        filename = PROJECT_PATH + '/outcropa.jpg'
        print(' ')
        print('filename: ', filename)
        return send_file(filename, mimetype='image/jpg')

class MultiContours(Resource):

    def get(self):

        mapping_object = real_setup.creat_mapping_object(
            series_df=geo_data.series_df,
            surfaces_df=geo_data.surfaces_df
        )
        extent = list(geo_data.geo_model_extent.values())
        surface_points_original_df = geo_data.surface_points_df
        surface_points_copy = copy.deepcopy(geo_data.surface_points_df)


        contours = uq_runs.calc_multi_real_contours(
            surface_points_copy=surface_points_copy,
            surface_points_original_df=surface_points_copy,
            extent=extent,
            geo_model=geo_model,
            mapping_object=mapping_object
        )

        return hfunc.success_response(
            data=contours,
            message="Mutli realization of contours",
            code=200)

###############################################################################
###                             Register Ressources                         ###
###############################################################################
api.add_resource(
    SectionTops,
    '/geo-model/compute/section/tops'
)

api.add_resource(
    SectionContours,
    '/geo-model/compute/section/contours'
)

api.add_resource(
    EntropyMap,
    '/geo-model/compute/section/entropy'
)

api.add_resource(
    EntropyMapImg,
    '/geo-model/compute/section/entropy-img'
)

api.add_resource(
    EntropyMapImage,
    '/geo-model/compute/section/entropy-image'
)

api.add_resource(
    OutcropImg,
    '/geo-model/compute/section/outcrop-image'
)

api.add_resource(
    MultiContours,
    '/geo-model/compute/section/multi-contours'
)
