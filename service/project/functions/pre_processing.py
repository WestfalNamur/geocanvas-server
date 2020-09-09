from typing import Tuple

import pandas as pd  # type: ignore
import project.types.typed_dicts as td


def format_geological_input_data(
    surface_points_df: pd.DataFrame,
    orientations_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Format and filter geological input data.

    Selects active process-model-data and formats them into a Gempy friendly
    format.

    1. SurfacePoints
        Filter
        Format
    2. Orientations
        Filter
        Format

    Args:
        series_df: DataFrame = containing series data of td.Serie type. 
        surfaces_df: DataFrame = containing surfaces data of td.Serie type.

    Returns:
        geo_model_input_surface_points_df: DataFrame = geo_model surface points
            input.
        geo_model_input_orientations_df: DataFrame = geo_model orientations
            input.
    """

    # SurfacePoints
    # Filter
    geo_model_input_surface_points_df = surface_points_df[[
        'x',
        'y',
        'z',
        'surface'
    ]]
    # Format
    geo_model_input_surface_points_df.columns = [
        'X',
        'Y',
        'Z',
        'surface'
    ]
    # Orientations
    # Filter
    geo_model_input_orientations_df = orientations_df[[
        'x',
        'y',
        'z',
        'dip',
        'azimuth',
        'polarity',
        'surface'
    ]]
    # Format
    geo_model_input_orientations_df.columns = [
        'X',
        'Y',
        'Z',
        'dip',
        'azimuth',
        'polarity',
        'formation'
    ]

    # Return
    return (geo_model_input_surface_points_df, geo_model_input_orientations_df)
