from email.mime import application, image
from operator import index
from unicodedata import name
from unittest import result
from flask import Flask,render_template,request,redirect,url_for,g,session,Blueprint
import sys
from db_connect import db
from model import UserWine



# from database import load_list
application = Blueprint('application', __name__)




import database

# app.py에 있는 route('/')와 중복되어서 주석처리했어요!
# @application.route('/')
# def main():
#     return render_template("mainpage.html")

@application.route('/winelist')
def winelist():
    wine_list=database.load_list()
    return render_template("winelist.html",wine_list=wine_list)

@application.route('/wineliststar')
def wineliststar():
    wine_list=database.load_list_star()
    return render_template("wineliststar.html",wine_list=wine_list)


@application.route('/winelistprice')
def winelistprice():
    wine_list=database.load_list_price()
    return render_template("winelistprice.html",wine_list=wine_list)

@application.route('/wineinfo/<int:index>/')
def wineinfo(index):
    # 와인 기본 정보
    wine_info=database.load_info(index)
    wine_id=wine_info["wine_id"]
    name=wine_info["name"]
    vintage=wine_info["vintage"]
    wine_type=wine_info["wine_type"]
    grape_simple=wine_info["grape_simple"]
    rating_num=wine_info["rating_num"]
    kprice=wine_info["kprice"]
    winery=wine_info["Winery"]
    grapes=wine_info["Grapes"]
    region=wine_info["Region"]
    alcohol=wine_info["Alcohol content"]
    pairings=wine_info["Pairings"]
    rec_id=wine_info["rec_id"]
    imgurl=wine_info["imgurl"]
    # rec_id.tolist()




    # 추천 와인 정보
    winerecolist=[]
    recwines=rec_id.split(',')
    for x in recwines:
        x=int(x)
        winereco=database.load_info(x)
        reco_img=winereco["imgurl"]
        reco_name=winereco["name"]
        reco_vintage=winereco["vintage"]
        reco_type=winereco["wine_type"]
        reco_id=x
        winerecolist.append([reco_name,reco_vintage,reco_type,reco_img,reco_id])

    return render_template("wineinfo.html",wine_id=wine_id,name=name,vintage=vintage,wine_type=wine_type,grape_simple=grape_simple
    ,rating_num=rating_num,kprice=kprice,winery=winery,grapes=grapes,region=region,alcohol=alcohol,pairings=pairings,imgurl=imgurl,rec_id=rec_id
    ,winerecolist=winerecolist
    )


# 찜하기를 눌렀을때
@application.route('/mywineclick',methods=['GET','POST'])
def mywineclick():
    if request.method=='POST':
        mywine=request.form['mywine']
        print("*******",mywine)

        userwine=UserWine(g.user_name,mywine)
        db.session.add(userwine)
        db.session.commit()
        return redirect(url_for("application.mywine"))
        # return redirect(url_for("wineinfo(index)"))
    else:
        return render_template("mywine.html")

# 나의와인
@application.route('/mywine')
def mywine():
    result=[]

    # data = db.session.query(UserWine).filter(UserWine.id.like(g.user_name)).all()
    data = list(set(db.session.query(UserWine.id, UserWine.mywine).filter(UserWine.id.like(g.user_name)).all()))
    print(data)

    for d in data:
        tmp={'id':d.id ,'mywine':d.mywine}
        mywine=int(d.mywine)
        wine_info=database.load_info(mywine)
        tmp['wine_name']=wine_info["name"]
        tmp['imgurl']=wine_info["imgurl"]
        tmp['wine_vintage']=wine_info["vintage"]
        tmp['wine_type']=wine_info["wine_type"]
        result.append(tmp)

    return render_template("mywine.html",userwine_list=result)


# @app.route('/search',methods=['GET','POST'])
# def search():
#     if request.method=='POST':
#         key=request.form['keyword']
#         con=request.form['condition']
#     return render_template("winelist.html")