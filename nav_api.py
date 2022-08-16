from flask import Flask, render_template, session, abort, redirect, request, Blueprint
import pandas as pd
from recommend_wine_modules import start
from db_connect import db


nav = Blueprint('nav', __name__)

# 간단히만 만들어 놓고 나중에 수정할 예정

@nav.route('/service')
def service():
    return render_template('service.html')
    
@nav.route('/winenews')
def winenews():
    return render_template('winenews.html')
    
@nav.route('/winedic')
def winedic():
    return render_template('winedic.html')
    
@nav.route('/winemap')
def winemap():
    return render_template('winemap.html')
    
@nav.route('/contactus')
def contactus():
    return render_template('contactus.html')
