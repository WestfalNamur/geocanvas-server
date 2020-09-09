""" Flask app factory for geo-model-app-process. """


from flask import Flask
from flask_cors import CORS  # type: ignore


# instantiate the extensions
cors = CORS()


def create_app():
    """
    App factory

    Each geo-model is a singel process. Therfore only one mide
    """

    # instantiate the app
    app = Flask(__name__)

    # set up extension
    cors.init_app(app)  # allow CORS

    # import blueprints
    from project.api.data import geo_model_data_blueprint
    from project.api.compute_on_request import compute_on_request_blueprint

    # register blueprints
    app.register_blueprint(geo_model_data_blueprint)
    app.register_blueprint(compute_on_request_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
