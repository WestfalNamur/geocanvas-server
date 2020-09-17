import copy

import numpy as np  # type: ignore
import gempy as gp  # type: ignore
import scipy.stats as ss  # type: ignore
from skimage import measure  # type: ignore


def manipulate_surface_points_inplace(surface_points_copy, surface_points_original_df):
    """Manipulates the surface_points_copy dataframe.

        Samples X, Y, Z values form the original DataFrame and thier
        respective distribution types and parameters.\
        Potential update:
            - Sampling parameter per axis i.e. param1_x, param1_y, ...
            - Diffenrent sampling types i.e. normal, uniformal, ...

        Args:
            surface_points_copy: DataFrame = copy of the original geological
                input data surface-points DataFrame.
            surface_points_original_df: DataFrame = original geological input data
                surface-points DataFrame.
    """

    surface_points_copy['X'] = ss.norm.rvs(
        loc=surface_points_original_df['x'].values,
        scale=surface_points_original_df['param1'].values)
    surface_points_copy['Y'] = ss.norm.rvs(
        loc=surface_points_original_df['y'].values,
        scale=surface_points_original_df['param1'].values)
    surface_points_copy['Z'] = ss.norm.rvs(
        loc=surface_points_original_df['z'].values,
        scale=surface_points_original_df['param1'].values)


def run_realizations(
    geo_model,
    n_realizations,
    surface_points_original_df,
    orientations_original_df,
    section,
    mapping_object
):
    """Runs x ralizations"""

    # Copy geological input data to manipulate per realization.
    surface_points_copy = copy.deepcopy(surface_points_original_df)

    # Storage for calucalted ralizations
    list_section_data = []
    lst_boolen_tops_dicts = {}

    # Calculate realizations
    for i in range(n_realizations):

        print(f'Realization: {i}')

        # manipulate surface_points_copy in place
        manipulate_surface_points_inplace(
            surface_points_copy=surface_points_copy,
            surface_points_original_df=surface_points_original_df)

        # Set manipulated surface points
        geo_model.set_surface_points(
            surface_points_copy, update_surfaces=False)
        gp.map_series_to_surfaces(
            geo_model=geo_model,
            mapping_object=mapping_object
        )

        # update to interpolator
        geo_model.update_to_interpolator()
        # Compute solution
        # TODO: Fix bug!
        # till here: until 90.1 ms for 1 realizations
        # 213 m with 2x gp.compute_model()
        try:
            gp.compute_model(model=geo_model)
        except ValueError as err:
            print('ValueError')
            # Append last working realization
            list_section_data.append(geo_model
                                     .solutions
                                     .sections[0][0]
                                     .reshape(section['resolution'])
                                     )
        # collect extracted section data
        list_section_data.append(geo_model
                                 .solutions
                                 .sections[0][0]
                                 .reshape(section['resolution'])
                                 )

    return list_section_data


def process_list_section_data(list_section_data):

    # Process results Stack results
    section_data_stack = np.round(np.dstack(list_section_data))

    # Get lithologies in stack
    lithology_ids = np.unique(section_data_stack)

    return section_data_stack, lithology_ids


def count_lithology_occurrences_over_realizations(
        section_data_stack,
        lithology_ids,
        section
):

    count_array = np.empty((
        section['resolution'][0],
        section['resolution'][1],
        len(lithology_ids)))

    for index, lithology in enumerate(lithology_ids):

        count_array[:, :, index] = np.sum((
            section_data_stack == lithology).astype(int), axis=2)

    return count_array


def calculate_information_entropy(count_array, n_realizations):

    # Calculate information entropy
    probability_array = count_array / n_realizations
    return ss.entropy(probability_array, axis=2)


