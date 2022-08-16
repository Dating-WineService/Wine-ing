import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import MinMaxScaler



from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import MinMaxScaler

def euc_dist(df):

  scaler = MinMaxScaler()
  e_d = euclidean_distances(df.iloc[:,-12:], np.array(df.loc['input'][-12:]).reshape(1, -1))
  
  # 여기에 pairings 가중하기
  sp = pd.DataFrame(df.loc['input',:][:-12])
  try:
    exp_pair = sp[sp['input'] == 1].index[0] ### -> 음식은 단 하나만 선택[beef] 추천 받음
    add_weight_idx = df[df[exp_pair] != 1].index
    # print(add_weight_idx)
  except:
    add_weight_idx = df.index
    # print(add_weight_idx)

  e_d = pd.DataFrame(e_d, index=df.index)
  e_d.loc[add_weight_idx] += 3


  eculidean_similarity = scaler.fit_transform(e_d)
  eculidean_similarity = 1 - eculidean_similarity

  sim_record = pd.DataFrame(eculidean_similarity, index=df.index, columns=['similarity'])
  sim_record.sort_values(by='similarity', ascending=False)[:10]
  sim_record.drop(['input'], axis=0, inplace=True)
  return sim_record


def get_weighted_rating_average(record):
  global wine_df
  percentile = 0.
  m = wine_df['rating_num'].quantile(percentile)
  C = wine_df['rating_mean'].mean()

  v = record['rating_num']
  R = record['rating_mean']
  weighted_rating_average = ( (v/(v+m)) * R ) + ( (m/(m+v)) * C )
  return weighted_rating_average

def get_sim_weight_table(sim_record):
  global wine_df
  sim_record['weighted_vote'] = wine_df.apply(get_weighted_rating_average, axis=1)
  return sim_record

def get_full_sim_weight_table(sim_weight_table):
  global wine_df
  full_sim_weight_table = pd.concat([sim_weight_table, wine_df], axis=1)
  full_sim_weight_table = full_sim_weight_table.sort_values(by=['similarity', 'weighted_vote'], ascending=False)
  return full_sim_weight_table


def get_recommended_idx(full_sim_weight_table, top_n):
  final_idx = full_sim_weight_table.iloc[:top_n].index
  return final_idx

def start(df, top_n):
  sim_record = euc_dist(df)
  sim_weight_table = get_sim_weight_table(sim_record)
  full_sim_weight_table = get_full_sim_weight_table(sim_weight_table)
  final_index = get_recommended_idx(full_sim_weight_table, top_n)
  return final_index

# 설문조사에서 입력 받을 레코드 양식 -> bin_df
wine_df = pd.read_csv('Dating_wineservice\csv_data\wine_df.csv')
