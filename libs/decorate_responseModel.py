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
from configs import compressConfig

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
            response_code = 200
            try:
                response = await func(*args, **kwargs)
            except Exception as e:
                response = str(e)
                response_code = 500
            datetime_end = datetime.now()

            if(not isinstance(response, responseModel)):
                repM = responseModel(
                    code=response_code,
                    data=response,
                    costs=round((datetime_end - datetime_start).total_seconds() * 1000, 2)
                )
                return repM
            else:
                response.costs = round((datetime_end - datetime_start).total_seconds() * 1000, 2)
                return response

        async_wrapper.__signature__ = new_sig
        return async_wrapper
    
    else:
        # 同步函数装饰器
        @functools.wraps(func)
        def sync_wrapper(
                x_use_gzip: typing.Annotated[str, Header(description="如果您希望响应被 Gzip 压缩，请将此标题设置为True，否则，设置为False")] = 'false',
                *args, **kwargs
        ) -> responseModel:
            use_gzip = compressConfig.defaultCompress
            if compressConfig.defaultCompress:
                if x_use_gzip.lower() == 'false':
                    use_gzip = False
            else:
                if x_use_gzip.lower() == 'true':
                    use_gzip = True
            
            datetime_start = datetime.now()
            response_code = 200
            try:
                # 直接调用同步函数，不使用 await
                response = func(*args, **kwargs)
                if(isinstance(response, responseModel)):
                    if(use_gzip):
                        response.data = compressConfig.CompressFunc(response.data)
                else:
                    if(use_gzip):
                        response = compressConfig.CompressFunc(response)
            except Exception as e:
                response = str(e)
                response_code = 500
            datetime_end = datetime.now()

            if(not isinstance(response, responseModel)):
                repM = responseModel(
                    code=response_code,
                    data=response,
                    costs=round((datetime_end - datetime_start).total_seconds() * 1000, 2)
                )
                if(use_gzip):
                    repM.compressMethod = compressConfig.CompressFunc.__name__
                return repM
            else:
                response.costs = round((datetime_end - datetime_start).total_seconds() * 1000, 2)
                if(use_gzip):
                    response.compressMethod = compressConfig.CompressFunc.__name__
                return response

        sync_wrapper.__signature__ = new_sig
        return sync_wrapper
