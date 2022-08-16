from email.mime import image
from operator import index
from unicodedata import name
from unittest import result
from flask import Flask,render_template,request,redirect,url_for,g,session
import sys
from db_connect import db
from model import User
from model import UserWine
from data_api import application
from user_api import user
from survey_api import survey



# from database import load_list
app = Flask(__name__)
app.secret_key = "secret"
app.register_blueprint(user)
app.register_blueprint(survey)
app.register_blueprint(application)


# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:3306/wine_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



import database

@app.route('/')
def main():
    if g.user_name:
        return render_template('mainpage.html', user_name=g.user_name)
    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)