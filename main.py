import inspect
import os
import os.path
import sys
sys.path.append(os.path.dirname(__file__))
#以上代码作用是将项目根目录添加到系统路径中，以便于在其他模块中导入自定义模块
import typing
from fastapi import FastAPI, applications, Request, Response, Depends,Header,Query
from fastapi.openapi.docs import get_swagger_ui_html,get_redoc_html
from fastapi.responses import  JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import uvicorn
import json
from models.base import responseModel
from pydantic import BaseModel
import typing
from fastapi.responses import ORJSONResponse
from libs.decorate_responseModel import decorate_responseModel
from models.base import responseModel
import fnmatch
import hashlib
import pickle
import urllib.request
import uuid
import warnings
import logging
import traceback
import configs.UserConfig as userConfig
import importlib

root_path='/music-ws'
logger=logging.getLogger('fastapi')

startTime=datetime.now()

def swagger_ui_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url=f'./statics/swagger-ui/swagger-ui-bundle.js',
        swagger_css_url=f'./statics/swagger-ui/swagger-ui.css',
        swagger_favicon_url=f'./statics/swagger-ui/favicon.png',
    )

def redoc_ui_path(*args,**kwargs):
    return get_redoc_html(
        *args,**kwargs,
        redoc_js_url=f'./statics/swagger-ui/redoc.standalone.js',
        redoc_favicon_url=f'./statics/swagger-ui/favicon.png',
    )

applications.get_swagger_ui_html=swagger_ui_patch
applications.get_redoc_html=redoc_ui_path

