from db_connect import db


class UserWine(db.Model):
    __tablename__ = "user_wine"
    # id = db.Column(db.ForeignKey('g.id'), primary_key=True, unique=True, nullable=False)
    id = db.Column(db.String(100), primary_key=False, unique=False, nullable=False)
    mywine = db.Column(db.String(100), nullable=True)
    email = db.Column(db.Integer, db.ForeignKey('User.id'))
    idx = db.Column(db.Integer, primary_key=True)
    

    def __init__(self, id, mywine):
        self.id = id
        self.mywine = mywine


class User(db.Model):
    __tablename__ = "User"
    # id = db.Column(db.Float, primary_key=True, unique=True)
    id = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    # created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, id, name):
        self.id = id
        self.name = name
