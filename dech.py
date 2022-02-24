from cgitb import text
from lib2to3.pgen2 import token
from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(500), nullable=False)

    def __init__(self, name, psswd):
        super().__init__()
        self.name = name
        self.password = psswd

    def __repr__(self):
        return f"<users {self.id}>"

class Meseges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer)
    to_user = db.Column(db.Integer)
    text = db.Column(db.Text)

    def __init__(self, from_user, to_user, text):
        super().__init__()
        self.from_user = from_user
        self.to_user = to_user
        self.text = text

    def __repr__(self):
        return f"<msg {self.id}>"


@app.route("/reg/<name>/<password>")
def reg(name, password):
    usrs = Users.query.filter_by(name=name).all()

    if len(usrs) > 0:
        return 'ALREADY'
    else:
        db.session.add(Users(name, password))
        db.session.flush()
        db.session.commit()
        uid = Users.query.filter_by(name=name).first().id
        return f'id={uid}'


@app.route("/login/<name>/<password>")
def reg(name, password):
    usrs = Users.query.filter_by(name=name).all()

    if len(usrs) != 1:
        return 'NO'
    else:
        return f'id={usrs[0].id}'

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

