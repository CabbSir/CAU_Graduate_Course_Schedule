from flask import Blueprint, render_template

page_bp = Blueprint('page_bp', __name__)


@page_bp.route('/')
def index():
    return "Hello World!"


@page_bp.route('/login')
def login():
    return render_template("login.html")


@page_bp.route('/app')
def app():
    return render_template("app.html")


@page_bp.route('/contact')
def contact():
    return render_template("contact.html")


@page_bp.route('/disclaimer')
def disclaimer():
    return render_template("disclaimer.html")


@page_bp.route('/schedule')
def schedule():
    return render_template("schedule.html")


@page_bp.route('/user_info')
def user_info():
    return render_template("user_info.html")