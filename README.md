# 气象大数据云平台（天擎）模拟及MCP服务项目
模拟天擎API接口，提供气象数据服务；基于模拟API、nmc_met_io、FastMCP开发天擎数据获取MCPServer（SSE协议）

## contributors
longtsing


## 项目架构
基于 FastAPI web框架
各文件夹作用:
- configs ：相关配置信息，诸如访问的账号密码
- datas : 相关数据存储，大多为csv格式
- libs ： 访问装饰器等web框架相关支持模块
- models ： 数据模型，主要为天擎返回数据模型
- routers ： 各数据库、接口实现代码
- statics ： swaggerUI 的静态资源
- test : 开发时的一些测试 jupyter 代码
- examples : 基于 nmc_met_io 如何调用获取数据的测试 jupyter 案例

main.py 是模拟天擎的程序的入口

MCP 文件夹下是基于 FastMCP 开发的天擎数据获取MCPServer（SSE协议）

## 环境搭建
由于使用了部分编译后的资源，所以选择采用 mamba 或 conda 管理运行环境
```shell
mamba create -n fastapi python==3.11.11 fastapi uvicorn pydantic orjson ujson msgpack-python cryptography pyjwt redis-py urllib3 aiohttp httpx sqlmodel sqlacodegen mysql-connector-python cassandra-driver numpy pandas xarray geopandas scipy cartopy matplotlib cnmaps metpy cython numba  nb_conda  -c conda-forge -y
pip install cinrad  pyxxl fastmcp nmc_met_io
# linux 下
pip install uvloop
mamba install libuv xemsf -c conda-forge -y
```

## 系统运行
开发模式
```shell
uvicorn main:app --reload
fastapi dev main.py
```

运行模式
```shell
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 &
nohup fastapi run main.py --reload --host 0.0.0.0 --port 8000 --workers 4 > ./web.log 2>&1 &
```
## 防火墙开关
linux 下 firewalld 防火墙
```shell
firewall-cmd --zone=public --add-port=8000/tcp --permanent
firewall-cmd --reload
firewall-cmd --list-all
```
