import pandas as pd

# def save(location, cleaness, built_in):
#     idx = len(pd.read_csv("database.csv"))
#     new_df = pd.DataFrame({"location":location,
#                            "cleaness":cleaness,
#                            "built_in":built_in}, 
#                          index = [idx])
#     new_df.to_csv("database.csv",mode = "a", header = False)
#     return None

def load_list():
    wine_list = []
    df = pd.read_csv("wine_data.csv",encoding='utf-8')
    for i in range(len(df)):
        wine_list.append(df.iloc[i].tolist())
    print(wine_list[0])
    return wine_list

def load_list_star():
    wine_list = []
    df = pd.read_csv("wine_data_rating.csv",encoding='utf-8')
    for i in range(len(df)):
        wine_list.append(df.iloc[i].tolist())
    print(wine_list[0])
    return wine_list

def load_list_price():
    wine_list = []
    df = pd.read_csv("wine_data_price.csv",encoding='utf-8')
    for i in range(len(df)):
        wine_list.append(df.iloc[i].tolist())
    print(wine_list[0])
    return wine_list

# def now_index():
#     df = pd.read_csv("database.csv")
#     return len(df)-1


def load_info(idx):
    df = pd.read_csv("wine_info_data.csv",encoding='utf-8')
    wine_info = df.iloc[idx]
    return wine_info


# if __name__ =="__main__":
#     load_list()