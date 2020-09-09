"""Test geo-model-data-api."""

import json

from project.tests.base import BaseTestCase
import project.data.data as process_data


class TestDataApiConfiguration(BaseTestCase):

    def test_geo_model_extent_get(self):
        response = self.client.get('/geo-model/data/geo-model-extent')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        extent = response_data['data']
        extent_keys = ['x_min', 'x_max', 'y_min', 'y_max', 'z_min', 'z_max']
        self.assertEqual(extent_keys, list(extent.keys()))
        self.assertTrue(all([
            isinstance(value, (int, float))
            for value in extent.values()
        ]))

    def test_geo_model_extent_put(self):
        with self.client:
            response = self.client.put(
                '/geo-model/data/geo-model-extent',
                data=json.dumps({
                    "x_min": 0,
                    "x_max": 42,
                    "y_min": 0,
                    "y_max": 42,
                    "z_min": 0,
                    "z_max": 42,
                }),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        updated_extent = {
            "x_min": 0,
            "x_max": 42,
            "y_min": 0,
            "y_max": 42,
            "z_min": 0,
            "z_max": 42
        }
        self.assertEqual(updated_extent, response_data['data'])

    def test_geo_model_section_get(self):
        response = self.client.get('/geo-model/data/geo-model-section')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        section = response_data['data']
        section_keys = ['p1', 'p2', 'resolution']
        self.assertEqual(section_keys, list(section.keys()))
        section_values = section['p1'] + section['p2'] + section['resolution']
        self.assertTrue(all([
            isinstance(value, (int, float))
            for value in section_values
        ]))

    def test_geo_model_section_put(self):
        with self.client:
            response = self.client.put(
                '/geo-model/data/geo-model-section',
                data=json.dumps({
                    'p1': [0, 21],
                    'p2': [42, 21],
                    'resolution': [100, 100]
                }),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        updated_section = {
            'p1': [0, 21],
            'p2': [42, 21],
            'resolution': [100, 100]
        }
        self.assertEqual(updated_section, response_data['data'])


class TestDataApiToplogicalData(BaseTestCase):

    def test_geo_model_series_get(self):
        response = self.client.get('/geo-model/data/geo-model-series')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_geo_model_series_put(self):
        new_series = {
            'name': 'NewSeries',
            'isfault': False,
            'order_series': 1}
        with self.client:
            response = self.client.put(
                '/geo-model/data/geo-model-series',
                data=json.dumps(new_series),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertIn(new_series, response_data['data'])
        process_data.series_df.drop('NewSeries', inplace=True)

    def test_geo_model_series_delete(self):
        serei_to_delete = {
            'name': 'SeriesToDelete',
            'isfault': False,
            'order_series': 42}
        process_data.series_df.loc['SeriesToDelete'] = serei_to_delete
        with self.client:
            response = self.client.delete(
                '/geo-model/data/geo-model-series',
                data=json.dumps(serei_to_delete),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertNotIn(serei_to_delete, response_data['data'])

    def test_geo_model_surfaces_get(self):
        response = self.client.get('/geo-model/data/geo-model-surfaces')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_geo_model_surfaces_put(self):
        new_surface = {
            'name': 'NewSurface',
            'serie': 'Strat_Series',
            'order_surface': 7}
        with self.client:
            response = self.client.put(
                '/geo-model/data/geo-model-surfaces',
                data=json.dumps(new_surface),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertIn(new_surface, response_data['data'])
        process_data.surfaces_df.drop('NewSurface', inplace=True)

    def test_geo_model_surfaces_delete(self):
        surfaces_to_delete = {
            'name': 'SurfaceToDelte',
            'serie': 'Strat_Series',
            'order_surface': 8}
        process_data.surfaces_df.loc['SurfaceToDelte'] = surfaces_to_delete
        with self.client:
            response = self.client.delete(
                '/geo-model/data/geo-model-surfaces',
                data=json.dumps(surfaces_to_delete),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(surfaces_to_delete, response_data['data'])


class TestDataApiGeologicalInputlData(BaseTestCase):

    def test_geo_model_surface_points__get(self):
        response = self.client.get('/geo-model/data/geo-model-surface-points')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_geo_model_surface_point_post(self):
        new_surface_point = {
            'x': 200,
            'y': 201,
            'z': 202,
            'surface': 'SomeSurface',
            'probdist': 'normal',
            'param1': 1,
            'param2': 0.1,
            'active': True,
            'locstr': '200201202'}
        with self.client:
            response = self.client.post(
                '/geo-model/data/geo-model-surface-points',
                data=json.dumps(new_surface_point),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['success'])
        self.assertIsInstance(response_data['data']['id'], str)
        process_data.surface_points_df.drop(
            response_data['data']['id'],
            inplace=True)

    def test_geo_model_surface_points_put(self):
        new_surface_point = {
            'id': 'b4ba235f-43c7-42a8-864e-b41960cb0ec7',
            'x': 100,
            'y': 101,
            'z': 102,
            'surface': 'SomeSurface',
            'probdist': 'normal',
            'param1': 1,
            'param2': 0.1,
            'active': True,
            'locstr': '100101102'}
        with self.client:
            response = self.client.put(
                '/geo-model/data/geo-model-surface-points',
                data=json.dumps(new_surface_point),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['success'])
        self.assertEqual(new_surface_point, response_data['data'])
        process_data.surface_points_df.drop(
            'b4ba235f-43c7-42a8-864e-b41960cb0ec7',
            inplace=True)

    def test_geo_model_surface_points_delete(self):
        surface_point_to_delte = {
            'id': 'f5bc8892-331c-4cf1-bc5b-846e8d2ffe40',
            'x': 100,
            'y': 101,
            'z': 102,
            'surface': 'SomeSurface',
            'probdist': 'normal',
            'param1': 1,
            'param2': 0.1,
            'active': True,
            'locstr': '100101102'}
        process_data.surface_points_df.loc[
            'f5bc8892-331c-4cf1-bc5b-846e8d2ffe40'
        ] = surface_point_to_delte
        with self.client:
            response = self.client.delete(
                '/geo-model/data/geo-model-surface-points',
                data=json.dumps(surface_point_to_delte),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertNotIn(surface_point_to_delte, response_data['data'])

    def test_geo_model_orientations_get(self):
        response = self.client.get('/geo-model/data/geo-model-orientations')
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)

    def test_geo_model_orientations_post(self):
        new_orientation = {
            'x': 100,
            'y': 101,
            'z': 102,
            'azimuth': 90,
            'dip': 90,
            'polarity': 90,
            'surface': 'SomeSurface',
            'probdist': 'normal',
            'param1': 1,
            'param2': 0.1,
            'active': True,
            'locstr': '100101102'}
        with self.client:
            response = self.client.post(
                '/geo-model/data/geo-model-orientations',
                data=json.dumps(new_orientation),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['success'])
        self.assertIsInstance(response_data['data']['id'], str)
        process_data.orientations_df.drop(
            response_data['data']['id'],
            inplace=True)

    def test_geo_model_orientations_put(self):
        new_orientation = {
            'id': '5189555351367804857314011177841044473',
            'x': 100,
            'y': 101,
            'z': 102,
            'azimuth': 90,
            'dip': 90,
            'polarity': 90,
            'surface': 'SomeSurface',
            'probdist': 'normal',
            'param1': 1,
            'param2': 0.1,
            'active': True,
            'locstr': '100101102'}
        with self.client:
            response = self.client.put(
                '/geo-model/data/geo-model-orientations',
                data=json.dumps(new_orientation),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertIn(new_orientation, response_data['data'])
        process_data.orientations_df.drop(
            '5189555351367804857314011177841044473',
            inplace=True)

    def test_geo_model_orientations_delete(self):
        orientation_to_delete = {
            'id': '100101102',
            'x': 100,
            'y': 101,
            'z': 102,
            'azimuth': 90,
            'dip': 90,
            'polarity': 90,
            'surface': 'SomeSurface',
            'probdist': 'normal',
            'param1': 1,
            'param2': 0.1,
            'active': True,
            'locstr': '100101102'}
        process_data.orientations_df.loc['100101102'] = orientation_to_delete
        with self.client:
            response = self.client.delete(
                '/geo-model/data/geo-model-orientations',
                data=json.dumps(orientation_to_delete),
                content_type="application/json",
            )
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['success'], True)
        self.assertNotIn(orientation_to_delete, response_data['data'])
