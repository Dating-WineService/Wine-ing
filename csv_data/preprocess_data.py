import pandas as pd
from ast import literal_eval

def preprocessing_at_once(df):
  wine_df = df.copy()
    # 필요 열 추출
  col_list = ['wine_id', 'name', 'wine_type',
        'rating_mean', 'rating_num', 'kprice',
        'Alcohol content', 'Pairings',
        'LightBold', 'SmoothTannic', 'DrySweet', 'SoftAcidic']
  wine_df = wine_df[col_list]

  wine_df = wine_df.rename(columns={'Alcohol content':'Alcohol_content','LightBold':'Light_Bold',
                                    'SmoothTannic':'Smooth_Tannic','DrySweet':'Dry_Sweet','SoftAcidic':'Soft_Acidic'})


  # wine_id를 인덱스로
  wine_df = wine_df.set_index('wine_id')

  # rating_num 전처리
  wine_df['rating_num'] = wine_df['rating_num'].str.split().str[0].astype('int')

  # Parings를 리스트 타입으로 만들기
  for i in range(len(wine_df['Pairings'])):
    if type(wine_df['Pairings'][i]) == float:
      # 같이 먹을 음식이 없으면 0으로 설정
      wine_df['Pairings'][i] = '0'


  # 문자열을 객체로 변경: 리스트 내의 사전
  wine_df['Pairings'] = wine_df['Pairings'].apply(literal_eval)

  # 와인 타입에서 wine 문자열 제거하기
  wine_df_type = wine_df['wine_type'].copy()
  wine_df_type = wine_df_type.str.replace(' wine', '')
  wine_df_type = wine_df_type.str.replace(' Wine', '')
  wine_df_type = wine_df_type.str.strip()

  wine_df['wine_type'] = wine_df_type
  wine_df[['wine_type']].value_counts()

  # kprice 쉼표 제거하기
  wine_df_price = wine_df['kprice'].copy()
  wine_df_price = wine_df_price.str.replace(',', '').astype('float')
  wine_df['kprice'] = wine_df_price
  wine_df[['kprice']]

  # 유사도에 사용할 열(설문조사와 관련된 열) 선택 -> survey_df
  col_need = ['wine_type', 'Alcohol_content', 'Light_Bold', 'Smooth_Tannic', 'Soft_Acidic', 'Dry_Sweet', 'kprice','Pairings']
  survey_df = wine_df[col_need].copy()

  ### wine_type, Pairings 값 분리해서 원핫인코딩하기 -> sim_df
  # Pairings 중복 제거하기
  survey_df['Pairings'][0]
  pa_list = survey_df['Pairings'].copy()
  flat = []
  for sublist in pa_list:
    if sublist == 0:
      sublist = ['None_pairing']
    for item in sublist:
      flat.append(item)
  pair_list = list(set(flat))

  # 정수로 바뀐 0을 문자로 바꾸기
  survey_df.loc[survey_df['Pairings'] == 0,'Pairings'] = '0'

  # item이 존재하면 1 아니면 0
  for item in pair_list:
    survey_df[item] = survey_df['Pairings'].apply(lambda x: 1 if item in x else 0)

  # 와인 타입 원핫인코딩
  type_df = survey_df['wine_type'].str.get_dummies()

  # survey_df, type_df 합치기 -> sim_df
  sim_df = pd.concat([survey_df, type_df], axis=1)

  # 원핫 인코딩한 열 제거
  sim_df.drop(['wine_type', 'Pairings'],1, inplace=True)

  # Light_Bold, Smooth_Tannic, Soft_Acidic, Dry_Sweet, kprice
  bin_df = sim_df.copy()
  group = [1, 2, 3, 4, 5]

  bin_df['light_bold_level'], mybin = pd.cut(bin_df['Light_Bold'], 5, labels=group, retbins=True)
  print('light_bold_level')
  print(mybin)

  bin_df['smooth_tannic_level'], mybin = pd.cut(bin_df['Smooth_Tannic'], 5, labels=group, retbins=True)
  print('smooth_tannic_level')
  print(mybin)

  bin_df['soft_acidic_level'], mybin = pd.cut(bin_df['Soft_Acidic'], 5, labels=group, retbins=True)
  print('soft_acidic_level')
  print(mybin)

  bin_df['dry_sweet_level'], mybin = pd.cut(bin_df['Dry_Sweet'], 5, labels=group, retbins=True)
  print('dry_sweet_level')
  print(mybin)

  price_group = [1, 2, 3, 4, 5, 6]
  bin_df['kprice_level'], mybin = pd.cut(bin_df['kprice'], bins=[0, 30000, 70000, 100000, 150000, 200000, 1000000], labels=price_group, retbins=True)
  print('kprice_level')
  print(mybin)

  bin_df['Alcohol_content_level'], mybin = pd.cut(bin_df['Alcohol_content'], 5, labels=group, retbins=True)
  print('Alcohol_content_level')
  print(mybin)

  bin_df.drop(['Alcohol_content', 'Light_Bold', 'Smooth_Tannic', 'Soft_Acidic', 'Dry_Sweet', 'kprice'],1, inplace=True)

  return wine_df, bin_df