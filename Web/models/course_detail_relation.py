from . import db


class CourseDetailRelation:
    course_id = db.Column(db.Integer, nullable=False)
    detail_id = db.Column(db.Integer, nullable=False)