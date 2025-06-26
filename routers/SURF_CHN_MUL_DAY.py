import os
import sys
from datetime import datetime,timedelta
import random
import json
import math
import numpy as np
import pandas as pd
from models.base import responseModel
import dateutil.parser
import dateutil.rrule
import functools

stations=pd.read_csv(os.path.abspath(os.path.dirname(__file__)+'/../')+'/datas/Stations.csv', encoding='utf-8')
for c in ['Station_Id_C', 'Province', 'City', 'Cnty', 'Town','Admin_Code_CHN', 'Town_code', 'ProvinceCode', 'CityCode', 'CntyCode',]:
    stations[c]=stations[c].apply(lambda x:str(x))
elementDict={
    "Station_Id_C": {"name": "区站号(字符)", "unit": "-"},
    "Station_levl": {"name": "测站级别", "unit": "标识/代码表"},
    "Lat": {"name": "纬度", "unit": "°"},
    "Lon": {"name": "经度", "unit": "°"},
    "Alti": {"name": "测站高度", "unit": "m"},
    "Admin_Code_CHN": {"name": "行政编码", "unit": "标识/代码表"},
    "V_ACODE_4SEARCH": {"name": "行政编码2", "unit": "-"},
    "Town_code": {"name": "镇编码", "unit": "-"},
    "City": {"name": "地市名", "unit": "-"},
    "Station_Name": {"name": "站名", "unit": "-"},
    "Cnty": {"name": "区县名", "unit": "-"},
    "COUNTRYCODE": {"name": "国家代码", "unit": "-"},
    "Country": {"name": "国家名称", "unit": "-"},
    "NetCode": {"name": "站网代码", "unit": "-"},
    "Province": {"name": "省名", "unit": "-"},
    "REGIONCODE": {"name": "区域代码", "unit": "-"},
    "Town": {"name": "乡镇名", "unit": "-"},
    "DATA_ID": {"name": "资料标识", "unit": "-"},
    "Datetime": {"name": "数据时间", "unit": "标识/代码表"},
    "IYMDHM": {"name": "入库时间", "unit": "-"},
    "RECORD_ID": {"name": "记录标识ID", "unit": "-"},
    "D_RETAIN_ID": {"name": "记录标识", "unit": "-"},
    "RYMDHM": {"name": "数据收到时间", "unit": "-"},
    "D_SOURCE_ID": {"name": "数据来源", "unit": "-"},
    "UPDATE_TIME": {"name": "数据更新时间", "unit": "-"},
    "Q_PRE_Arti_Enc_CYC": {"name": "人工加密观测降水量描述时间周期质控码", "unit": "标识/代码表"},
    "Q_WEP_Past_CYC": {"name": "过去天气描述时间周期质控码", "unit": "标识/代码表"},
    "Q04080_05_1": {"name": "过去天气描述时间周期计算值质控码", "unit": "标识/代码表"},
    "Q_PRS": {"name": "气压质控码", "unit": "标识/代码表"},
    "Q_PRS_Sea": {"name": "海平面气压质量控制标志", "unit": "标识/代码表"},
    "Q_PRS_Change_3h": {"name": "3小时变压质控码", "unit": "标识/代码表"},
    "Q_PRS_Change_24h": {"name": "24小时变压质控码", "unit": "标识/代码表"},
    "Q_PRS_Max": {"name": "日最高本站气压质控码", "unit": "标识/代码表"},
    "Q_PRS_Max_OTime": {"name": "日最高本站气压出现时间质控码", "unit": "标识/代码表"},
    "Q_PRS_Min": {"name": "日最低本站气压质控码", "unit": "标识/代码表"},
    "Q_PRS_Min_OTime": {"name": "日最低本站气压出现时间质控码", "unit": "标识/代码表"},
    "Q_WIN_D": {"name": "风向质控码", "unit": "标识/代码表"},
    "Q_WIN_S": {"name": "风速质控码", "unit": "标识/代码表"},
    "Q_WIN_S_Max": {"name": "日最大风速质控码", "unit": "标识/代码表"},
    "Q_WIN_S_Max_OTime": {"name": "日最大风速出现时间质控码", "unit": "标识/代码表"},
    "Q_WIN_S_Inst_Max": {"name": "日极大风速质控码", "unit": "标识/代码表"},
    "Q_WIN_S_INST_Max_OTime": {"name": "日极大风速出现时间质控码", "unit": "标识/代码表"},
    "Q_WIN_D_INST": {"name": "瞬时风向(角度)质控码", "unit": "标识/代码表"},
    "Q_WIN_S_INST": {"name": "瞬时风速质控码", "unit": "标识/代码表"},
    "Q_WIN_D_INST_Max": {"name": "日极大风速的风向质控码", "unit": "标识/代码表"},
    "Q_WIN_D_Avg_2mi": {"name": "2分钟平均风向质控码值", "unit": "标识/代码表"},
    "Q_WIN_S_Avg_2mi": {"name": "2分钟平均风速成质控码值", "unit": "标识/代码表"},
    "Q_WIN_D_Avg_10mi": {"name": "10分钟风向质控码", "unit": "标识/代码表"},
    "Q_WIN_S_Avg_10mi": {"name": "10分钟平均风速质控码", "unit": "标识/代码表"},
    "Q_WIN_D_S_Max": {"name": "日最大风速的风向质控码", "unit": "标识/代码表"},
    "Q_WIN_D_Inst_Max_6h": {"name": "过去6小时极大瞬时风向质控码", "unit": "标识/代码表"},
    "Q_WIN_D_Inst_Max_12h": {"name": "过去12小时极大瞬时风向质控码", "unit": "标识/代码表"},
    "Q_WIN_S_Inst_Max_6h": {"name": "过去6小时极大瞬时风速质控码", "unit": "标识/代码表"},
    "Q_WIN_S_Inst_Max_12h": {"name": "过去12小时极大瞬时风速质控码", "unit": "标识/代码表"},
    "Q_TEM": {"name": "温度/气温质控码", "unit": "标识/代码表"},
    "Q_DPT": {"name": "露点温度质控码", "unit": "标识/代码表"},
    "Q_TEM_Max": {"name": "日最高气温质控码", "unit": "标识/代码表"},
    "Q_TEM_Max_OTime": {"name": "日最高气温出现时间质控码", "unit": "标识/代码表"},
    "Q_TEM_Min": {"name": "1小时内最低气温质控码", "unit": "标识/代码表"},
    "Q_TEM_Min_OTime": {"name": "小时内最低气温出现时间质控码", "unit": "标识/代码表"},
    "Q_GST_Min_12h": {"name": "过去12小时最低地面温度质控码", "unit": "标识/代码表"},
    "Q_TEM_Max_24h": {"name": "过去24小时最高气温质控码", "unit": "标识/代码表"},
    "Q_TEM_Min_24h": {"name": "过去24小时最低气温质控码", "unit": "标识/代码表"},
    "Q_GST_5cm": {"name": "5cm地温质控码", "unit": "标识/代码表"},
    "Q_GST_10cm": {"name": "10cm地温质控码", "unit": "标识/代码表"},
    "Q_GST_15cm": {"name": "15cm地温质控码", "unit": "标识/代码表"},
    "Q_GST_20cm": {"name": "20cm地温质控码", "unit": "标识/代码表"},
    "Q_GST_40Cm": {"name": "40cm地温质控码", "unit": "标识/代码表"},
    "Q_GST_80cm": {"name": "80cm地温质控码", "unit": "标识/代码表"},
    "Q_GST_160cm": {"name": "160cm地温质控码", "unit": "标识/代码表"},
    "Q_GST_320cm": {"name": "320cm地温质控码", "unit": "标识/代码表"},
    "Q_GST": {"name": "地面温度质控码", "unit": "标识/代码表"},
    "Q_GST_Min": {"name": "日最低地面温度质控码", "unit": "标识/代码表"},
    "Q_GST_Min_OTime": {"name": "日最低地面温度出现时间质控码", "unit": "标识/代码表"},
    "Q_GST_Max": {"name": "日最高地面温度质控码", "unit": "标识/代码表"},
    "Q_GST_Max_Otime": {"name": "日最高地面温度出现时间质控码", "unit": "标识/代码表"},
    "Q_LGST": {"name": "草面（雪面）温度质控码", "unit": "标识/代码表"},
    "Q_LGST_Max": {"name": "日草面（雪面）最高温度质控码", "unit": "标识/代码表"},
    "Q_LGST_Max_OTime": {"name": "日草面（雪面）最高温度出现时间质控码", "unit": "标识/代码表"},
    "Q_LGST_Min": {"name": "日草面（雪面）最低温度质控码", "unit": "标识/代码表"},
    "Q_LGST_Min_OTime": {"name": "日草面（雪面）最低温度出现时间质控码", "unit": "标识/代码表"},
    "Q_TEM_ChANGE_24h": {"name": "24小时变温质控码", "unit": "标识/代码表"},
    "Q_RHU": {"name": "相对湿度质控码", "unit": "标识/代码表"},
    "Q_VAP": {"name": "水汽压质控码", "unit": "标识/代码表"},
    "Q_RHU_Min": {"name": "最小相对湿度质控码", "unit": "标识/代码表"},
    "Q_RHU_Min_OTIME": {"name": "最小相对湿度出现时间质控码", "unit": "标识/代码表"},
    "Q_PRE": {"name": "分钟降水量质控码", "unit": "标识/代码表"},
    "Q_Snow_Depth": {"name": "积雪深度质控码", "unit": "标识/代码表"},
    "Q_PRE_1h": {"name": "小时降水量质控码", "unit": "标识/代码表"},
    "Q_PRE_3h": {"name": "过去3小时降水量质控码", "unit": "标识/代码表"},
    "Q_PRE_6h": {"name": "过去6小时降水量质控码", "unit": "标识/代码表"},
    "Q_PRE_12h": {"name": "过去12小时降水量质控码", "unit": "标识/代码表"},
    "Q_PRE_24h": {"name": "24小时降水量质控码", "unit": "标识/代码表"},
    "Q_EVP_Big": {"name": "日蒸发量（大型）质控码", "unit": "标识/代码表"},
    "Q_Snow_PRS": {"name": "积雪雪压质控码", "unit": "标识/代码表"},
    "Q_VIS": {"name": "水平能见度质控码", "unit": "标识/代码表"},
    "Q_VIS_HOR_1MI": {"name": "1分钟平均水平能见度质控码", "unit": "标识/代码表"},
    "Q_VIS_HOR_10MI": {"name": "10分钟平均水平能见度质控码", "unit": "标识/代码表"},
    "Q_WEP_Now": {"name": "现在天气质控码", "unit": "标识/代码表"},
    "Q20003_1": {"name": "现在天气计算值质控码", "unit": "标识/代码表"},
    "Q_WEP_Past_1": {"name": "过去天气1质控码", "unit": "标识/代码表"},
    "Q20004_1": {"name": "过去天气1计算值质控码", "unit": "标识/代码表"},
    "Q_WEP_Past_2": {"name": "过去天气2质控码", "unit": "标识/代码表"},
    "Q20005_1": {"name": "过去天气2计算值质控码", "unit": "标识/代码表"},
    "Q_CLO_Cov": {"name": "总云量质控码", "unit": "标识/代码表"},
    "Q_CLO_COV_LM": {"name": "低云或中云的云量质控码", "unit": "标识/代码表"},
    "Q_CLO_Height_LoM": {"name": "云底高度质控码", "unit": "标识/代码表"},
    "Q_CLO_Cov_Low": {"name": "低云量质控码", "unit": "标识/代码表"},
    "Q_VIS_Min": {"name": "日最小水平能见度质控码", "unit": "标识/代码表"},
    "Q_VIS_Min_OTime": {"name": "日最小水平能见度出现时间质控码", "unit": "标识/代码表"},
    "Q_SCO": {"name": "地面状态质控码", "unit": "标识/代码表"},
    "Q20214": {"name": "冰雹的最大重量质控码", "unit": "标识/代码表"},
    "Q_Dew": {"name": "露是否出现质控码", "unit": "标识/代码表"},
    "Q_Frost": {"name": "霜是否出现质控码", "unit": "标识/代码表"},
    "Q_ICE": {"name": "结冰是否出现质控码", "unit": "标识/代码表"},
    "Q_GSS": {"name": "积雪是否出现质控码", "unit": "标识/代码表"},
    "Q_SoRi": {"name": "雾凇是否出现质控码", "unit": "标识/代码表"},
    "Q_Glaze": {"name": "雨凇是否出现质控码", "unit": "标识/代码表"},
    "Q20303_1": {"name": "天气现象摘要计算值质控码", "unit": "标识/代码表"},
    "Q20304_1": {"name": "天气现象记录计算值质控码", "unit": "标识/代码表"},
    "Q_EICE": {"name": "电线积冰-现象质控码", "unit": "标识/代码表"},
    "Q_EICET_NS": {"name": "电线积冰-南北方向厚度质控码", "unit": "标识/代码表"},
    "Q_EICET_WE": {"name": "电线积冰-东西方向厚度质控码", "unit": "标识/代码表"},
    "Q_EICEW_NS": {"name": "电线积冰-南北方向重量质控码", "unit": "标识/代码表"},
    "Q_EICEW_WE": {"name": "电线积冰-东西方向重量质控码", "unit": "标识/代码表"},
    "Q_EICED_NS": {"name": "电线积冰-南北方向直径质控码", "unit": "标识/代码表"},
    "Q_EICED_WE": {"name": "电线积冰-东西方向直径质控码", "unit": "标识/代码表"},
    "Q_FRS_1st_Top": {"name": "第一冻土层上界值质控码", "unit": "标识/代码表"},
    "Q_FRS_2nd_Top": {"name": "第二冻土层上界值质控码", "unit": "标识/代码表"},
    "Q_FRS_1st_Bot": {"name": "第一冻土层下界值质控码", "unit": "标识/代码表"},
    "Q_FRS_2nd_Bot": {"name": "第二冻土层下界值质控码", "unit": "标识/代码表"},
    "Q_CLO_FOME_1": {"name": "云状1质控码", "unit": "标识/代码表"},
    "Q_CLO_Fome_2": {"name": "云状2质控码", "unit": "标识/代码表"},
    "Q_CLO_Fome_3": {"name": "云状3质控码", "unit": "标识/代码表"},
    "Q_CLO_Fome_4": {"name": "云状4质控码", "unit": "标识/代码表"},
    "Q_CLO_FOME_5": {"name": "云状5质控码", "unit": "标识/代码表"},
    "Q_CLO_FOME_6": {"name": "云状6质控码", "unit": "标识/代码表"},
    "Q_CLO_FOME_7": {"name": "云状7质控码", "unit": "标识/代码表"},
    "Q_CLO_Fome_8": {"name": "云状8质控码", "unit": "标识/代码表"},
    "Q_CLO_Fome_Low": {"name": "低云状质控码", "unit": "标识/代码表"},
    "Q_CLO_Fome_MID": {"name": "中云状质控码", "unit": "标识/代码表"},
    "Q_CLO_Fome_High": {"name": "高云状质控码", "unit": "标识/代码表"},
    "Station_Id_d": {"name": "区站号/观测平台标识(数字)", "unit": "-"},
    "Station_Type": {"name": "测站类型", "unit": "标识/代码表"},
    "V02175": {"name": "降水测量方法", "unit": "标识/代码表"},
    "V02176": {"name": "地面状态测量方法", "unit": "-"},
    "V02177": {"name": "积雪深度的测量方法", "unit": "标识/代码表"},
    "V02180": {"name": "天气现象检测系统", "unit": "标识/代码表"},
    "V02183": {"name": "云探测系统", "unit": "标识/代码表"},
    "Year": {"name": "年", "unit": "-"},
    "Mon": {"name": "月", "unit": "-"},
    "Day": {"name": "日", "unit": "-"},
    "Hour": {"name": "时", "unit": "时"},
    "PRE_Arti_Enc_CYC": {"name": "人工加密观测降水量描述周期", "unit": "hour"},
    "WEP_Past_CYC": {"name": "过去天气描述事件周期", "unit": "hour"},
    "V04080_05_1": {"name": "过去天气描述时间周期计算值", "unit": "-"},
    "PRS_Sensor_Alti": {"name": "气压传感器海拔高度", "unit": "m"},
    "TEM_RHU_Sensor_Heigh": {"name": "温湿传感器距地高度", "unit": "m"},
    "VIS_Sensor_Heigh": {"name": "能见度传感器距地高度", "unit": "m"},
    "WIN_S_Sensor_Heigh": {"name": "风速传感器距地面高度", "unit": "m"},
    "V08010": {"name": "地面限定符（温度数据）", "unit": "标识/代码表"},
    "PRS": {"name": "气压", "unit": "hPa"},
    "PRS_Sea": {"name": "海平面气压", "unit": "hPa"},
    "PRS_Change_3h": {"name": "3小时变压", "unit": "hPa"},
    "PRS_Change_24h": {"name": "24小时变压", "unit": "hPa"},
    "PRS_Max": {"name": "最高本站气压", "unit": "hPa"},
    "PRS_Max_OTime": {"name": "最高本站气压出现时间", "unit": "-"},
    "PRS_Min": {"name": "最低本站气压", "unit": "hPa"},
    "PRS_Min_OTime": {"name": "最低本站气压出现时间", "unit": "-"},
    "WIN_D": {"name": "风向", "unit": "°"},
    "WIN_S": {"name": "风速", "unit": "m·s-1"},
    "WIN_S_Max": {"name": "最大风速", "unit": "米/秒"},
    "WIN_S_Max_OTime": {"name": "最大风速出现时间", "unit": "-"},
    "WIN_S_Inst_Max": {"name": "极大风速", "unit": "米/秒"},
    "WIN_S_INST_Max_OTime": {"name": "极大风速出现时间", "unit": "-"},
    "WIN_D_INST": {"name": "瞬时风向(角度)", "unit": "°"},
    "WIN_S_INST": {"name": "瞬时风速", "unit": "米/秒"},
    "WIN_D_INST_Max": {"name": "极大风速的风向(角度)", "unit": "°"},
    "WIN_D_Avg_2mi": {"name": "2分钟平均风向(角度)", "unit": "°"},
    "WIN_S_Avg_2mi": {"name": "2分钟平均风速", "unit": "m-s"},
    "WIN_D_Avg_10mi": {"name": "10分钟平均风向(角度)", "unit": "°"},
    "WIN_S_Avg_10mi": {"name": "10分钟平均风速", "unit": "m-s"},
    "WIN_D_S_Max": {"name": "日最大风速的风向(角度)", "unit": "°"},
    "WIN_D_Inst_Max_6h": {"name": "过去6小时极大瞬时风向", "unit": "°"},
    "WIN_D_Inst_Max_12h": {"name": "过去12小时极大瞬时风向", "unit": "°"},
    "WIN_S_Inst_Max_6h": {"name": "过去6小时极大瞬时风速", "unit": "m-s"},
    "WIN_S_Inst_Max_12h": {"name": "过去12小时极大瞬时风速", "unit": "m-s"},
    "TEM": {"name": "温度/气温", "unit": "℃"},
    "DPT": {"name": "露点温度", "unit": "℃"},
    "TEM_Max": {"name": "最高气温", "unit": "℃"},
    "TEM_Max_OTime": {"name": "最高气温出现时间", "unit": "-"},
    "TEM_Min": {"name": "最低气温", "unit": "℃"},
    "TEM_Min_OTime": {"name": "最低气温出现时间", "unit": "-"},
    "GST_Min_12h": {"name": "过去12小时地面最低温度", "unit": "℃"},
    "TEM_Max_24h": {"name": "过去24小时最高气温", "unit": "℃"},
    "TEM_Min_24h": {"name": "过去24小时最低气温", "unit": "℃"},
    "GST_5cm": {"name": "5cm地温", "unit": "℃"},
    "GST_10cm": {"name": "10cm地温", "unit": "℃"},
    "GST_15cm": {"name": "15cm地温", "unit": "℃"},
    "GST_20cm": {"name": "20cm地温", "unit": "℃"},
    "GST_40Cm": {"name": "40cm地温", "unit": "℃"},
    "GST_80cm": {"name": "80cm地温", "unit": "℃"},
    "GST_160cm": {"name": "160cm地温", "unit": "℃"},
    "GST_320cm": {"name": "320cm地温", "unit": "℃"},
    "GST": {"name": "地面温度", "unit": "℃"},
    "GST_Min": {"name": "最低地面温度", "unit": "℃"},
    "GST_Min_OTime": {"name": "最低地面温度出现时间", "unit": "-"},
    "GST_Max": {"name": "最高地面温度", "unit": "℃"},
    "GST_Max_Otime": {"name": "最高地面温度出现时间", "unit": "-"},
    "LGST": {"name": "草面(雪面)温度", "unit": "℃"},
    "LGST_Max": {"name": "草面(雪面)最高温度", "unit": "℃"},
    "LGST_Max_OTime": {"name": "草面(雪面)最高温度出现时间", "unit": "-"},
    "LGST_Min": {"name": "草面(雪面)最低温度", "unit": "℃"},
    "LGST_Min_OTime": {"name": "草面(雪面)最低温度出现时间", "unit": "-"},
    "TEM_ChANGE_24h": {"name": "过去24小时变温", "unit": "℃"},
    "RHU": {"name": "相对湿度", "unit": "%"},
    "VAP": {"name": "水汽压", "unit": "hPa"},
    "RHU_Min": {"name": "最小相对湿度", "unit": "%"},
    "RHU_Min_OTIME": {"name": "最小相对湿度出现时间", "unit": "-"},
    "PRE": {"name": "降水量", "unit": "mm"},
    "Snow_Depth": {"name": "积雪深度计算值", "unit": "cm"},
    "PRE_1h": {"name": "过去1小时降水量", "unit": "mm"},
    "PRE_3h": {"name": "过去3小时降水量", "unit": "mm"},
    "PRE_6h": {"name": "过去6小时降水量", "unit": "mm"},
    "PRE_12h": {"name": "过去12小时降水量", "unit": "mm"},
    "PRE_24h": {"name": "过去24小时降水量", "unit": "mm"},
    "EVP_Big": {"name": "蒸发(大型)", "unit": "mm"},
    "V13196": {"name": "蒸发水位", "unit": "-"},
    "Snow_PRS": {"name": "积雪雪压", "unit": "g/cm2"},
    "VIS": {"name": "水平能见度(人工)", "unit": "m"},
    "VIS_HOR_1MI": {"name": "1分钟平均能见度", "unit": "m"},
    "VIS_HOR_10MI": {"name": "10分钟平均能见度", "unit": "m"},
    "WEP_Now": {"name": "现在天气", "unit": "标识/代码表"},
    "V20003_1": {"name": "现在天气计算值", "unit": "-"},
    "WEP_Past_1": {"name": "过去天气1", "unit": "标识/代码表"},
    "V20004_1": {"name": "过去天气1计算值", "unit": "-"},
    "WEP_Past_2": {"name": "过去天气2", "unit": "标识/代码表"},
    "V20005_1": {"name": "过去天气2计算值", "unit": "-"},
    "CLO_Cov": {"name": "总云量计算值", "unit": "%"},
    "CLO_COV_LM": {"name": "云量(低云或中云)", "unit": "%"},
    "CLO_Height_LoM": {"name": "云底高度计算值", "unit": "m"},
    "CLO_Cov_Low": {"name": "低云量", "unit": "%"},
    "VIS_Min": {"name": "最小水平能见度", "unit": "m"},
    "VIS_Min_OTime": {"name": "最小水平能见度出现时间", "unit": "-"},
    "SCO": {"name": "地面状态", "unit": "标识/代码表"},
    "V20214": {"name": "冰雹重量", "unit": "-"},
    "Dew": {"name": "露是否出现计算值", "unit": "标识/代码表"},
    "Frost": {"name": "霜是否出现计算值", "unit": "标识/代码表"},
    "ICE": {"name": "结冰是否出现计算值", "unit": "标识/代码表"},
    "GSS": {"name": "积雪是否出现计算值", "unit": "标识/代码表"},
    "SoRi": {"name": "雾凇是否出现计算值", "unit": "标识/代码表"},
    "Glaze": {"name": "雨凇是否出现计算值", "unit": "标识/代码表"},
    "V20303_1": {"name": "天气现象摘要计算值", "unit": "-"},
    "WEP_Record": {"name": "天气现象记录", "unit": "-"},
    "V20304_1": {"name": "天气现象记录计算值", "unit": "-"},
    "EICE": {"name": "电线积冰-现象是否出现计算值", "unit": "标识/代码表"},
    "EICET_NS": {"name": "电线积冰-南北方向厚度", "unit": "m"},
    "EICET_WE": {"name": "电线积冰-东西方向厚度", "unit": "m"},
    "EICEW_NS": {"name": "电线积冰-南北方向重量", "unit": "1g/m"},
    "EICEW_WE": {"name": "电线积冰-东西方向重量", "unit": "1g/m"},
    "EICED_NS": {"name": "电线积冰-南北方向直径", "unit": "m"},
    "EICED_WE": {"name": "电线积冰-东西方向直径", "unit": "m"},
    "FRS_1st_Top": {"name": "第一冻土层上界值计算值", "unit": "cm"},
    "FRS_2nd_Top": {"name": "第二冻土层上界值计算值", "unit": "cm"},
    "FRS_1st_Bot": {"name": "第一冻土层下界值计算值", "unit": "cm"},
    "FRS_2nd_Bot": {"name": "第二冻土层下界值计算值", "unit": "cm"},
    "CLO_FOME_1": {"name": "云状1", "unit": "标识/代码表"},
    "CLO_Fome_2": {"name": "云状2", "unit": "标识/代码表"},
    "CLO_Fome_3": {"name": "云状3", "unit": "标识/代码表"},
    "CLO_Fome_4": {"name": "云状4", "unit": "标识/代码表"},
    "CLO_FOME_5": {"name": "云状5", "unit": "标识/代码表"},
    "CLO_FOME_6": {"name": "云状6", "unit": "标识/代码表"},
    "CLO_FOME_7": {"name": "云状7", "unit": "标识/代码表"},
    "CLO_FOME_8": {"name": "云状8", "unit": "标识/代码表"},
    "CLO_Fome_Low": {"name": "低云状", "unit": "标识/代码表"},
    "CLO_Fome_MID": {"name": "中云状", "unit": "标识/代码表"},
    "CLO_Fome_High": {"name": "高云状", "unit": "标识/代码表"},
    "REP_CORR_ID": {"name": "更正报标志", "unit": "-"},
    "RETAIN1": {"name": "保留字段1", "unit": "-"},
    "V_RETAIN10": {"name": "保留字段10", "unit": "-"},
    "RETAIN2": {"name": "保留字段2", "unit": "-"},
    "RETAIN3": {"name": "保留字段3", "unit": "-"},
    "V_RETAIN4": {"name": "保留字段4", "unit": "-"},
    "V_RETAIN5": {"name": "保留字段5", "unit": "-"},
    "V_RETAIN6": {"name": "保留字段6", "unit": "-"},
    "V_RETAIN7": {"name": "保留字段7", "unit": "-"},
    "V_RETAIN8": {"name": "保留字段8", "unit": "-"},
    "V_RETAIN9": {"name": "保留字段9", "unit": "-"},
    "V_RETAIN_OLD1": {"name": "保留字段旧1", "unit": "-"},
    "V_RETAIN_OLD10": {"name": "保留字段旧10", "unit": "-"},
    "V_RETAIN_OLD11": {"name": "保留字段旧11", "unit": "-"},
    "V_RETAIN_OLD12": {"name": "保留字段旧12", "unit": "-"},
    "V_RETAIN_OLD13": {"name": "保留字段旧13", "unit": "-"},
    "V_RETAIN_OLD14": {"name": "保留字段旧14", "unit": "-"},
    "V_RETAIN_OLD2": {"name": "保留字段旧2", "unit": "-"},
    "V_RETAIN_OLD3": {"name": "保留字段旧3", "unit": "-"},
    "V_RETAIN_OLD4": {"name": "保留字段旧4", "unit": "-"},
    "V_RETAIN_OLD5": {"name": "保留字段旧5", "unit": "-"},
    "V_RETAIN_OLD6": {"name": "保留字段旧6", "unit": "-"},
    "V_RETAIN_OLD7": {"name": "保留字段旧7", "unit": "-"},
    "V_RETAIN_OLD8": {"name": "保留字段旧8", "unit": "-"},
    "V_RETAIN_OLD9": {"name": "保留字段旧9", "unit": "-"}
}    