def calulate_entropy_map(
    geo_model,
    n_realization,
    surface_points_original_df,
    orientations_original_df,
    section,
    mapping_object
):

    list_section_data = run_realizations(
        geo_model=geo_model,
        n_realizations=n_realization,
        surface_points_original_df=surface_points_original_df,
        orientations_original_df=orientations_original_df,
        section=section,
        mapping_object=mapping_object
    )

    section_data_stack, lithology_ids = process_list_section_data(
        list_section_data=list_section_data
    )

    count_array = count_lithology_occurrences_over_realizations(
        section_data_stack=section_data_stack,
        lithology_ids=lithology_ids,
        section=section
    )

    entropy_map = calculate_information_entropy(
        count_array=count_array,
        n_realizations=n_realization
    )

    return entropy_map


def calc_multi_real_contours(
    surface_points_copy,
    surface_points_original_df,
    extent,
    geo_model,
    mapping_object
    ):

    contour_lst = {}
    for real_i in range(10):

        # maniupulate surface points for realization
        manipulate_surface_points_inplace(
            surface_points_copy,
            surface_points_original_df
        )

        # correct values outside the model boundaries
        for XYZ_i in ['X', 'Y', 'Z']:

            if XYZ_i == 'X':
                surface_points_copy['X'][surface_points_copy['X'] < extent[0]] = extent[0]
                surface_points_copy['X'][surface_points_copy['X'] > extent[1]] = extent[1]

            if XYZ_i == 'Y':
                surface_points_copy['Y'][surface_points_copy['Y'] < extent[2]] = extent[2]
                surface_points_copy['Y'][surface_points_copy['Y'] > extent[3]] = extent[3]

            if XYZ_i == 'Z':
                surface_points_copy['Z'][surface_points_copy['Z'] < extent[4]] = extent[4]
                surface_points_copy['Z'][surface_points_copy['Z'] > extent[5]] = extent[5]

        # Set manipulated surface points
        geo_model.set_surface_points(surface_points_copy, update_surfaces=False)
        gp.map_series_to_surfaces(
            geo_model=geo_model,
            mapping_object=mapping_object
        )

        # update to interpolator
        geo_model.update_to_interpolator()

        # compute realization
        try:
            gp.compute_model(model=geo_model, sort_surfaces=False)
            print(f'Realization {real_i} computed.')
        except:
            print(f'Error in realization {real_i}.')
            pass

        # get contours
        # get start and end of section in grid scalar vals array
        arr_len_0, arr_len_n = geo_model.grid.sections.get_section_args('section')

        # CAUTION: if more section present they have to be indexexed accrodingly;
        # get shape of section  # 1st and only one here as only one section present.
        section_shape = geo_model.grid.sections.resolution[0]
        # extract section scalar values from solutions.sections# [series,serie_pos_0:serie_pos_n]
        section_scalar_field_values = geo_model.solutions.sections[1][:,arr_len_0:arr_len_n]

        # number scalar field blocks
        n_scalar_field_blocks = section_scalar_field_values.shape[0]
        # creat a dictionary to assemble all scalat field boolen matrices shifts
        # extract transition towards current level
        contours = {}
        for block_i in range(n_scalar_field_blocks):

            # number scalar field blocks
            n_scalar_field_blocks = section_scalar_field_values.shape[0]
            # creat a dictionary to assemble all scalat field boolen matrices shifts
            # extract transition towards current level
            contours = {}
            for scalar_field_block_i in range(n_scalar_field_blocks):

                # scalarfield values of scalarfield_block-i
                block = section_scalar_field_values[scalar_field_block_i, :]
                # ??? level
                level = geo_model.solutions.scalar_field_at_surface_points[scalar_field_block_i][np.where(
                    geo_model.solutions.scalar_field_at_surface_points[scalar_field_block_i] != 0)]
                # ??? calulcate scalarfeild levels
                levels = np.insert(level, 0, block.max())
                # extract and reshape scalar field values
                scalar_field = block.reshape(section_shape)
                # loop over levels to extract tops present within current scalar field
                for lvl_i in range(len(levels)):

                    # get top name
                    top_name = geo_model.surfaces.df['surface'][lvl_i]
                    # Find contour
                    contour = measure.find_contours(scalar_field, levels[lvl_i])
                    # add contour to contoures if there are some
                    if len(contour) > 0:

                        contour_lst[f'real_{real_i}_{top_name}'] = contour[0].flatten().tolist()

    return contour_lst
        