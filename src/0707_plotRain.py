# -*- coding: utf-8 -*-
# when   : 2020.0x.xx
# who : [sori-machi]
# what : [ ]
#---------------------------------------------------------------------------
# basic-module
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.simplefilter('ignore')
from tqdm import tqdm
import seaborn as sns
#---------------------------------------------------
# sori -module
sys.path.append('/home/griduser/tool')
from getErrorValues import me,rmse,mae,r2 #(x,y)
from getPlot import drawPlot,autoLabel #(x=False,y,path),(rects, ax)
from convSokuhouData import conv2allwithTime,conv2CutCols #(df),(df, ave=minutes,hour)
from convAmedasData import conv2allwithTime,conv2CutCols #(df),(df, ave=minutes,hour)
from checkFileExistSize import checkFile #(input_path)
# from plotMonthData import plotDayfor1Month #(df,_col,title=False)
#---------------------------------------------------

OUTD="/home/griduser/work/sori-py2/timeWeather/out/0707/rain"



def selectCode(tbl, _ff):
    print("before", tbl.shape)
    _tbl2=[]
    for ff in _ff:
        _tbl2.append(tbl[tbl["ken47"]== int(ff)])
    
    tbl= pd.concat(_tbl2, axis=0).reset_index(drop=True)
    print("after", tbl.shape)
    return tbl

_FF=["83","84","85","86","87","88"]

tbl = pd.read_csv("../tbl/tbl_ame.csv")
tbl = selectCode(tbl, _FF)

def nameKEN(x):
  x=str(x)
  if x=="83":
    return "OITA"
  if x=="84":
    return "NAGASAKI"
  if x=="85":
    return "SAGA"
  if x=="86":
    return "KUMAMOTO"
  if x=="87":
    return "MIYAZAKI"
  if x == "88":
    return "KAGOSHIMA"


_code = tbl["観測所番号"].astype(str).values.tolist()
_name = tbl["name"].astype(str).values.tolist()

tbl["ken"] = tbl["ken47"].apply(lambda x:nameKEN(x))
_ken = tbl["ken"].values.tolist()
# _timej = pd.date_range(start="202007040100", freq="30T", periods=3*(24)*2 + 11*2)
# _timeu = [ time - timedelta(hours=9) for time in _timej ]

# DIR="/home/griduser/work/sori-py2/timeWeather/dat/100571/code_x"
DIR_T="/home/griduser/work/sori-py2/timeWeather/dat/100571/code_t"



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

for code,name,ken in zip(_code,_name,_ken):
  col='tenminPrecip'
  use_col=["time",col]

  df = pd.read_csv(f"{DIR_T}/{code}.csv")
  df= df[use_col]
  df["time"] = pd.to_datetime(df["time"].astype(str)).apply(lambda x: x + timedelta(hours=9))
  df[col] = np.round(df[col]*3, 1)

  f,ax = plt.subplots(figsize=(22,8))
  bx = ax.twinx()



  rects = ax.bar(df["time"],df[col], color="b", label="30min precip")
  autoLabel(rects, ax)

  bx.plot(df["time"],df[col].cumsum(), color="r", label="precip CUMSUM")
  
  title=f"{ken}_{name}_{code}\n 0704 01:00 - 0707 11:30"
  title2=f"{ken}_{name}_{code}"
  ax.set_title(title, pad=-20)

  ax.legend(loc="upper left")
  bx.legend(loc = "best")


  # ax.plot()
  f.savefig(f"{OUTD}/{title2}.png", bbox_inches="tight")
  plt.close()
  # sys.exit()
  print("end",code)