# src/api/helper_functions.py
"""Functions to be inlcuded in multiple api ressources."""


def success_response(message=None, data=None, code=200):
    """Response for successfull requests."""

    response_object = {
        'success': True,
        'message': message,
        'data': data
    }
    return response_object, code


def no_data():
    """Response when required JSON is missing."""

    response_object = {
        "success": False,
        "error": f'Data is missing.'
    }
    return response_object, 400


def schema_error_response(err, data=None):
    """ Returns a error statuts code and an according response object for json
    validation errors.
    """

    response_object = {
        "success": False,
        "error": err.message,
        'data': data
    }
    return response_object, 400


def value_err_response(err, data=None):
    """
    Returns error status code and according response object for value errors.
    """

    response_object = {
        "success": False,
        "error": str(err),
        'data': data
    }
    return response_object, 400
