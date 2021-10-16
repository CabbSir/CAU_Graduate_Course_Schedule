import time

from . import db


class Season(db.Model):
    __tablename__ = 'tb_season'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    year = db.Column(db.Integer, nullable = False)
    season = db.Column(db.SmallInteger, nullable = False)
    begin_date = db.Column(db.Date, nullable = False)
    total_weeks = db.Column(db.Integer, nullable = False)
    is_now = db.Column(db.SmallInteger, nullable = False, default = 2)
    create_time = db.Column(db.Integer, nullable = False, default = int(time.time()))
    modify_time = db.Column(db.Integer, nullable = False, default = int(time.time()))
