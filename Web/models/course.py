import time

from . import db


class Course(db.Model):
    __tablename__ = 'tb_course'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    no = db.Column(db.String(20), nullable = False)
    season_id = db.Column(db.Integer, nullable = False) # 新增season字段
    name = db.Column(db.String(50), nullable = False)
    class_no = db.Column(db.Integer, nullable = False)
    point = db.Column(db.Numeric(10, 1), nullable = False)
    week_start = db.Column(db.SmallInteger, nullable = False)
    week_end = db.Column(db.SmallInteger, nullable = False)
    is_special = db.Column(db.SmallInteger, nullable = False, default = 2)
    build_status = db.Column(db.SmallInteger, nullable = False, default = 2)
    remark = db.Column(db.String(2000), nullable = True, default = "")
    create_time = db.Column(db.Integer, nullable = False, default = int(time.time()))
    modify_time = db.Column(db.Integer, nullable = False, default = int(time.time()))
