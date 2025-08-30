# typersonal FastAPI 服务

这是一个基于 FastAPI 的 AI 字体生成服务，集成了 typersonal 模型。

## 🚀 快速启动

### 方法 1: 使用最终启动脚本 (强烈推荐)
```bash
# Windows 批处理文件
start_final.bat

# PowerShell 脚本
.\start_final.ps1
```

### 方法 2: 使用基础启动脚本
```bash
# Windows 批处理文件
start_server.bat

# PowerShell 脚本
.\start_server.ps1
```

### 方法 3: 手动启动
```bash
# 激活环境
conda activate typersonal

# 启动服务器
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📋 环境检查

在启动服务之前，建议先检查环境配置：

```bash
# 使用 typersonal 环境中的 Python
C:\Users\HackathonUser\miniconda3\envs\typersonal\python.exe check_environment.py
```

## 🌐 服务端点

启动成功后，服务将在以下地址运行：

- **主服务**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **交互式文档**: http://localhost:8000/redoc

### 主要 API 端点

#### 1. 根路径
- `GET /` - 服务状态检查
- `GET /users` - 获取用户列表
- `POST /users` - 创建新用户

#### 2. AI 生成端点
- `POST /8000/ai/generate` - 生成字体图像
  - 参数: `character` (字符), `sampling_step` (采样步数), `reference_image` (参考图像)
  
- `POST /8000/ai/blend` - 混合字体风格
  - 参数: `character` (字符), `style_option` (风格选项), `alpha` (透明度), `thickness` (粗细), `image_a` (图像)

## 🔧 配置说明

### 环境要求
- Python 3.10.18
- PyTorch 2.2.2 (CPU 版本)
- FastAPI 0.99.1
- Uvicorn 0.34.0

### 依赖包
所有依赖包已在 `requirements_fastapi_ai.txt` 中指定，并已安装在 `typersonal` 环境中。

### 模型路径
服务会自动查找 `../typersonal` 目录中的模型文件。

## 📁 文件结构

```
fastapi/
├── main.py                 # FastAPI 主应用
├── ai_router.py           # AI 相关路由
├── db/                    # 数据库相关
├── start_server.bat       # Windows 启动脚本
├── start_server.ps1       # PowerShell 启动脚本
├── check_environment.py   # 环境检查脚本
├── requirements_fastapi_ai.txt  # 依赖包列表
└── README.md              # 本文件
```

## 🧪 测试 API

### 使用测试脚本 (推荐)
```bash
# 使用 typersonal 环境中的 Python
C:\Users\HackathonUser\miniconda3\envs\typersonal\python.exe test_api.py
```

### 使用 curl 测试

#### 测试服务状态
```bash
curl http://localhost:8000/
```

#### 测试用户列表
```bash
curl http://localhost:8000/users
```

### 使用 Python 测试

```python
import requests

# 测试服务状态
response = requests.get("http://localhost:8000/")
print(response.json())

# 测试用户列表
response = requests.get("http://localhost:8000/users")
print(response.json())
```

## 🚨 故障排除

### 常见问题

1. **环境激活失败**
   - 确保已安装 conda
   - 检查 `typersonal` 环境是否存在
   - 运行 `conda env list` 查看环境

2. **模块导入错误**
   - 检查 `../typersonal` 目录是否存在
   - 确保 typersonal 环境中的包已正确安装
   - 运行 `check_environment.py` 检查依赖

3. **端口占用**
   - 检查 8000 端口是否被占用
   - 使用 `netstat -an | findstr 8000` 检查
   - 修改启动脚本中的端口号

4. **模型加载失败**
   - 检查 typersonal 目录中的模型文件
   - 确保模型文件路径正确
   - 检查模型文件是否完整

### 日志查看

启动服务后，控制台会显示详细的日志信息，包括：
- 请求处理状态
- 图像处理过程
- 错误信息

## 🔄 开发模式

服务默认以开发模式运行，支持：
- 自动重载代码更改
- 详细的错误信息
- 热重载

## 📊 性能优化

由于使用 CPU 版本的 PyTorch：
- 推理速度适中
- 适合中小型模型
- 建议使用较小的图像尺寸

## 🤝 贡献

如需修改或扩展功能：
1. 修改相应的 Python 文件
2. 服务会自动重载
3. 测试新功能
4. 提交更改

---

**服务启动后，可以通过浏览器访问 http://localhost:8000/docs 查看完整的 API 文档！** 🎉
