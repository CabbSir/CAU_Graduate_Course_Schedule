from time import time

from . import db


class Course:
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    no = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    class_no = db.Column(db.Integer, nullable=False)
    point = db.Column(db.Numeric, nullable=False)
    week_start = db.Column(db.SmallInteger, nullable=False)
    week_end = db.Column(db.SmallInteger, nullable=False)
    create_time = db.Column(db.Integer, nullable=False, default=time)
    modify_time = db.Column(db.Integer, nullable=False, default=time)
