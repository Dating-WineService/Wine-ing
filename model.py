from db_connect import db


class UserWine(db.Model):
    __tablename__ = "user_wine"
    # id = db.Column(db.ForeignKey('g.id'), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    mywine = db.Column(db.String(100), nullable=True)


    def __init__(self, id, mywine):
        self.id = id
        self.mywine = mywine