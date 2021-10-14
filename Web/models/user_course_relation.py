from . import db


class UserCourseRelation(db.Model):
    __tablename__ = 'tb_user_course_relation'
    id = db.Column(db.Integer, nullable = False, primary_key = True) # orm必须创建主键
    user_id = db.Column(db.Integer, nullable = False)
    course_id = db.Column(db.Integer, nullable = False)
