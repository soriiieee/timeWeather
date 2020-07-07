# -*- coding: utf-8 -*-
# xml形式のデータから日射量を切り出す
import xml.etree.ElementTree as ET
import numpy as np
import sys
import os
import requests
from tqdm import tqdm
import pandas as pd
from datetime import datetime, timedelta



def selectCode(tbl, _ff):
    print("before", tbl.shape)
    _tbl2=[]
    for ff in _ff:
        _tbl2.append(tbl[tbl["ken47"]== int(ff)])
    
    tbl= pd.concat(_tbl2, axis=0).reset_index(drop=True)
    print("after", tbl.shape)
    return tbl

    res = requests.get(url,auth=('micosguest', 'mic6guest'))
    logger.info(res.status_code)

    # continue
    # sys.exit()
    if res.status_code == 200: #sokuhou
        root = ET.fromstring(res.text)
        _productCode = []
        _ele = root.findall('point')

# sys.exit()
# site
#element


xml_col1=["stationLongitude","stationLatitude","stationHeightASL","anemometerHeight"]
xml_col2=["tenminPrecip","sixtyminPrecip","windDirection","windSpeed","temp","tenminSunshine","sixtyminSunshine", "snowDepth","humidity","seaLevelPressure", "stationPressure","visibility","dailyMaxTenminPrecip", "dailyMaxSixtyminPrecip","dailyMaxWindDirection","dailyMaxInstWindSpeed","dailyMaxInstWindDirection", "dailyMaxTemp","dailyMaxSnowDepth","dailyMinTemp", "dailyMinHumidity", "onehourMaxTenminPrecip","onehourMaxSixtyminPrecip","onehourMaxWindSpeed","onehourMaxWindDirection", "onehourMaxInstWindSpeed","onehourMaxInstWindDirection","onehourMaxTemp", "onehourMaxSnowDepth","onehourMinTemp","twentyfourhourPrecip","twentyfourhourSnowFall","onehourSnowFall","autoObsWeather","tenminMaxTemp", "tenminMaxInstWindSpeed","tenminMaxInstWindDirection","tenminMinTemp","tenminMinHumidity"]


def make_dummy():
    e_codes,e_info1,err_name,err_info,time_name,time_info=[],[],[],[],[],[]
    #shape
    e_codes = [ 9999 for i in range(len(xml_col1))]
    e_info1 = [ 9999 for i in range(len(xml_col2))]
    err_name = [ 9999 for i in range(len(xml_col2))]
    err_info = [ 9999 for i in range(len(xml_col2))]
    time_name = [ 9999 for i in range(len(xml_col2))]
    time_info = [ 9999 for i in range(len(xml_col2))]

    return [e_codes,e_info1,err_name,err_info,time_name,time_info]

def read_val(e):
    #init
    e_codes     = [] #xml_col1

    e_info1     = [] #xml_col2
    err_name    = [] #xml_col2
    err_info    = [] #xml_col2
    time_name   = [] #xml_col2
    time_info   = [] #xml_col2
    a = e.find('observation')

    for epl in xml_col1:
        val = a.find(epl).text
        if val is None:
            val = 9999
            
        e_codes.append(val)

    #weather info2
    for ele in xml_col2:
        val = a.find(ele).text
        aqc = a.find(ele).get('aqcCode')
        time = a.find(ele).get('time')
        # time = time[0:16]

        if val is None:
            val = 9999
        if aqc is None:
            aqc  = 9999
        if time is None:
            time = 9999

        # val
        e_info1.append(val)
        # acp
        err_name.append(ele)
        err_info.append(aqc)
        # time
        time_name.append(ele)
        time_info.append(time)
        
    #-----logger add-----------------------------------
    # logger.info('{}, {},{},{},{}'.format(code,ini_u,val,ele,aqc,time))
    #-----logger add-----------------------------------
    return e_info1