@functools.lru_cache
def getSurfEleInRegionByTime(**kwargs):
    '''
    getSurfEleInRegionByTime(按时间、地区检索地面要素数据)
    '''
    times=kwargs.get('times', None)
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])   
    repM = None
    if times is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='times is required',
            requestParams=requestParams,
            DS=''
        )
    adminCodes = kwargs.get('adminCodes', None)
    elements0 = kwargs.get('elements', None)
    if adminCodes is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='adminCodes is required',
            requestParams=requestParams,
            DS=''
        )
    if elements0 is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='elements is required',
            requestParams=requestParams,
            DS=''
        )
    if repM is None:
        times=times.split(',')
        adminCodes=adminCodes.split(',')
        stations_filtered0 = stations.copy()
        stations_filtered0=stations_filtered0[(stations_filtered0['ProvinceCode'].isin(adminCodes))|(stations_filtered0['CityCode'].isin(adminCodes))|(stations_filtered0['CntyCode'].isin(adminCodes))]
        print(f"筛选后的站点数量: {len(stations_filtered0)}")
        elements=list(set(elements0.split(','))-set(stations_filtered0.columns)-set(['Datetime']))
        dfs=[]
        
        for time in times:
            dtime=dateutil.parser.parse(time)
            stations_filtered=stations_filtered0.copy()
            data = {}
            for element in elements:
                data[element] = np.round(np.random.randint(0,100,size=len(stations_filtered))/10,1)
            
            data= pd.DataFrame(data,index=stations_filtered.index)   
            data=pd.concat([stations_filtered, data], axis=1)     
            data['Datetime'] = dtime.strftime('%Y-%m-%d %H:%M:%S')
            data['Year'] = dtime.year
            data['Mon'] = dtime.month
            data['Day'] = dtime.day
            data['Hour'] = dtime.hour            
            dfs.append(data)
        ds=pd.concat(dfs)
        fieldNames=[]
        for c in ds.columns:
            if(not c in  elements0.split(',')):
                ds.drop(c, axis=1, inplace=True)
            else:                
                if(c in elementDict):
                    fieldNames.append(elementDict[c]['name'])
        ds=ds[elements0.split(',')]
        repM = responseModel(
            returnCode='0',
            returnMessage='Query Succeed',
            requestParams=requestParams,
            rowCount=len(ds),
            colCount=len(ds.columns),
            fieldNames=','.join(fieldNames),
            DS=json.loads(ds.to_json(orient='records'))
        )
    return repM

