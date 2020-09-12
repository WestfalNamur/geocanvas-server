import base64
import io
import os
from pathlib import Path

import jsonschema  # type: ignore
from flask import Blueprint, request, send_file
from flask_restful import Resource, Api  # type: ignore
from PIL import Image  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

import project.api.helper_functions as hfunc
import project.functions.realization_runs as real_run
import project.functions.post_processing as post_pro
import project.functions.realization_setup as real_setup
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