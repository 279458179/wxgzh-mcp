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

## API 文档

启动服务后访问: http://localhost:8000/docs

### 认证

- `GET /api/auth/token` - 获取Token状态
- `POST /api/auth/token/refresh` - 刷新Token

### 素材管理

- `POST /api/materials/upload` - 上传临时素材
- `POST /api/materials/permanent` - 添加永久素材
- `GET /api/materials` - 获取素材列表
- `DELETE /api/materials/{media_id}` - 删除素材

### 图文消息

- `POST /api/articles` - 创建图文消息
- `GET /api/articles` - 获取图文消息列表
- `PUT /api/articles/{media_id}` - 更新图文消息
- `DELETE /api/articles/{media_id}` - 删除图文消息
- `POST /api/articles/{media_id}/preview` - 预览图文消息

### 消息管理

- `POST /api/messages/send` - 发送客服消息
- `POST /api/messages/broadcast` - 群发消息
- `POST /api/messages/template` - 发送模板消息

### 用户管理

- `GET /api/users` - 获取用户列表
- `GET /api/users/{openid}` - 获取用户信息
- `PUT /api/users/{openid}` - 更新用户备注
- `GET /api/users/tags` - 获取用户标签
- `POST /api/users/tags` - 创建用户标签

### 菜单管理

- `GET /api/menus` - 获取菜单
- `POST /api/menus` - 创建菜单
- `DELETE /api/menus` - 删除菜单

### 数据统计

- `GET /api/analytics/users` - 用户分析
- `GET /api/analytics/articles` - 图文分析

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

## 项目结构

```
wxgzh-mcp/
├── src/
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── api/                 # API模块
│   │   ├── client.py        # API客户端核心
│   │   ├── auth.py          # 认证管理
│   │   ├── materials.py     # 素材管理
│   │   ├── articles.py      # 图文消息
│   │   ├── messages.py      # 消息管理
│   │   ├── users.py         # 用户管理
│   │   ├── menus.py         # 菜单管理
│   │   └── analytics.py     # 数据统计
│   ├── models/              # 数据模型
│   └── utils/               # 工具函数
├── tests/                   # 单元测试
├── requirements.txt         # 依赖包
└── README.md                # 使用说明
```

## 注意事项

1. 请妥善保管你的 AppID 和 AppSecret，不要泄露给他人
2. 公众号 API 有调用频率限制，请合理使用
3. 部分功能需要微信公众号认证后才能使用

## License

MIT License