def add_100571_file(code,info):
    # info = [e_codes,e_info1,err_name,err_info,time_name,time_info]
    _wth = info[0] + info[1]
    _aqc = info[0] + info[3]
    _time = info[0] + info[5]

    #info
    L = [str(ele) for ele in _wth ]
    L =" ".join(L)
    f=open(out_d+"/"+code+".dat","+a") # param[2] = 出力ファイル
    string = "{0} {1}\n".format(ini_j,L)
    f.write(string)
    f.close()

    #acp ---------------------------------------------
    L = [str(ele) for ele in _aqc ]
    L =" ".join(L)
    f=open(out_d+"/"+code+"_aqc.dat","+a") # param[2] = 出力ファイル
    string = "{0} {1}\n".format(ini_j,L)
    f.write(string)
    f.close()
    #time ---------------------------------------------
    L = [ str(ele) for ele in _time ]
    L =" ".join(L)
    f=open(out_d+"/"+code+"_time.dat","+a") # param[2] = 出力ファイル
    string = "{0} {1}\n".format(ini_j,L)
    f.write(string)
    f.close()
    return

l=0

_FF=["83","84","85","86","87","88"]

tbl = pd.read_csv("../tbl/tbl_ame.csv")
tbl = selectCode(tbl, _FF)
_code = tbl["観測所番号"].astype(str).values.tolist()

_timej = pd.date_range(start="202007040100", freq="30T", periods=3*(24)*2 + 11*2)
_timeu = [ time - timedelta(hours=9) for time in _timej ]

DIR="/home/griduser/work/sori-py2/timeWeather/dat/100571/code_x"
DIR_T="/home/griduser/work/sori-py2/timeWeather/dat/100571/code_t"


        # _df = []
        # for time  in tqdm(_timeu):
        #     ctime = time.strftime("%Y%m%d%H%M")
        #     df = pd.read_csv(f"{DIR}/{ctime}.csv")
        #     df["time"] = ctime
        #     df = df.rename(columns={"Unnamed: 0":"code"})
        #     _df.append(df)
        #     print(df.head())

        # df_all = pd.concat(_df,axis=0)
        # df_all.to_csv(f"{DIR}/df_all.csv")

df_all = pd.read_csv(f"{DIR}/df_all.csv")
# print(df_all.dtypes)
# sys.exit()
use_cols=['time','tenminPrecip', 'sixtyminPrecip', 'windDirection',
       'windSpeed', 'temp', 'tenminSunshine', 'sixtyminSunshine', 'snowDepth',
       'humidity', 'seaLevelPressure', 'stationPressure', 'visibility',
       'dailyMaxTenminPrecip', 'dailyMaxSixtyminPrecip',
       'dailyMaxWindDirection', 'dailyMaxInstWindSpeed',
       'dailyMaxInstWindDirection', 'dailyMaxTemp', 'dailyMaxSnowDepth',
       'dailyMinTemp', 'dailyMinHumidity', 'onehourMaxTenminPrecip',
       'onehourMaxSixtyminPrecip', 'onehourMaxWindSpeed',
       'onehourMaxWindDirection', 'onehourMaxInstWindSpeed',
       'onehourMaxInstWindDirection', 'onehourMaxTemp', 'onehourMaxSnowDepth',
       'onehourMinTemp', 'twentyfourhourPrecip', 'twentyfourhourSnowFall',
       'onehourSnowFall', 'autoObsWeather', 'tenminMaxTemp',
       'tenminMaxInstWindSpeed', 'tenminMaxInstWindDirection', 'tenminMinTemp',
       'tenminMinHumidity']
for code in tqdm(_code):
    tmp = df_all[df_all["code"]== int(code)]
    tmp = tmp.reset_index(drop=True)
    tmp = tmp[use_cols]
    # print(tmp.columns)
    # sys.exit()
    # print()
    # print(tmp.head())
    # sys.exit()
    tmp.to_csv(f"{DIR_T}/{code}.csv")
    # print(code)