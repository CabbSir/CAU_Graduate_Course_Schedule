from . import db


class Calendar(db.Model):
    __tablename__ = 'tb_calendar'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    season_id = db.Column(db.Integer, nullable = False)
    week_no = db.Column(db.Integer, nullable = False)
    week_day = db.Column(db.SmallInteger, nullable = False)
    date = db.Column(db.Date(), nullable = False)
