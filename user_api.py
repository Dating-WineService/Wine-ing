import os
import pathlib

import requests
from flask import Flask, render_template, session, abort, redirect, request, Blueprint, jsonify, g

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from model import User
from db_connect import db

user = Blueprint('user', __name__)

# Google login config


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "53534203015-fggu8umovmpvppacsafkd4a1ib6hgl0t.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# 로그인한 사용자 확인
@user.before_app_request
def load_logged_in_user():
    user_id = session.get('google_id')
    # user_name = session.get('name')
    # print(user_id)
    if user_id is None:
        g.user_obj = None
        g.user_name = None
        print(g.user_name)
        return render_template('login.html')
    else:
        g.user_obj = db.session.query(User).filter(User.id == user_id).first()
        g.user_name = g.user_obj.name
        print(g.user_name)


# @user.route("/login")
# def login():
#     return render_template('login.html')


@user.route("/index")
def index():
    if g.user_name:
        return render_template('index.html', user_name=g.user_name)
    else:
    # print(g.user_obj)
        return render_template('login.html')


@user.route("/google_login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@user.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    user_id = id_info.get("email")
    user_name = id_info.get("name")

    user_obj = User.query.filter(User.id == user_id).first()

    # 유저 정보가 있으면
    if user_obj is not None:
        session['google_id'] = user_obj.id
        session["name"] = user_obj.name
        print('success')
        # return jsonify({'result':'success'})

    # 유저 정보가 없으면 가입, db에 저장
    else:
        print('fail')
        user_obj = User(user_id, user_name)
        db.session.add(user_obj)
        db.session.commit()
        print('save in DB')
        # return jsonify({'result':'save'})
    return redirect('/index')

@user.route("/logout")
def logout():
    session.clear()
    return redirect("/")
