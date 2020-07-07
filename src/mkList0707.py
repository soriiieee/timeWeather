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
# from convSokuhouData import conv2allwithTime,conv2CutCols #(df),(df, ave=minutes,hour)
# from convAmedasData import conv2allwithTime,conv2CutCols #(df),(df, ave=minutes,hour)
from checkFileExistSize import checkFile #(input_path)
from plotMonthData import plotDayfor1Month #(df,_col,title=False)
from convKana2Roma import conv2romaji #(x, han=False)
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
# initial
#

DIR="/home/griduser/work/sori-py2/timeWeather/tbl"
input_path=f"{DIR}/ame_master.csv" 

if os.path.exists(input_path):
  tbl_ame = pd.read_csv(input_path)
  tbl_ame = tbl_ame[['観測所番号', '種類', 'ｶﾀｶﾅ名', '所在地', '緯度(度)', '緯度(分)','経度(度)', '経度(分)']]
  
  #convert
  tbl_ame["name"] = tbl_ame["ｶﾀｶﾅ名"].apply(lambda x: conv2romaji(x, han=True))
  tbl_ame["lat"] = tbl_ame["緯度(度)"] + tbl_ame["緯度(分)"]/60.
  tbl_ame["lon"] = tbl_ame["経度(度)"] + tbl_ame["経度(分)"]/60.
  tbl_ame["ken47"] = tbl_ame["観測所番号"].apply(lambda x: int(str(x)[:2]))
  # tbl_ame = tbl_ame[['観測所番号', '種類',"lat","lon","name"]]


  tbl_ame = tbl_ame[['観測所番号', '種類',"lat","lon","name","ken47"]]
  print(tbl_ame.head())
  tbl_ame.to_csv(f"{DIR}/tbl_ame.csv", index=False)
