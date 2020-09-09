import json

from project.tests.base import BaseTestCase
import project.gpmodel.default_model as def_mod
import project.data.data as geo_data


class TestSetupOfDefaultModel(BaseTestCase):

    def test_small_default_model(self):

        # setup default model small
        def_mod.setup_default_model_small()

        # section
        self.assertEqual(
            [0, 500],
            geo_data.section['p1']
        )
        self.assertEqual(
            [1000, 500],
            geo_data.section['p2']
        )
        self.assertEqual(
            [200, 200],
            geo_data.section['resolution']
        )
        # extent
        self.assertEqual(
            list(geo_data.geo_model_extent.values()),
            [0, 1000, 0, 1000, 0, 1000]
        )

        # series
        lst_should_be = ['Basement_Series', 'Strat_Series']
        lst_series_names = geo_data.series_df['name'].to_list()
        set_compare_series = set(lst_should_be) & set(lst_series_names)
        self.assertIs(len(set_compare_series), 2)
        # surfaces
        lst_should_be = ['basement', 'rock1', 'rock2']
        lst_surfaces_names = geo_data.surfaces_df['name'].to_list()
        set_compare_surfaces = set(lst_should_be) & set(lst_surfaces_names)
        self.assertIs(len(set_compare_surfaces), 3)

        # surface_points
        self.assertEqual(geo_data.surface_points_df.shape, (36, 10))
        # orintations
        self.assertEqual(geo_data.orientations_df.shape, (2, 13))

    def test_large_default_model(self):

        # setup default model large
        def_mod.setup_default_model_large()

        # section
        self.assertEqual(
            [0, 1000],
            geo_data.section['p1']
        )
        self.assertEqual(
            [2000, 1000],
            geo_data.section['p2']
        )
        self.assertEqual(
            [200, 200],
            geo_data.section['resolution']
        )
        # extent
        self.assertEqual(
            list(geo_data.geo_model_extent.values()),
            [0, 2000, 0, 2000, 0, 2000]
        )

        # series
        lst_should_be = ['Fault_Series', 'Strat_Series']
        lst_series_names = geo_data.series_df['name'].to_list()
        set_compare_series = set(lst_should_be) & set(lst_series_names)
        self.assertIs(len(set_compare_series), 2)
        # surfaces
        lst_should_be = [
            'Main_Fault',
            'Sandstone_2',
            'Siltstone',
            'Shale',
            'Sandstone_1',
            'basement'
        ]
        lst_surfaces_names = geo_data.surfaces_df['name'].to_list()
        set_compare_surfaces = set(lst_should_be) & set(lst_surfaces_names)
        self.assertIs(len(set_compare_surfaces), 6)

        # surface_points
        self.assertEqual(geo_data.surface_points_df.shape, (57, 10))
        # orintations
        self.assertEqual(geo_data.orientations_df.shape, (3, 13))
