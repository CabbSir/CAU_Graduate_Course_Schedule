from . import db


class CourseDetailRelation(db.Model):
    __tablename__ = 'tb_course_detail_relation'
    course_id = db.Column(db.Integer, nullable = False)
    detail_id = db.Column(db.Integer, nullable = False)