@functools.lru_cache
def getSurfEleInRectByTime(**kwargs):
    
    '''
    getSurfEleInRectByTime(按时间、经纬度范围检索地面数据要素)
    '''
    times=kwargs.get('times', None)
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])   
    repM = None
    if times is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='times is required',
            requestParams=requestParams,
            DS=''
        )
    elements0 = kwargs.get('elements', None)
    if elements0 is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='elements is required',
            requestParams=requestParams,
            DS=''
        )
    minLat=kwargs.get('minLat', None)
    minLon=kwargs.get('minLon', None)
    maxLat=kwargs.get('maxLat', None)
    maxLon=kwargs.get('maxLon', None)
    if( minLat is None) or (minLon is None) or (maxLat is None) or (maxLon is None):
        repM = responseModel(
            returnCode='-2001',
            returnMessage='minLat, minLon, maxLat, maxLon are required',
            requestParams=requestParams,
            DS=''
        )

    if repM is None:
        times=times.split(',')
        stations_filtered0 = stations.copy()
        minLon= float(minLon)
        maxLon= float(maxLon)
        minLat= float(minLat)
        maxLat= float(maxLat)
        stations_filtered0=stations_filtered0[(stations_filtered0['Lon']>=minLon) & (stations_filtered0['Lon']<=maxLon) & (stations_filtered0['Lat']>=minLat) & (stations_filtered0['Lat']<=maxLat)]
        print(f"筛选后的站点数量: {len(stations_filtered0)}")
        elements=list(set(elements0.split(','))-set(stations_filtered0.columns)-set(['Datetime']))
        dfs=[]
        
        for time in times:
            dtime=dateutil.parser.parse(time)
            stations_filtered=stations_filtered0.copy()
            data = {}
            for element in elements:
                data[element] = np.round(np.random.randint(0,100,size=len(stations_filtered))/10,1)
            
            data= pd.DataFrame(data,index=stations_filtered.index)   
            data=pd.concat([stations_filtered, data], axis=1)  
            data['Datetime'] = dtime.strftime('%Y-%m-%d %H:%M:%S')
            data['Year'] = dtime.year
            data['Mon'] = dtime.month
            data['Day'] = dtime.day
            data['Hour'] = dtime.hour            
            dfs.append(data)
        ds=pd.concat(dfs)
        fieldNames=[]
        for c in ds.columns:
            if(not c in  elements0.split(',')):
                ds.drop(c, axis=1, inplace=True)
            else:                
                if(c in elementDict):
                    fieldNames.append(elementDict[c]['name'])
        ds=ds[elements0.split(',')]
        repM = responseModel(
            returnCode='0',
            returnMessage='Query Succeed',
            requestParams=requestParams,
            rowCount=len(ds),
            colCount=len(ds.columns),
            fieldNames=','.join(fieldNames),
            DS=json.loads(ds.to_json(orient='records'))
        )
    return repM

