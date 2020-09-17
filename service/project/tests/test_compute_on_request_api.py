import json
from PIL import Image  # type: ignore
import os
import numpy as np  # type: ignore
from pathlib import Path
import matplotlib.pyplot as plt  # type: ignore
import base64

from project.tests.base import BaseTestCase
import project.functions.post_processing as post_pro
import project.gpmodel.default_model as def_mod

PROJECT_PATH = str(Path(os.path.dirname(
    os.path.realpath(__file__))).parent)


class TestDataApiConfiguration(BaseTestCase):

    def test_compute_section_tops_get(self):

        def_mod.setup_default_model()

        response = self.client.get('/geo-model/compute/section/tops')
        response_data = json.loads(response.data.decode())

        tops_dict = response_data['data']
        post_pro.plot_tops(
            tops_coordinates=tops_dict,
            xmin=0,
            xmax=800,
            ymin=0,
            ymax=1000,
            name='compute_section_tops'
        )

        # compare images
        img1 = Image.open(
            PROJECT_PATH
            + '/tests/snapshots/'
            + 'compute_section_tops'
            + '.png'
        )
        img2 = Image.open(
            PROJECT_PATH
            + '/tests/snapshots/'
            + 'compute_section_tops_prototype'
            + '.png'
        )
        diff = np.fabs(np.subtract(img2, img1))
        self.assertTrue(np.sum(diff) == 0)

        self.assertEqual(response.status_code, 200)

    def test_compute_contours(self):

        def_mod.setup_default_model()

        response = self.client.get('/geo-model/compute/section/contours')
        response_data = json.loads(response.data.decode())

        self.assertEqual(
            ['rock1', 'rock2'],
            list(response_data['data'].keys())
        )

    def _test_get_entropy_map(self):

        # setup default model
        def_mod.setup_default_model()
        # make request and load response data
        response = self.client.get('/geo-model/compute/section/entropy')
        response_data = json.loads(response.data.decode())
        # process response to ndarry in right shape (sections shape)
        entropy_map_flattened = response_data['data']
        entropy_map_ndarray = np.array(entropy_map_flattened).reshape(200, 200)
        # save for check
        fig = plt.figure()
        plt.imshow(entropy_map_ndarray)
        fig.savefig(
            PROJECT_PATH
            + '/tests/snapshots/'
            + 'entropy_map_new'
            + '.png'
        )
        self.assertEqual(response.status_code, 200)

    def _test_get_entropy_map_img(self):

        # setup default model
        def_mod.setup_default_model()
        # make request and load response data
        response = self.client.get('/geo-model/compute/section/entropy-img')
        response_data = json.loads(response.data.decode())
        im_bytes_64_str = response_data['data']
        im_bytes_64 = bytes(im_bytes_64_str, 'utf8')
        im_bytes = base64.b64decode(im_bytes_64)
        im = Image.frombytes('F', (200, 200), im_bytes)
        im.show()

    def test_get_mulit_real_contours(self):

        # setup default model
        def_mod.setup_default_model()
        response = self.client.get('/geo-model/compute/section/multi-contours')
        response_data = json.loads(response.data.decode())
        contours = response_data['data']
        self.assertEqual(response.status_code, 200)
