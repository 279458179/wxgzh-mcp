# WXGZH-MCP 微信公众号管理容器

## 1. 项目概述

### 项目名称
wxgzh-mcp (微信公众号管理容器)

### 项目类型
基于Python和FastAPI的Web应用

### 核心功能
提供微信公众号API的Python封装，实现公众号内容管理、用户互动、消息处理等自动化功能。

### 目标用户
- 公众号运营者
- 内容创作者
- 需要自动化管理公众号的开发者

## 2. 功能列表

### 2.1 基础API功能
- ✅ 微信公众平台API身份认证（Access Token管理）
- ✅ 自动刷新和缓存Access Token
- ✅ 请求重试机制和错误处理

### 2.2 素材管理
- ✅ 临时素材上传（图片、语音、视频、缩略图）
- ✅ 永久素材管理（新增、获取、删除、修改）
- ✅ 素材计数查询
- ✅ 素材列表查询（图片、视频、语音、缩略图）

### 2.3 图文消息管理
- ✅ 新增永久图文素材
- ✅ 修改永久图文素材
- ✅ 删除永久图文素材
- ✅ 获取图文素材详情
- ✅ 图文消息预览

### 2.4 消息管理
- ✅ 群发消息（图文、文本、图片等）
- ✅ 模板消息发送
- ✅ 客服消息发送
- ✅ 自动回复规则管理

### 2.5 用户管理
- ✅ 用户列表获取
- ✅ 用户信息查询
- ✅ 用户标签管理
- ✅ 用户备注名设置
- ✅ 用户拉黑/取消拉黑

### 2.6 菜单管理
- ✅ 自定义菜单创建
- ✅ 自定义菜单查询
- ✅ 自定义菜单删除
- ✅ 个性化菜单管理

### 2.7 数据统计
- ✅ 用户分析数据
- ✅ 文章分析数据
- ✅ 消息分析数据
- ✅ 接口分析数据

## 3. 技术架构

### 3.1 技术栈
- **语言**: Python 3.9+
- **Web框架**: FastAPI
- **HTTP客户端**: httpx
- **数据处理**: Pydantic
- **异步支持**: asyncio
- **配置管理**: Python-dotenv
- **日志管理**: Python logging
- **测试框架**: pytest

### 3.2 项目结构
```
wxgzh-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── api/
│   │   ├── __init__.py
│   │   ├── client.py        # API客户端核心
│   │   ├── auth.py          # 认证管理
│   │   ├── materials.py     # 素材管理API
│   │   ├── articles.py      # 图文消息API
│   │   ├── messages.py      # 消息管理API
│   │   ├── users.py         # 用户管理API
│   │   ├── menus.py         # 菜单管理API
│   │   └── analytics.py     # 数据统计API
│   ├── models/
│   │   ├── __init__.py
│   │   ├── requests.py      # 请求模型
│   │   └── responses.py    # 响应模型
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py    # 自定义异常
│       └── helpers.py       # 辅助函数
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_materials.py
│   ├── test_articles.py
│   └── test_messages.py
├── .env.example
├── requirements.txt
├── pytest.ini
├── SPEC.md
└── README.md
```

## 4. API接口设计

### 4.1 RESTful API端点

#### 认证
- `GET /api/auth/token` - 获取当前access token状态

#### 素材管理
- `POST /api/materials/upload` - 上传临时素材
- `POST /api/materials/permanent` - 添加永久素材
- `GET /api/materials` - 获取素材列表
- `GET /api/materials/{media_id}` - 获取素材详情
- `DELETE /api/materials/{media_id}` - 删除素材

#### 图文消息
- `POST /api/articles` - 创建图文消息
- `GET /api/articles` - 获取图文消息列表
- `GET /api/articles/{media_id}` - 获取图文消息详情
- `PUT /api/articles/{media_id}` - 更新图文消息
- `DELETE /api/articles/{media_id}` - 删除图文消息
- `POST /api/articles/{media_id}/preview` - 预览图文消息

#### 消息管理
- `POST /api/messages/send` - 发送客服消息
- `POST /api/messages/broadcast` - 群发消息
- `POST /api/messages/template` - 发送模板消息

#### 用户管理
- `GET /api/users` - 获取用户列表
- `GET /api/users/{openid}` - 获取用户信息
- `PUT /api/users/{openid}` - 更新用户备注
- `GET /api/users/tags` - 获取用户标签
- `POST /api/users/tags` - 创建用户标签
- `POST /api/users/tags/{tag_id}` - 批量为用户打标签

#### 菜单管理
- `GET /api/menus` - 获取菜单
- `POST /api/menus` - 创建菜单
- `DELETE /api/menus` - 删除菜单

#### 数据统计
- `GET /api/analytics/users` - 用户分析数据
- `GET /api/analytics/articles` - 图文分析数据

## 5. 数据模型

### 5.1 核心模型
```python
# Access Token
{
    "access_token": "string",
    "expires_in": 7200,
    "refresh_time": "timestamp"
}

# 素材
{
    "media_id": "string",
    "type": "image|voice|video|thumb",
    "created_at": "timestamp",
    "name": "string",
    "url": "string"  # 永久图片素材有
}

# 图文消息
{
    "media_id": "string",
    "articles": [
        {
            "title": "string",
            "thumb_media_id": "string",
            "author": "string",
            "digest": "string",
            "show_cover_pic": 0|1,
            "content": "string",
            "content_source_url": "string"
        }
    ]
}

# 用户
{
    "openid": "string",
    "nickname": "string",
    "sex": 0|1|2,
    "province": "string",
    "city": "string",
    "country": "string",
    "headimgurl": "string",
    "subscribe_time": "timestamp",
    "remark": "string"
}
```

## 6. 配置管理

### 6.1 环境变量
```
WECHAT_APP_ID=           # 微信公众号AppID
WECHAT_APP_SECRET=       # 微信公众号AppSecret
WECHAT_TOKEN=            # 微信公众号Token（用于回调验证）
API_PORT=8000            # API服务端口
LOG_LEVEL=INFO           # 日志级别
TOKEN_CACHE_FILE=./token_cache.json  # Token缓存文件路径
```

## 7. 错误处理

### 7.1 自定义异常
- `WeChatAPIError` - API调用错误
- `AuthenticationError` - 认证错误
- `TokenExpiredError` - Token过期
- `RateLimitError` - 频率限制
- `InvalidParameterError` - 参数错误

### 7.2 重试机制
- 自动重试次数：3次
- 重试延迟：1秒、2秒、4秒（指数退避）
- 重试条件：网络错误、500错误、频率限制

## 8. 安全考虑

- 不在代码中硬编码AppID和AppSecret
- 所有敏感配置通过环境变量注入
- Token缓存文件权限控制
- API请求HTTPS加密
- 回调URL签名验证

## 9. 依赖版本

```
fastapi>=0.68.0
uvicorn>=0.15.0
httpx>=0.18.0
pydantic>=1.8.0
python-dotenv>=0.19.0
pytest>=6.2.0
pytest-asyncio>=0.15.0
```