@functools.lru_cache
def getSurfEleByTimeAndStaID(**kwargs):
    
    '''
    getSurfEleByTimeAndStaID(按时间、站号检索地面数据要素)
    '''
    times=kwargs.get('times', None)
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])   
    repM = None
    if times is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='times is required',
            requestParams=requestParams,
            DS=''
        )
    elements0 = kwargs.get('elements', None)
    if elements0 is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='elements is required',
            requestParams=requestParams,
            DS=''
        )
    staIds=kwargs.get('staIds', None)
    if( staIds is None) or (len(staIds)==0):
        repM = responseModel(
            returnCode='-2001',
            returnMessage='staIds are required',
            requestParams=requestParams,
            DS=''
        )

    if repM is None:
        times=times.split(',')
        stations_filtered0 = stations.copy()
        staIds=staIds.split(',')
        stations_filtered0=stations_filtered0[stations_filtered0['Station_Id_C'].isin(staIds)]
        print(f"筛选后的站点数量: {len(stations_filtered0)}")
        elements=list(set(elements0.split(','))-set(stations_filtered0.columns)-set(['Datetime']))
        dfs=[]
        
        for time in times:
            dtime=dateutil.parser.parse(time)
            stations_filtered=stations_filtered0.copy()
            data = {}
            for element in elements:
                data[element] = np.round(np.random.randint(0,100,size=len(stations_filtered))/10,1)
            
            data= pd.DataFrame(data,index=stations_filtered.index)   
            data=pd.concat([stations_filtered, data], axis=1)     
            data['Datetime'] = dtime.strftime('%Y-%m-%d %H:%M:%S')
            data['Year'] = dtime.year
            data['Mon'] = dtime.month
            data['Day'] = dtime.day
            data['Hour'] = dtime.hour     
            dfs.append(data)
        ds=pd.concat(dfs)
        fieldNames=[]
        for c in ds.columns:
            if(not c in  elements0.split(',')):
                ds.drop(c, axis=1, inplace=True)
            else:                
                if(c in elementDict):
                    fieldNames.append(elementDict[c]['name'])
        ds=ds[elements0.split(',')]
        repM = responseModel(
            returnCode='0',
            returnMessage='Query Succeed',
            requestParams=requestParams,
            rowCount=len(ds),
            colCount=len(ds.columns),
            fieldNames=','.join(fieldNames),
            DS=json.loads(ds.to_json(orient='records'))
        )
    return repM

