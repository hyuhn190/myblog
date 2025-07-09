# 🧑‍💻 Django 博客系统项目文档

> 一个基于 Django 的博客平台，支持用户登录、阅读计数统计、缓存优化与异步任务处理。

---

## 📌 项目简介

这是一个功能完善的 **Django 博客系统**，包含以下核心模块：

- 用户注册与登录
- 博客文章展示与详情查看
- 阅读量统计（Redis 缓存 + 异步落库）
- 缓存命中率监控
- Celery 定时任务同步缓存数据到数据库

该项目适用于学习 Django Web 开发、缓存优化、异步任务调度等实践场景。

---

## 🧩 核心功能

### 1. 用户管理
- 注册 / 登录 / 登出
- 自动跳转支持 `?next=` 参数
- 注册成功页面自动跳转

> 使用 Django 内置认证系统，安全性高。

### 2. 博客系统
- 展示所有博客列表
- 查看单篇博客内容
- 每位用户阅读次数独立统计
- 总访问量、独立访客数、当前用户阅读次数实时显示

> 基于 Django ORM 实现，结合 Redis 缓存提升性能。

### 3. 阅读统计（高性能设计）
- 使用 Redis 缓存记录阅读行为（`incr`, `sadd`）
- 统计维度：
  - 总阅读量
  - 独立访客数（UV）
  - 当前用户阅读次数
- 定期通过 Celery 同步缓存数据到 MySQL 数据库

> 采用缓存前置设计，保证高并发下的性能表现。

### 4. 缓存监控
- 提供接口 `/myblogs/stats/` 返回缓存命中率数据
- 支持定时打印缓存命中率日志（通过 [log_cache_stats](file://E:\django\blog\myblog\management\commands\log_cache_stats.py#L0-L0) 命令）

### 5. 异步任务
- 使用 Celery + Redis 实现异步任务队列
- 定时将 Redis 中的阅读统计落库至 MySQL

```python
@shared_task
def sync_blog_stats_to_db():
    ...
```


---

## 📁 项目结构概览

```
blog/
├── blog/              # Django 项目配置
├── myblog/            # 博客核心应用
│   ├── cache/         # 缓存客户端与监控
│   ├── models.py      # Blog 与 BlogView 模型
│   ├── views.py       # 博客展示逻辑
│   └── services/      # 缓存服务调用封装
├── users/             # 用户相关模块
├── mycelery/          # Celery 异步任务模块
└── manage.py
```


---

## ⚙️ 技术栈

| 技术 | 描述 |
|------|------|
| Python 3.x | 语言基础 |
| Django 5.2 | Web 框架 |
| MySQL | 主数据库 |
| Redis | 缓存与计数存储 |
| Celery | 异步任务调度 |
| django-redis | Django Redis 缓存集成 |
| Logging | 日志系统（命中率日志） |

---

## 🔐 安全与权限控制

- 只有登录用户才能查看博客详情
- 用户信息由 Django 认证系统统一管理
- 所有操作均具备异常捕获与日志记录机制

---

## 📈 性能优化亮点

- Redis 缓存减少数据库压力
- 阅读量统计使用原子操作，避免并发问题
- 缓存失效策略：TTL + 手动清理
- 缓存命中率监控可视化
- 异步任务定期落库，避免频繁写入

---

## 🛠️ 安装与部署

### 依赖安装

```bash
pip install -r requirements.txt
```


### 数据库迁移

```bash
python manage.py migrate
```


### 创建管理员账号（可选）

```bash
python manage.py createsuperuser
```


### 运行开发服务器

```bash
python manage.py runserver
```


### 启动 Celery Worker

```bash
celery -A blog worker --loglevel=info
```


### 启动定时任务（如缓存命中率日志输出）

```bash
python manage.py log_cache_stats
```


---

## 📦 数据模型

### `Blog`
- id
- title
- content
- author (User)
- created_at

### `BlogView`
- id
- blog (外键)
- user (外键, 可为空)
- viewed_at

---

## 📊 接口说明

| 路径 | 方法 | 描述 |
|------|------|------|
| `/myblogs/` | GET | 显示所有博客列表 |
| `/myblogs/<int:blog_id>/` | GET | 查看博客详情并更新阅读统计 |
| `/myblogs/stats/` | GET | 获取当前缓存命中率统计 |
| `/users/register/` | POST | 用户注册 |
| `/users/login/` | POST | 用户登录 |
| `/users/logout/` | GET | 用户登出 |

---

## 🧪 测试建议

- 单元测试放在各 app 的 `tests.py` 中
- 可编写缓存命中测试、阅读统计准确性验证、用户权限测试等

---

## 📝 示例截图

### 博客首页
![image-20250709080505314](C:\Users\hy303\AppData\Roaming\Typora\typora-user-images\image-20250709080505314.png)

### 博客详情页
![image-20250709080606851](C:\Users\hy303\AppData\Roaming\Typora\typora-user-images\image-20250709080606851.png)

---

## 📌 待优化点

- 增加单元测试覆盖率
- 增加前端页面交互优化（如点赞、评论）
- 增加分页、搜索、标签等功能
- 增加 API 接口（RESTful）
- 增加缓存降级策略（如 Redis 不可用时回退 DB 查询）

---

## ✅ 总结

本项目是一个典型的 **前后端分离式 Django 应用**，集成了缓存、异步任务、权限控制等现代 Web 开发常用技术。适合用于教学、练手或作为企业级博客系统的原型框架。
