# service/manage.py
"""Project manage file."""

import sys
import unittest

from mypy import api as mypy_api
from flask.cli import FlaskGroup

from project import create_app

# Typechecking /project
mypy_result = mypy_api.run(['project/'])
if mypy_result[2]:
    print('Error during type-checking. Script execution stoped.')
    print(' ')
    print(mypy_result[0])
    print(mypy_result[1])
    sys.exit()


# Run app process
app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def test():
    """Runs the tests and typechecking without code coverage

    Order: Api, Pipelines
    """
    print('DATA API')
    api_tests_data = unittest.TestLoader().discover(
        'project/tests', pattern='test_api*.py')
    api_result_data = unittest.TextTestRunner(verbosity=2).run(api_tests_data)
    print('DEFAULTS')
    defaults_tests_data = unittest.TestLoader().discover(
        'project/tests', pattern='test_default*.py')
    defaults_result_data = unittest.TextTestRunner(
        verbosity=2).run(defaults_tests_data)
    print('COMPUTES')
    computes_tests_data = unittest.TestLoader().discover(
        'project/tests', pattern='test_compute*.py')
    computes_result_data = unittest.TextTestRunner(
        verbosity=2).run(computes_tests_data)
    print('DATA API', api_result_data)
    print('DEFAULTS', defaults_result_data)
    print('COMPUTES', computes_result_data)
    sys.exit()


@cli.command()
def testdata():
    """Runs the tests and typechecking without code coverage."""
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    tests = unittest.TestLoader().discover('project/tests', pattern='test_api*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command()
def testdefaultmodel():
    """Runs the tests and typechecking without code coverage."""
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DEFAULTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    tests = unittest.TestLoader().discover(
        'project/tests', pattern='test_default*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command()
def testcomputes():
    """Runs the tests and typechecking without code coverage."""
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ COMPUTES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    tests = unittest.TestLoader().discover(
        'project/tests', pattern='test_compute*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == '__main__':
    cli()