@functools.lru_cache
def getSurfEleByTimeRangeAndStaID(**kwargs):
    
    '''
    getSurfEleByTimeRangeAndStaID(按时间段、站号检索地面数据要素)
    '''
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])   
    repM = None
    elements0 = kwargs.get('elements', None)
    if elements0 is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='elements is required',
            requestParams=requestParams,
            DS=''
        )
    staIds=kwargs.get('staIds', None)
    if (repM is None) and (( staIds is None) or (len(staIds)==0)):
        repM = responseModel(
            returnCode='-2001',
            returnMessage='staIds are required',
            requestParams=requestParams,
            DS=''
        )

    timeRange=kwargs.get('timeRange', None)
    if (repM is None) and (timeRange is None):
        repM = responseModel(
            returnCode='-3001',
            returnMessage='. detail: the first time cannot bigger than last time {timeRange}',
            requestParams=requestParams,
            DS=''
        )
    if(repM is None):        
        timeRange=timeRange.replace('[','').replace(']','').split(',')
        dt_start=dateutil.parser.parse(timeRange[0])
        dt_end=dateutil.parser.parse(timeRange[1])
        if dt_end<= dt_start:
            repM = responseModel(
                returnCode='-2001',
                returnMessage='timeRange start must  is required',
                requestParams=requestParams,
                DS=''
            )

    if repM is None:

        times=list(dateutil.rrule.rrule(
            dateutil.rrule.DAILY,
            dtstart=dt_start,
            until=dt_end
        ))
        times=times[:100]  # 限制查询时间范围为100天内
        stations_filtered0 = stations.copy()
        staIds=staIds.split(',')
        stations_filtered0=stations_filtered0[stations_filtered0['Station_Id_C'].isin(staIds)]
        print(f"筛选后的站点数量: {len(stations_filtered0)}")
        elements=list(set(elements0.split(','))-set(stations_filtered0.columns)-set(['Datetime']))
        dfs=[]
        
        for time in times:
            stations_filtered=stations_filtered0.copy()
            data = {}
            for element in elements:
                data[element] = np.round(np.random.randint(0,100,size=len(stations_filtered))/10,1)
            
            data= pd.DataFrame(data,index=stations_filtered.index)   
            data=pd.concat([stations_filtered, data], axis=1)     
            data['Datetime'] = time.strftime('%Y-%m-%d %H:%M:%S')
            data['Year'] = time.year
            data['Mon'] = time.month
            data['Day'] = time.day
            data['Hour'] = time.hour     
            dfs.append(data)
        ds=pd.concat(dfs)
        fieldNames=[]
        for c in ds.columns:
            if(not c in  elements0.split(',')):
                ds.drop(c, axis=1, inplace=True)
            else:                
                if(c in elementDict):
                    fieldNames.append(elementDict[c]['name'])
        ds=ds[elements0.split(',')]
        repM = responseModel(
            returnCode='0',
            returnMessage='Query Succeed',
            requestParams=requestParams,
            rowCount=len(ds),
            colCount=len(ds.columns),
            fieldNames=','.join(fieldNames),
            DS=json.loads(ds.to_json(orient='records'))
        )
    return repM
