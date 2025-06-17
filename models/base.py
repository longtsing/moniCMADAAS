from pydantic import BaseModel, Field
import typing
from typing import TypeVar, Generic

T = TypeVar('T')  # 定义类型变量

class responseModel(BaseModel, Generic[T]):
    returnCode: typing.Annotated[int, Field(description='响应状态码')]
    returnMessage: typing.Annotated[str, Field(description='响应状态信息，通常为“成功”或错误信息')]
    rowCount: typing.Annotated[int, Field(description='响应数据行数，通常为查询结果的数量')] = 0
    colCount: typing.Annotated[int, Field(description='响应数据列数，通常为查询结果的字段数量')] = 0
    requestParams: typing.Annotated[dict, Field(description='请求参数，通常为查询条件或其他相关参数')] = {}
    requestTime: typing.Annotated[str, Field(description='请求时间，通常为ISO格式的时间字符串')] = ''
    responseTime: typing.Annotated[str, Field(description='响应时间，通常为ISO格式的时间字符串')] = ''
    takeTime: typing.Annotated[float, Field(description='请求处理时间，单位为秒')] = 0.0
    fieldNames: typing.Annotated[typing.List[str], Field(description='响应数据的字段名称列表')] = []
    fieldUnits: typing.Annotated[typing.List[str], Field(description='响应数据的字段单位列表')] = []
    DS:typing.Annotated[T, Field(description='响应内容，类型由泛型参数 T 决定')]
