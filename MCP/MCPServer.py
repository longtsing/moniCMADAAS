from fastmcp import FastMCP
import os
import sys
from datetime import datetime, timedelta
import json
import math
import numpy as np
import pandas as pd
import dateutil.parser
import dateutil.rrule
import nmc_met_io
import nmc_met_io.retrieve_cmadaas
import nmc_met_io.retrieve_cmadaas_history
import datamaps

mcp = FastMCP(name="气象大数据云平台（天擎）数据MCPServer")

@mcp.tool("get_datetime_now")
def get_datetime_now():
    """
    获取当前时间
    :return: 当前时间字符串，格式为：YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool("get_ProvinceCode")
def get_ProvinceCode(province: str):
    """
    根据中文省名获取省份行政编码
    :param province: 省份名全称
    :return: 省份行政编码
    """

    return (
        datamaps.province2CodeMaps[province]
        if province in datamaps.province2CodeMaps
        else "未找到该省编码，请输入省份全称"
    )


@mcp.tool("get_province_representative_station")
def get_province_representative_station(province: str):
    """
    根据中文省名获取该省份的代表站点
    :param province: 省份名全称
    :return: 代表站点站号
    """
    
    return (
        datamaps.province2StationCodeMaps[province]
        if province in datamaps.province2StationCodeMaps
        else "未找到该省代表站，请输入省份全称"
    )


@mcp.tool("get_CityCode")
def get_CityCode(city: str):
    """
    根据中文省名和城市名获取城市行政编码
    :param city: 省份名+城市名全称，例如：湖北省宜昌市
    :return: 城市行政编码
    """

    return (
        datamaps.city2CodeMaps[city]
        if city in datamaps.city2CodeMaps
        else "未找到该城市编码，请输入省份名+城市名全称，例如：湖北省宜昌市"
    )


@mcp.tool("get_city_representative_station")
def get_city_representative_station(city: str):
    """
    根据中文省名和城市名获取该城市代表站点
    :param city: 省份名+城市名全称，例如：湖北省宜昌市
    :return: 代表站点站号
    """
    
    return (
        datamaps.city2StationCodeMaps[city]
        if city in datamaps.city2StationCodeMaps
        else "未找到该城市代表站，请输入省份名+城市名全称，例如：湖北省宜昌市"
    )


@mcp.tool("get_areaCode_Hourly_data")
def get_areaCode_Hourly_data(
    adminCodes: str, times: str
):
    """
    根据行政编码获取指定时间的小时气象观测数据
    :param adminCodes: 行政编码，如湖北省行政编码420000，又如湖北省宜昌市行政编码420500
    :param times: 观测时间 ,格式：20250625170000 ；也可以是以逗号分割的多个时间，如：20250625170000,20250625180000
    :return: 小时气象观测数据
    """
    # set retrieve parameters

    contents =nmc_met_io.retrieve_cmadaas.get_rest_result(
        'getSurfEleInRegionByTime',
        {        
            'dataCode': 'SURF_CHN_MUL_HOR_N',        
            'elements': "Station_Id_C,Lat,Lon,Alti,Year,Mon,Day,Hour,PRS_sea,TEM,DPT,RHU,PRE_1h,PRE_12h,PRE_24h",
            'times': times,
            'adminCodes': adminCodes,
            'orderby': "Datetime:ASC"
        },
    )
    contents = nmc_met_io.retrieve_cmadaas._load_contents(contents)
    data = pd.DataFrame(contents['DS'])
    if (data is None) or (len(data) == 0):
        return "未找到该省的小时观测数据，请检查省份编码和时间字符串内容"
    else:
        return data.rename(columns=datamaps.elementmaps).to_dict(orient="records")


@mcp.tool("get_stations_times_Hourly_data")
def get_stations_times_Hourly_data(
    stations: str, times: str
):
    """
    根据站号指定时间的小时气象观测数据
    :param stations: 站点站号,例如：57461；也可以是以逗号分割的多个站号，如：57461,53871
    :param times: 观测时间 ,格式：20250625170000 ；也可以是以逗号分割的多个时间，如：20250625170000,20250625180000
    :return: 小时气象观测数据
    """
    # set retrieve parameters

    contents =nmc_met_io.retrieve_cmadaas.get_rest_result(
        'getSurfEleByTimeAndStaID',
        {        
            'dataCode': 'SURF_CHN_MUL_HOR_N',        
            'elements': "Station_Id_C,Lat,Lon,Alti,Year,Mon,Day,Hour,PRS_sea,TEM,DPT,RHU,PRE_1h,PRE_12h,PRE_24h",
            'times': times,
            'staIds': stations,
            'orderby': "Datetime:ASC"
        },
    )
    contents = nmc_met_io.retrieve_cmadaas._load_contents(contents)
    data = pd.DataFrame(contents['DS'])
    if (data is None) or (len(data) == 0):
        return "未找到该省的小时观测数据，请检查省份编码和时间字符串内容"
    else:
        return data.rename(columns=datamaps.elementmaps).to_dict(orient="records")

@mcp.tool("get_station_timeRange_Hourly_data")
def get_station_timeRange_Hourly_data(
    station: str, StartTime: str, EndTime: str
):
    """
    根据站号获取该站指定时间段内的逐小时观测数据
    :param station: 站点站号,例如：57461；也可以是以逗号分割的多个站号，如：57461,53871
    :param StartTime: 观测开始时间 ,格式：20250625170000
    :param EndTime: 观测结束时间,格式：20250625200000
    :return: 逐小时观测数据
    """
    # set retrieve parameters

    data = nmc_met_io.retrieve_cmadaas.cmadaas_obs_by_time_range_and_id(
        f'[{StartTime},{EndTime}]',
        data_code="SURF_CHN_MUL_HOR_N",
        elements="Station_Id_C,Lat,Lon,Alti,Year,Mon,Day,Hour,PRS_sea,TEM,DPT,RHU,PRE_1h,PRE_12h,PRE_24h",
        sta_ids=station,
    )
    if (data is None) or (len(data) == 0):
        return "未找到该站点的逐小时观测数据，请检查站号和时间范围"
    else:
        return data.rename(columns=datamaps.elementmaps).to_dict(orient="records")


@mcp.tool("get_station_YearsDaily_data")
def get_station_YearsDaily_data(
    station: str, StartYear: int, EndYear: int
):
    """
    根据站号获取指定时间段内的逐日观测数据
    :param station: 站点站号,例如：57461
    :param StartYear: 数据起始年份，例如：2022
    :param EndYear: 数据结束年份，例如：2025
    :return: 起始到结束年份之间逐日观测数据
    """
    # set retrieve parameters

    data = data = nmc_met_io.retrieve_cmadaas_history.get_hist_obs_id(
        years=np.arange(StartYear, EndYear+1,1), 
        data_code='SURF_CHN_MUL_DAY', 
        elements='Station_Id_C,Datetime,Lat,Lon,Alti,TEM_Avg,TEM_Max,TEM_Min,PRE_Time_2020,PRE_Time_0808,WIN_S_2mi_Avg,WIN_S_Max', 
        sta_ids=station
        )
    if (data is None) or (len(data) == 0):
        return "未找到该站点的逐小时观测数据，请检查站号和时间范围"
    else:
        return data.rename(columns=datamaps.elementmaps).to_dict(orient="records")

@mcp.tool("get_GFS_Forecast_TMP_2M")
def get_GFS_Forecast_TMP_2M(
    lat: str, lon: str
):
    """
    获取指定经纬度点的未来7天气温预报
    :param lat: 纬度，例如：39.9042
    :param lon: 经度，例如：116.4074
    :return: 未来7天气温逐日预报数据
    """
    data=nmc_met_io.retrieve_cmadaas.cmadaas_model_points(    
        'NAFP_ANA_FTM_GRAPES_GFS_NEHE', 
        datetime.now().strftime('%Y%m%d08'), 
        [24, 48, 72, 96, 120, 144, 168], 
        'TEM', 0,1,
        {
            'lon':list(map(float,lon.split(','))), 'lat':list(map(float,lat.split(',')))
        },
        cache=False
    )
    
    if (data is None) or (len(data) == 0):
        return "未找到GFS预报数据，请检查和经纬度"
    else:
        return '未来的的气温预测为：'+'℃,'.join(map(str,np.round(data.data.values,1).flatten().tolist()))+'℃'




@mcp.resource("data://version")
def version():
    """
    获取MCPServer版本信息
    :return: MCPServer版本信息
    """
    return {
        "version": 0.8,
        "name": mcp.name,
    }


@mcp.resource("data://all_provinces")
def all_provinces():
    """
    获取所有省的名称
    :return: 所有省全称列表
    """
    return list(datamaps.province2CodeMaps.keys())






if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=3001, transport="sse")