#设置网站服务对象
app = FastAPI(
    root_path=root_path,
    title='模拟天擎平台',
    description='模拟气象大数据云平台“天擎”的API服务，提供气象数据查询、下载等功能。'+\
    'demo 用户 userId:heywhale passwd:doUp',
    version='1.1.0',
    docs_url='/doc.html',
    redoc_url=None,
    contact={
        'name':'longtsing',
        'url':'https://github.com/longtsing',
        'email':'longtsing@cug.edu.cn'
    },
    license_info={
        'name':'Apache 2.0',
        'url':'http://www.apache.org/licenses/LICENSE-2.0.html'
    },
    default_response_class=ORJSONResponse,
)
#挂载静态资源区
app.mount('/statics', StaticFiles(directory=os.path.dirname(__file__)+'/statics/'), name='static')
app.mount('/datas', StaticFiles(directory=os.path.dirname(__file__)+'/datas/'), name='datas')
#添加允许跨域访问中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#默认入口，返回网站基本信息
@app.get(
    "/",
    summary='平台运行信息'
)
@decorate_responseModel
async def index(request: Request):
    webinfo={
        'title':app.title,
        'description':app.description,
        'version':app.version,
        'startTime':startTime.strftime('%Y-%m-%d %H:%M:%S'),
        'Datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return webinfo


#默认入口，返回网站基本信息
@app.get(
    "/api",
    summary='数据检索核心入口',
    description='模拟天擎平台的核心数据检索接口，提供气象数据查询、下载等功能。' +\
    '该接口支持多种查询参数，包括服务节点ID、数据代码、接口ID、用户ID、时间戳、随机数和签名等。' +\
    '用户可以通过这些参数进行精确的数据检索，返回结果包括查询状态码、消息、请求参数等信息。' +\
    '可选参数包括密码等，具体使用方法请参考API文档。'+\
    'demo 用户 userId:heywhale passwd:doUp'
)
@decorate_responseModel
async def api(
    request: Request,
): 
    
    kwargs = dict(request.query_params)
    requestParams = '&'.join([key+'='+str(kwargs[key]) for key in kwargs])   
    try:
        #必选参数
        serviceNodeId= kwargs.get('serviceNodeId', None)
        dataCode= kwargs.get('dataCode', None)
        interfaceId= kwargs.get('interfaceId', None)
        userId = kwargs.get('userId', None)
        timestamp = kwargs.get('timestamp', None)
        nonce = kwargs.get('nonce', None)
        sign= kwargs.get('sign', None)
        # 可选参数
        pwd= kwargs.get('pwd', None) 
        # 模拟天擎账号检索
        users=list(filter(lambda useri:useri['userId']==userId,userConfig.Users))
        repM=None
        if(len(users)<1):
            repM = responseModel(
                returnCode='-1',
                returnMessage='User Not Found',
                requestParams=requestParams,
                DS=''
            )
        # 检查提交的时间戳是否在30分钟内，当提交了pwd 会绕过这个逻辑，转为传统 music 接口验证逻辑
        if(pwd is None):            
            # 提交时间戳转换为 datetime 对象
            requestDT=datetime.fromtimestamp(int(timestamp) / 1000)
            # 天擎验证逻辑，检查提交时间戳是否在30分钟内
            if(repM is None and requestDT < datetime.now() - timedelta(minutes=30)):
                repM = responseModel(
                    returnCode='-1',
                    returnMessage='Request Timeout',
                    requestParams=requestParams,
                    DS=''
                )
        if(repM is None):
            user=users[0]
            if(pwd is  None):
                # 如果没有提交密码，则需要验证签名
                # 这是天擎平台在 music 接口基础上的新增签名验证逻辑
                sign_params = kwargs.copy()
                del sign_params['sign']
                sign_params['pwd'] = user['pwd'].strip()
                keys = sorted(sign_params)
                sign_str=''
                for key in keys:
                    sign_str = sign_str + key + "=" + str(sign_params.get(key)).strip() + "&"
                sign_str = sign_str[:-1]
                sign_hash = hashlib.md5(sign_str.encode(encoding='UTF-8')).hexdigest().upper()
                if sign_hash != sign:
                    repM = responseModel(
                        returnCode='-1',
                        returnMessage='Sign Error',
                        requestParams=requestParams,
                        DS=''
                    )
            else:
                # 如果提交了密码，则直接验证密码是否正确
                # 传统 music 接口验证逻辑
                if(pwd!=user['pwd']):
                    repM = responseModel(
                        returnCode='-1',
                        returnMessage='Password Error',
                        requestParams=requestParams,
                        DS=''
                    )

            if repM is None:
                # 到这里表示通过了用户验证
                logger.info(f"Query Succeed: {requestParams}")

                # 采用动态加载方式每个 routers 下的 py 文件代表一类气象数据，具体接口由文件内定义的函数实现
                # 注意：每个 routers 下的 py 文件名必须与 dataCode 相同，且文件内必须定义与 interfaceId 相同的函数
        
                if(os.path.exists(os.path.join(os.path.dirname(__file__),'routers',f'{dataCode}.py'))):
                    module_name= f'routers.{dataCode}'
                    if not module_name in sys.modules:
                        module = importlib.import_module(f'routers.{dataCode}')
                    else:
                        module = sys.modules[module_name]
                    print(hasattr(module, interfaceId))
                    if hasattr(module, interfaceId):
                        interface_func = getattr(module, interfaceId)
                        # 同步函数调用
                        if(inspect.iscoroutinefunction(interface_func)):
                            # 异步函数调用
                            repM = await interface_func(**kwargs)
                        else:
                            # 同步函数调用
                            repM = interface_func(**kwargs)
                    else:
                        repM = responseModel(
                            returnCode='-2001',
                            returnMessage=f'. detail: dataCode {dataCode} not define the interface {interfaceId}',
                            requestParams=requestParams,
                            DS=''
                        )

        if(repM is None):
            repM = responseModel(
                returnCode='-2000',
                # 天擎当访问未定义数据集时会报这个错误
                returnMessage=f'. detail: dataCode {dataCode} not define the interface {interfaceId}',
                requestParams=requestParams,
                DS=''
            )


    
    except Exception as e:
        logger.error(f"Error in api: {e}"+traceback.format_exc())
        repM = responseModel(
            returnCode='-1',
            returnMessage=str(e),
            requestParams=requestParams,
            DS=''
        )

    return repM




#启动入口
if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=8000)
