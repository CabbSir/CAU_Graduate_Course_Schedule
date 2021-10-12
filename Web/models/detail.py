from . import db


class Detail:
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    weekday = db.Column(db.String(10), nullable=False)
    class_start = db.Column(db.SmallInteger, nullable=False)
    class_end = db.Column(db.SmallInteger, nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.String(10), nullable=False)
    modify_time = db.Column(db.String(10), nullable = False)
