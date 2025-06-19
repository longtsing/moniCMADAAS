import os
import sys
from datetime import datetime, timedelta
import random
import json
import math
import numpy as np
import pandas as pd
import xarray as xr
from models.base import responseModel
import dateutil.parser
import dateutil.rrule
import functools

latStep = -0.125  # 纬度分辨率
lonStep = 0.125  # 经度分辨率


@functools.lru_cache
def getNafpEleGridByTimeAndLevelAndValidtime(**kwargs):
    """
    getNafpEleGridByTimeAndLevelAndValidtime(按起报时间、预报层次、预报时效检索预报要素场)
    """
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])
    repM = None
    time = kwargs.get('time', None)
    if time is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='times is required',
            requestParams=requestParams,
            DS=''
        )

    if repM is None:
        minLon = 0
        maxLon = 180.0
        minLat = 0.0625
        maxLat = 89.9375
        Lons = np.arange(minLon, maxLon+lonStep, lonStep)
        Lats = np.arange(maxLat, minLat+latStep, latStep)

        repM = responseModel(
            returnCode='0',
            returnMessage='Query Succeed',
            requestParams=requestParams,
            startLat=maxLat,
            endLat=minLat,
            startLon=minLon,
            endLon=maxLon,
            latCount=len(Lats),
            lonCount=len(Lons),
            latStep=latStep,
            lonStep=lonStep,
            fieldNames='文件名,文件格式,文件大小,存储路径,资料时间',
            DS=np.random.rand(len(Lats), len(Lons)).tolist()
        )
    return repM

@functools.lru_cache
def getNafpEleGridInRectByTimeAndLevelAndValidtime(**kwargs):
    """
    getNafpEleGridInRectByTimeAndLevelAndValidtime(按经纬范围、起报时间、预报层次、预报时效检索预报要素场)
    """
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])
    repM = None
    time = kwargs.get('time', None)
    if time is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='times is required',
            requestParams=requestParams,
            DS=''
        )
    minLon = kwargs.get('minLon', None)
    maxLon = kwargs.get('maxLon', None)
    minLat = kwargs.get('minLat', None)
    maxLat = kwargs.get('maxLat', None)
    if (minLat is None) or (minLon is None) or (maxLat is None) or (maxLon is None):
        repM = responseModel(
            returnCode='-2001',
            returnMessage='minLat, minLon, maxLat, maxLon are required',
            requestParams=requestParams,
            DS=''
        )

    if repM is None:
        minLon = float(minLon)
        maxLon = float(maxLon)
        minLat = float(minLat)
        maxLat = float(maxLat)
        Lons = np.arange(minLon, maxLon+lonStep, lonStep)
        Lats = np.arange(maxLat, minLat+latStep, latStep)

        repM = responseModel(
            returnCode='0',
            returnMessage='Query Succeed',
            requestParams=requestParams,
            startLat=maxLat,
            endLat=minLat,
            startLon=minLon,
            endLon=maxLon,
            latCount=len(Lats),
            lonCount=len(Lons),
            latStep=latStep,
            lonStep=lonStep,
            fieldNames='文件名,文件格式,文件大小,存储路径,资料时间',
            DS=np.random.rand(len(Lats), len(Lons)).tolist()

        )
    return repM

@functools.lru_cache
def getNafpEleAtPointByTimeAndLevelAndValidtime(**kwargs):
    """
    getNafpEleAtPointByTimeAndLevelAndValidtime(按起报时间、预报层次、预报时效、经纬度检索预报要素插值)
    """
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])
    repM = None
    time = kwargs.get('time', None)
    if time is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='times is required',
            requestParams=requestParams,
            DS=''
        )
    validTime = kwargs.get('validTime', None)
    if validTime is None:
        repM = responseModel(
            returnCode='-2001',
            returnMessage='validTime is required',
            requestParams=requestParams,
            DS=''
        )
    latLons = kwargs.get('latLons', None)
    if (latLons is None):
        repM = responseModel(
            returnCode='-2001',
            returnMessage='latLons are required',
            requestParams=requestParams,
            DS=''
        )

    if repM is None:
        latLons = latLons.split(',')
        latLons = [list(map(float, latLon.split('/'))) for latLon in latLons]
        time = dateutil.parser.parse(time)
        ds=[]
        for latLon in latLons:
            if len(latLon) != 2:
                continue
            lat, lon = latLon
            # 模拟数据
            ds.append({
                'lat': lat,
                'lon': lon,
                'datetime':time.strftime('%Y-%m-%d %H:%M:%S'),
                'validtime': validTime,
                'value':round(random.uniform(-30, 40),1),  # 模拟温度值
            })

        repM = responseModel(
            returnCode='0',
            returnMessage='Query Succeed',
            requestParams=requestParams,
            fieldNames='文件名,文件格式,文件大小,存储路径,资料时间',
            DS=ds

        )
    return repM
