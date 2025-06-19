import functools
import inspect
import typing
import base64
import gzip
import json
import orjson
from fastapi import FastAPI, applications, Request, Response, Depends, Header, Query
from models.base import responseModel
from datetime import datetime, timedelta

def decorate_responseModel(func):
    '''
    为端点函数统一定义返回类型的装饰器函数
    :param func : 端点函数，支持同步和异步函数

    注意：
    1、fastapi 使用 inspect.signature 获取函数签名
    2、修改函数的 __signature__ 可以修改函数的签名
    3、修改函数的 __annotations__['return'] 可以修改函数的返回类型
    '''
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    new_sig = sig.replace(parameters=params).replace(return_annotation=responseModel)

    # 检查函数是否为异步函数
    is_async = inspect.iscoroutinefunction(func)
    
    if is_async:
        # 异步函数装饰器
        @functools.wraps(func)
        async def async_wrapper(
            *args, **kwargs
        ) -> responseModel:            
            
            datetime_start = datetime.now()
            response_code = '0'
            try:
                response = await func(*args, **kwargs)
            except Exception as e:
                response = str(e)
                response_code = '-1'
            datetime_end = datetime.now()

            if(not isinstance(response, responseModel)):
                repM = responseModel(
                    returnCode=response_code,
                    DS=response,
                    requestTime=datetime_start.strftime('%Y-%m-%d %H:%M:%S'),
                    responseTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    takeTime=round((datetime_end - datetime_start).total_seconds(), 3)
                )
                return repM
            else:
                response.requestTime=datetime_start.strftime('%Y-%m-%d %H:%M:%S')
                response.responseTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                response.takeTime = round((datetime_end - datetime_start).total_seconds() , 3)
                return response

        async_wrapper.__signature__ = new_sig
        return async_wrapper
    
    else:
        # 同步函数装饰器
        @functools.wraps(func)
        def sync_wrapper(
                *args, **kwargs
        ) -> responseModel:
            datetime_start = datetime.now()
            response_code = '0'
            try:
                # 直接调用同步函数，不使用 await
                response = func(*args, **kwargs)
            except Exception as e:
                response = str(e)
                response_code = '-1'
            datetime_end = datetime.now()

            if(not isinstance(response, responseModel)):
                repM = responseModel(
                    returnCode=response_code,
                    DS=response,
                    requestTime=datetime_start.strftime('%Y-%m-%d %H:%M:%S'),
                    responseTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    takeTime=round((datetime_end - datetime_start).total_seconds() , 3)
                )
                return repM
            else:
                response.requestTime=datetime_start.strftime('%Y-%m-%d %H:%M:%S')
                response.responseTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                response.takeTime = round((datetime_end - datetime_start).total_seconds() , 3)
                return response

        sync_wrapper.__signature__ = new_sig
        return sync_wrapper
