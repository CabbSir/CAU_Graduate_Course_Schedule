import time

from . import db


class Detail(db.Model):
    __tablename__ = 'tb_detail'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    course_id = db.Column(db.Integer, nullable = False)
    weekday = db.Column(db.String(10), nullable = False)
    class_start = db.Column(db.SmallInteger, nullable = False)
    class_end = db.Column(db.SmallInteger, nullable = False)
    classroom = db.Column(db.String(50), nullable = False)
    create_time = db.Column(db.String(10), nullable = False, default = int(time.time()))
    modify_time = db.Column(db.String(10), nullable = False, default = int(time.time()))
