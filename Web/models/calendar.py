from . import db


class Calendar(db.Model):
    __tablename__ = 'tb_calendar'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    season_id = db.Column(db.Integer, nullable = False)
    week_no = db.Column(db.Integer, nullable = False)
    mon = db.Column(db.Date(), nullable = False)
    tues = db.Column(db.Date(), nullable = False)
    wed = db.Column(db.Date(), nullable = False)
    thur = db.Column(db.Date(), nullable = False)
    fri = db.Column(db.Date(), nullable = False)
    sat = db.Column(db.Date(), nullable = False)
    sun = db.Column(db.Date(), nullable = False)
