# WXGZH-MCP

微信公众号管理容器 - 基于Python和FastAPI的微信公众号API封装

## 功能特性

- **素材管理**: 支持临时和永久素材的上传、获取、删除
- **图文消息**: 创建、编辑、删除、预览图文消息
- **消息管理**: 客服消息、群发消息、模板消息
- **用户管理**: 用户信息查询、标签管理、用户备注
- **菜单管理**: 自定义菜单创建、查询、删除
- **数据统计**: 用户分析、文章分析、消息分析

## 快速开始

### 环境要求

- Python 3.9+
- Docker (可选)

### 安装

1. 克隆仓库
```bash
git clone https://github.com/279458179/wxgzh-mcp.git
cd wxgzh-mcp
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的微信公众号 AppID 和 AppSecret
```

4. 运行服务
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Docker 部署

1. 配置环境变量
```bash
cd docker
cp .env.docker .env
# 编辑 .env 文件，填入你的微信公众号配置
```

2. 启动容器
```bash
docker-compose up -d
```

## API 文档

启动服务后访问: http://localhost:8000/docs

## 配置说明

在 `.env` 文件中配置以下环境变量:

```
WECHAT_APP_ID=你的微信公众号AppID
WECHAT_APP_SECRET=你的微信公众号AppSecret
WECHAT_TOKEN=验证Token(用于回调)
API_PORT=8000
LOG_LEVEL=INFO
```

## 运行测试

```bash
pytest tests/
```

## License

MIT License
