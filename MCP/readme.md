# 气象大数据云平台（天擎）MCP

## 环境配置
```bash
pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/
pip install langchain-core langchain-OpenAI langchain-community langgraph fastmcp nmc_met_io uv

```

## 调试命令

```bash
# 运行MCP Server
fastmcp run MCPServer.py  --transport sse --port 3001 --host 0.0.0.0
# http://101.35.88.42:3001/sse
nohup fastmcp run MCPServer.py  --transport sse --port 3001 --host 0.0.0.0 > mcpserver.log 2>&1 &



# 运行 MCP Inspector （本地前端调试）
npx @modelcontextprotocol/inspector

···
