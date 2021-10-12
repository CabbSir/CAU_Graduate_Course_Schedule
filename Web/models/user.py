from time import time

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    j_name = db.Column(db.String(255), nullable=True)
    j_passwd = db.Column(db.String(255), nullable=True)
    last_login_ip = db.Column(db.String(50), nullable=False)
    last_login_time = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.String(10), nullable=False, default=time())
    modify_time = db.Column(db.String(10), nullable=False, default=time())
