from flask import Blueprint

interface_bp = Blueprint('interface_bp', __name__)


@interface_bp.route('/')
def index():
    return "Hello World!"