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
import base64
from datetime import datetime, timedelta
import uvicorn
import json
from models.base import responseModel
from pydantic import BaseModel
import typing
from fastapi.responses import ORJSONResponse
from libs.decorate_responseModel import decorate_responseModel

root_path='/music-ws'
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
    description='模拟气象大数据云平台“天擎”的API服务，提供气象数据查询、下载等功能。',
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




#启动入口
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
