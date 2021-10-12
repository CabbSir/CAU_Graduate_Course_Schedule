from flask import Blueprint

page_bp = Blueprint('interface_bp', __name__)


@page_bp.route('/')
def index():
    return "Hello World!"