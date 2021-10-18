from flask import Flask, render_template
from .config import config
from . import models, routes


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.debug = False
    models.init_app(app)
    routes.init_app(app)

    @app.errorhandler(404)
    def handle_404_error(e):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host = '0.0.0.0', port = 5000)
