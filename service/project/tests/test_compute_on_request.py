import json
from PIL import Image  # type: ignore
import os
from pathlib import Path

import numpy as np  # type: ignore

from project.tests.base import BaseTestCase
import project.gpmodel.default_model as def_mod
import project.functions.realization_runs as real_run
import project.functions.post_processing as post_pro


PROJECT_PATH = str(Path(os.path.dirname(
    os.path.realpath(__file__))).parent)


class TestRealizationRuns(BaseTestCase):

    def test_surface_tops_snapshot_small(self):

        # small default mode
        def_mod.setup_default_model_small()

        # run realization
        real_run.run_realization()

        # calucalte surface tops
        B_tops = post_pro.compute_boolean_matrix_for_section_surface_top()
        section_coordinates = post_pro.compute_setction_grid_coordinates()
        tops_dict = post_pro.get_tops_coordinates(
            boolen_matrix_of_tops=B_tops,
            section_coordinates=section_coordinates
        )

        # plot and savefig.
        post_pro.plot_tops(tops_dict, 'small_model_tops', 0, 1000, 0, 1000)

        # compare images
        img1 = Image.open(
            PROJECT_PATH + '/tests/snapshots/' + 'small_model_tops' + '.png'
        )
        img2 = Image.open(
            PROJECT_PATH
            + '/tests/snapshots/'
            + 'small_model_tops_prototype'
            + '.png'
        )
        diff = np.fabs(np.subtract(img2, img1))
        self.assertTrue(np.sum(diff) == 0)

    def test_surface_tops_snapshot_large(self):

        # small default mode
        def_mod.setup_default_model_large()

        # run realization
        real_run.run_realization()

        # calucalte surface tops
        B_tops = post_pro.compute_boolean_matrix_for_section_surface_top()
        section_coordinates = post_pro.compute_setction_grid_coordinates()
        tops_dict = post_pro.get_tops_coordinates(
            boolen_matrix_of_tops=B_tops,
            section_coordinates=section_coordinates
        )

        # plot and savefig.
        post_pro.plot_tops(tops_dict, 'large_model_tops', 0, 2000, 0, 2000)

        # compare images
        img1 = Image.open(
            PROJECT_PATH + '/tests/snapshots/' + 'large_model_tops' + '.png'
        )
        img2 = Image.open(
            PROJECT_PATH
            + '/tests/snapshots/'
            + 'large_model_tops_prototype'
            + '.png'
        )
        diff = np.fabs(np.subtract(img2, img1))
        self.assertTrue(np.sum(diff) == 0)
