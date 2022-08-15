from email.mime import image
from operator import index
from unicodedata import name
from unittest import result
from flask import Flask,render_template,request,redirect,url_for,g,session
import sys
from db_connect import db
from model import UserWine
from data_api import application



# from database import load_list
app = Flask(__name__)
app.register_blueprint(application)


# DB config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:3306/wine_project'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)



import database

@app.route('/')
def main():
    return render_template("mainpage.html")

