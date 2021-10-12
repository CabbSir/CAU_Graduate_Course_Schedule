from .page import page_bp
from .interface import interface_bp


def init_app(app):
    app.register_blueprint(page_bp)
    app.register_blueprint(interface_bp)
