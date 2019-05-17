import pandas as pd
import os
from datetime import datetime, timedelta
os.chdir("/Users/zhengyuanma/Desktop/Thesis/Thesis/mongo_analysis/unicorn_scraper")
class Unicorn:
    def __init__(self, id_):
        self.id:str = id_
        self.name:str = None
        self.rongzi:pd.DataFrame = None

    def set_name(self, name):
        self.name = name
    def set_rongzi(self, table):
        self.rongzi = table

    def __str__(self):
        return (self.name + self.id + "\n" + self.rongzi.to_string())


import pickle
unic1, unic2, unic3 = None, None, None
with open("unis_0.bin", "rb") as f:
    unic1 = pickle.load(f)
with open("unis_1.bin", "rb") as f:
    unic2 = pickle.load(f)
with open("unis_2.bin", "rb") as f:
    unic3 = pickle.load(f)

unic = unic1 + unic2 + unic3
no_list = ["蚂蚁金服","阿里云","京东数科","菜鸟网络","京东物流","苏宁金融","平安医保科技","网易云音乐","金山云","苏宁体育","古北水镇","网易有道"]
unicd = {u.name:u.rongzi for u in unic if u.name not in no_list}
unic_no = {u.name:u.rongzi for u in unic if u.name in no_list and u.name is not "古北水镇"}

def get_date_diff(df:pd.DataFrame):
    if len(df) == 0:
        return timedelta(days=-1)
    a_t = df[df[1] == "A轮"][0]
    b_t = df[df[1] == "B轮"][0]
    if len(a_t) > 0 and len(b_t) > 0:
        a_t = list(a_t)[0]
        b_t = list(b_t)[0]
        a_t = datetime.strptime(a_t, "%Y-%m-%d")
        b_t = datetime.strptime(b_t, "%Y-%m-%d")
        diff = b_t - a_t
        return diff
    else:
        return timedelta(days=-1)

d_diff = {k:get_date_diff(v).days for k,v in unicd.items()}
no_diff = {k:get_date_diff(v).days for k,v in unic_no.items()}