# README
利用FastAPI构建Python微服务

## 资料
- [fastapi-learning-notes](https://github.com/Relph1119/fastapi-learning-notes/tree/master)
- [Building-Python-Microservices-with-FastAPI](https://github.com/PacktPublishing/Building-Python-Microservices-with-FastAPI/tree/main)

## 技术栈

### uv安装python依赖
```shell
# 安装uv
curl -Ls https://astral.sh/uv/install.sh | sh

# 创建虚拟环境并安装包依赖
uv venv .
uv pip install -r pyproject.toml

# 安装单个依赖
uv pip install fastapi
uv pip install "requests>=2.31"

# 查看安装了哪些包
uv pip freeze
uv pip list

# 检查哪些依赖要写入 .toml文件
uv pip install deptry
deptry .
```