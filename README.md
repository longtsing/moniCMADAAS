# 模拟天擎项目
模拟天擎API接口，提供气象数据服务

## 项目架构


## 环境搭建

```shell
mamba create -n fastapi python==3.11.11 fastapi uvicorn pydantic orjson ujson msgpack-python cryptography pyjwt redis-py urllib3 aiohttp httpx sqlmodel sqlacodegen mysql-connector-python cassandra-driver numpy pandas xarray geopandas scipy cartopy matplotlib cnmaps metpy cython numba  nb_conda  -c conda-forge -y
pip install cinrad  pyxxl
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
nohup fastapi run main.py --reload --host 0.0.0.0 --port 8000 --workers 4 &
```
## 防火墙开关
```shell
firewall-cmd --zone=public --add-port=8000/tcp --permanent
firewall-cmd --reload
firewall-cmd --list-all
```
