from . import db


class CourseDetailRelation(db.Model):
    __tablename__ = 'tb_course_detail_relation'
    id = db.Column(db.Integer, nullable = False, primary_key = True) # orm必须创建主键
    course_id = db.Column(db.Integer, nullable = False)
    detail_id = db.Column(db.Integer, nullable = False)
