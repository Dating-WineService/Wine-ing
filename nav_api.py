from flask import Flask, render_template, session, abort, redirect, request, Blueprint, g
import pandas as pd
from recommend_wine_modules import start
from db_connect import db


nav = Blueprint('nav', __name__)

# 간단히만 만들어 놓고 나중에 수정할 예정

@nav.route('/service')
def service():
    if g.user_name:
        return render_template('service.html', user_name=g.user_name)
    else:
        return render_template('service.html')
    
@nav.route('/winenews')
def winenews():
    if g.user_name:
        return render_template('winenews.html', user_name=g.user_name)
    else:
        return render_template('winenews.html')
    
@nav.route('/winedic')
def winedic():
    if g.user_name:
        return render_template('winedic.html', user_name=g.user_name)
    else:
        return render_template('winedic.html')
    
@nav.route('/winemap')
def winemap():
    if g.user_name:
        return render_template('winemap.html', user_name=g.user_name)
    else:
        return render_template('winemap.html')
    
@nav.route('/contactus')
def contactus():
    if g.user_name:
        return render_template('contactus.html', user_name=g.user_name)
    else:
        return render_template('contactus.html')
