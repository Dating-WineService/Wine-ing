from flask import Flask, render_template, session, abort, redirect, request, Blueprint
import pandas as pd
from recommend_wine_modules import start
from db_connect import db


survey = Blueprint('survey', __name__)

pairings_list = ['Spicy food', 'Beef', 'Appetizers and snacks',
                'Rich fish (salmon, tuna etc)', 'Lamb', 'Mushrooms', 'Blue cheese',
                'Pork', 'None_pairing', 'Sweet desserts', 'Shellfish', 'Pasta',
                'Fruity desserts', 'Poultry', 'Veal', 'Mature and hard cheese',
                'Lean fish', 'Vegetarian', 'Cured Meat', 'Goat cheese',
                'Game (deer, venison)', 'Aperitif', 'Mild and soft cheese']

# first_sur = ['light', 'sweet', 'party', 'drunk']
# second_sur = pairings_list
# third_sur = ['soft_acidic_level', 'smooth_tannic_level', 'light_bold_level', 'Alcohol_content_level', 'dry_sweet_level']
# forth_sur = ['kprice_level']

"""
bin_df.columns

boolean
       ['Spicy food', 'Beef', 'Appetizers and snacks',
       'Rich fish (salmon, tuna etc)', 'Lamb', 'Mushrooms', 'Blue cheese',
       'Pork', 'None_pairing', 'Sweet desserts', 'Shellfish', 'Pasta',
       'Fruity desserts', 'Poultry', 'Veal', 'Mature and hard cheese',
       'Lean fish', 'Vegetarian', 'Cured Meat', 'Goat cheese',
       'Game (deer, venison)', 'Aperitif', 'Mild and soft cheese', 'Dessert',
       'Fortified', 'Red', 'Rosï§', 'Sparkling', 'White']

int(1~5)
       ['light_bold_level',
       'smooth_tannic_level', 'soft_acidic_level', 'dry_sweet_level',
       'kprice_level', 'Alcohol_content_level']

"""
key_list = ['Spicy food', 'Beef', 'Appetizers and snacks',
       'Rich fish (salmon, tuna etc)', 'Lamb', 'Mushrooms', 'Blue cheese',
       'Pork', 'None_pairing', 'Sweet desserts', 'Shellfish', 'Pasta',
       'Fruity desserts', 'Poultry', 'Veal', 'Mature and hard cheese',
       'Lean fish', 'Vegetarian', 'Cured Meat', 'Goat cheese',
       'Game (deer, venison)', 'Aperitif', 'Mild and soft cheese', 'Dessert',
       'Fortified', 'Red', 'Rosï§', 'Sparkling', 'White',

       'light_bold_level',
       'smooth_tannic_level', 'soft_acidic_level', 'dry_sweet_level',
       'kprice_level', 'Alcohol_content_level']

# 딕셔너리로 만들어 초기화하기
input_survey = {}

for key in key_list:
    input_survey[key] = 0
print(input_survey)

sur1 = 0
sur2 = 'None_pairing'
sur3 = {'soft_acidic_level':0, 'smooth_tannic_level':0, 'light_bold_level':0, 'Alcohol_content_level':0, 'dry_sweet_level':0}
sur4 = 0


@survey.route('/winetest1', methods=['GET', 'POST'])
def winetest1():
    global sur1
    if request.method == 'POST':
        sur1 = request.form['shop']
        return redirect('/winetest2')
    else:
        return render_template('winetest1.html')

@survey.route('/winetest2', methods=['GET', 'POST'])
def winetest2():
    global sur2
    if request.method == 'POST':
        sur2 = request.form['pairings'] # 페어링 값 받기: pairing은 최대한 Pairings열의 값들로
        return redirect('/winetest3')
    else:
        return render_template('winetest2.html')

@survey.route('/winetest3', methods=['GET', 'POST'])
def winetest3():
    global sur3
    if request.method == 'POST':
        sur3['soft_acidic_level'] = int(request.form['soft_acidic_level'])
        sur3['smooth_tannic_level'] = int(request.form['smooth_tannic_level'])
        sur3['light_bold_level'] = int(request.form['light_bold_level'])
        sur3['Alcohol_content_level'] = int(request.form['Alcohol_content_level'])
        sur3['dry_sweet_level'] = int(request.form['dry_sweet_level'])
        return redirect('/winetest4')
    else:
        return render_template('winetest3.html')

@survey.route('/winetest4', methods=['GET', 'POST'])
def winetest4():
    global sur4
    if request.method == 'POST':
        sur4 = int(request.form['kprice_level'])
        return redirect('/winetestresult')
    else:
        return render_template('winetest4.html')


@survey.route('/winetestresult')
def winetestresult():
    print(sur1, sur2, sur3, sur4)

    # sur1
    mood = sur1
    if mood == 1:
        input_survey['light_bold_level'] = 1
        input_survey['Alcohol_content_level'] = 1
        input_survey['smooth_tannic_level'] = 1
    elif mood == 2:
        input_survey['dry_sweet_level'] = 5
    elif mood == 3:
        input_survey['Sparkling'] = 1
    elif mood == 4:
        input_survey['Alcohol_content_level'] = 5
    else:
        pass

    # sur2
    pairing = sur2
    input_survey[pairing] = 1

    # sur3
    third_sur = ['soft_acidic_level', 'smooth_tannic_level', 'light_bold_level', 'Alcohol_content_level', 'dry_sweet_level']
    for sur in third_sur:
        if input_survey[sur] == 0:
            input_survey[sur] = sur3['soft_acidic_level']
        else:
            input_survey[sur] = (input_survey[sur] + sur3['soft_acidic_level'])/2

    # sur4
    input_survey['kprice_level'] = sur4

    
    print(input_survey)

    # calculate result
    wine_df = pd.read_csv('csv_data\\wine_df.csv')

    sur_wine_idx = survey_recommend(input_survey)
    col = ['name', 'vintage', 'wine_type', 'imgurl']
    need_wines_info = wine_df.loc[sur_wine_idx][col]
    sur_wine_dic = need_wines_info.to_dict('index')
    
    # 추천 잘 되었는지 확인용
    for i in sur_wine_idx:
        print(sur_wine_dic[i]['name'])
        print(sur_wine_dic[i]['vintage'])
        print(sur_wine_dic[i]['wine_type'])
        print(sur_wine_dic[i]['imgurl'])
    
    
    return render_template('winetestresult.html', sur_wine_dic=sur_wine_dic, sur_wine_idx=sur_wine_idx)


def survey_recommend(input_survey):
    bin_df = pd.read_csv('csv_data\\bin_df.csv')
    input = pd.DataFrame([input_survey], index=['input'])
    bin_df = pd.concat([bin_df, input], axis=0)

    idx_list = start(bin_df, 3)
    return(idx_list)
