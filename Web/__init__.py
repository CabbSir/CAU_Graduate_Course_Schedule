from flask import Flask, render_template
from .config import config
from . import models, routes


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.debug = True # @TODO 上线更改
    models.init_app(app)
    routes.init_app(app)

    @app.errorhandler(404)
    def handle_404_error(e):
        return render_template("404.html"), 404

    return app
