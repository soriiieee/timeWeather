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


def fileURL100571(ctime12,code,RUN_MODE="RETRY",SYUSEI=False):

    ff = code[0:2]
    yy = ctime12[0:4]
    mm = ctime12[4:6]
    dd = ctime12[6:8]
    hh = ctime12[8:10]
    mi = ctime12[10:12]

    if mi =="00":
        T="0"
    else:
        T="1"

    if RUN_MODE=="RETRY":
        if SYUSEI:
            return f"http://micproxy2.core.micos.jp/stock/{yy}/{mm}/{yy}{mm}{dd}/data/100571/{yy}{mm}{dd}/000{T}{ff}/0000/100571-000{T}{ff}-0000-{ctime12}00.xml"
        else:
            return f"http://micproxy2.core.micos.jp/stock/{yy}/{mm}/{yy}{mm}{dd}/data/100571/{yy}{mm}{dd}/000{T}{ff}/0000/100571-000{T}{ff}-0000-{ctime12}00.xml"

    elif RUN_MODE=="UNYOU":
        if SYUSEI:
            return f"http://micproxy1.core.micos.jp/product/data/100571/{yy}{mm}{dd}/000{T}{ff}/0000/100571-000{T}{ff}-0000-{ctime12}00.xml"
        else:
            return f"http://micproxy1.core.micos.jp/product/data/100571/{yy}{mm}{dd}/000{T}{ff}/0000/100571-000{T}{ff}-0000-{ctime12}00.xml"


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
# print(tbl.head())

_code = tbl["観測所番号"].astype(str).values.tolist()

_timej = pd.date_range(start="202007040100", freq="30T", periods=3*(24)*2 + 11*2)
_timeu = [ time - timedelta(hours=9) for time in _timej ]
# print(_timeu[-1])
# sys.exit()
for utime12 in tqdm(_timeu):
    utime12 = utime12.strftime("%Y%m%d%H%M")

    _df=[]
    for ff in _FF:
        # ff="11
        _code2 = [ code for code in _code if code.startswith(ff)]
        # print(_code2)
        # sys.exit()
        # l += len(_code)
        url = fileURL100571(utime12,ff,RUN_MODE="UNYOU",SYUSEI=False)
        # print(url)
        # with open("../env/mic.conf") as f:
        mic_id = open("../env/mic.conf").read().split(" ")[0]
        mic_pass= open("../env/mic.conf").read().split(" ")[1]
        # print(mic_id, mic_pass)
        # sys.exit()
        res = requests.get(url,auth=(mic_id, mic_pass))

        if res.status_code == 200: #sokuhou

            root = ET.fromstring(res.text)
            _ele = root.findall('point')

            _productCode = []
            _eleMents = []
            for e in root.findall('point'):
                _productCode.append(e.attrib["pointCode"])
                elements = read_val(e)
                _eleMents.append(elements)
                # print(elements)
                # sys.exit()
                # print(len(elements))
                # print(len(xml_col2))
                # _eleMents.append(read_val(e))
                # sys.exit()

        else:
            pass

        df = pd.DataFrame()
        df["element"]= xml_col2
        df = df.set_index("element")
        # df[]index= xml_col2
        for i,code in enumerate(_productCode):
            # print(len(_eleMents[i]))
            df[code] = _eleMents[i]

        _df.append(df)
    
    df_all = pd.concat(_df, axis=1)
    df_all.T.to_csv(f"/home/griduser/work/sori-py2/timeWeather/dat/100571/code_x/{utime12}.csv")

    
    # sys.exit()
