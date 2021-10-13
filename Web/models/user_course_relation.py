from . import db


class UserCourseRelation(db.Model):
    __tablename__ = 'tb_user_course_relation'
    user_id = db.Column(db.Integer, nullable = False)
    course_id = db.Column(db.Integer, nullable = False)
