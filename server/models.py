from server import db, app, login_manager 
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    uid = db.Column( db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(50),nullable = False,unique = True)
    firstName = db.Column(db.String(120),nullable = False)
    lastName = db.Column(db.String(50),nullable = False)
    password = db.Column(db.String(60),nullable = False)
    addressLine = db.Column(db.String(100),nullable = False)
    city = db.Column(db.String(20),nullable = False)
    zip = db.Column(db.Integer,nullable = False)
    state = db.Column(db.String(20),nullable = False)
    country = db.Column(db.String(20),nullable = False)
    dob = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)

    def __repr__(self):
        return f"User('{self.email}','{self.password}','{self.firstName}','{self.dob}')"
    
    def get_id(self):
        return (self.uid)


class Books(db.Model):
    bid = db.Column( db.Integer, primary_key = True, autoincrement=True)
    isbn = db.Column(db.String(20),nullable = False,unique = True)
    title = db.Column(db.String(200),nullable = False)
    author = db.Column(db.String(200),nullable = False)
    yop = db.Column(db.String(6),nullable = False)
    publisher = db.Column(db.String(200),nullable = False)
    img_s = db.Column(db.String(200),nullable = False)
    img_m = db.Column(db.String(200),nullable = False)
    img_l = db.Column(db.String(200),nullable = False)
    price = db.Column(db.String(11),nullable = False)
    rating = db.Column(db.String(30),nullable = False)
    raters = db.Column(db.String(20),nullable = False)
    reviews = db.Column(db.Text,nullable = False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Books('{self.title}','{self.isbn}','{self.author}')"


class Clicks(db.Model):
    cid = db.Column( db.Integer, primary_key = True, autoincrement=True)
    isbn = db.Column(db.String(20),nullable = False,)
    uid = db.Column(db.String(20),nullable = False)
    time1 = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)

    def __repr__(self):
        return f"Click('{self.isbn}','{self.uid}')"

class Search(db.Model):
    sid = db.Column( db.Integer, primary_key = True, autoincrement=True)
    searchtxt = db.Column(db.String(20),nullable = False,)
    uid = db.Column(db.String(20),nullable = False)
    time1 = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)

    def __repr__(self):
        return f"Search('{self.isbn}','{self.uid}')"