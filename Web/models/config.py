import time

from . import db


class Season(db.Model):
    __tablename__ = 'tb_config'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    need_update_season = db.Column(db.SmallInteger, nullable = False, default = 2)
    create_time = db.Column(db.Integer, nullable = False, default = int(time.time()))
    modify_time = db.Column(db.Integer, nullable = False, default = int(time.time()))
