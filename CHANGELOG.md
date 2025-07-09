# 🧑‍💻 Django 博客系统开发日志（CHANGELOG）

---

### 初始化项目结构
- 创建 Django 项目 [blog](file://E:\django\blog\myblog\models.py#L13-L13)
- 新建应用 `myblog`, `users`, `mycelery`
- 配置数据库为 MySQL，设置默认用户模型和缓存配置（预留）
- 初始化数据模型：
  - [Blog](file://E:\django\blog\myblog\models.py#L3-L10): 标题、内容、作者、发布时间
  - [BlogView](file://E:\django\blog\myblog\models.py#L12-L15): 用户阅读记录

### 实现博客列表页
- 编写 [views.py](file://E:\django\blog\myblog\views.py) 展示所有博客文章
- 使用 Django 模板引擎渲染 HTML 页面
- 设计简单 UI 框架并实现点击跳转逻辑

### 用户登录注册流程初步实现
- 使用 Django 内置认证系统搭建登录、注册页面
- 支持自动跳转至原页面（通过 `?next=` 参数）
- 注册成功后自动跳转至登录页（增加用户体验）
- 添加前端 JavaScript 提醒机制，防止未登录访问详情页

###  博客详情页 + 阅读统计雏形
- 完成博客详情页面模板设计
- 在视图中增加对已登录用户的判断
- 实现最简单的阅读次数累加逻辑（仅在内存中模拟）
- 增加测试数据，支持快速调试

---

### 登录跳转逻辑优化
- 修改 [login_view](file://E:\django\blog\users\views.py#L18-L33) 和 [register_view](file://E:\django\blog\users\views.py#L4-L17) 支持 `next` 参数
- 表单提交时保留跳转地址
- 成功登录/注册后优先跳转原页面，否则跳转首页

### 前端样式调整与交互优化
- 调整登录页、注册页样式，提升可读性
- 添加注册成功页面倒计时跳转效果
- 对未登录用户点击博客标题添加提示弹窗
- 所有静态资源整理归类，便于后续部署

---

### Redis 缓存客户端封装
- 创建 `cache/clients.py` 封装博客详情缓存逻辑
- 使用 Redis 存储 blog 数据，减少数据库压力
- 设置 TTL（过期时间），提高缓存利用率
- 增加装饰器监控缓存命中率

### 阅读统计服务开发
- 创建 `cache/stats.py` 模块，使用 Redis 的 `incr`、`sadd` 实现阅读计数
- 统计维度：
  - 总阅读量
  - 当前用户阅读次数
  - 独立访客数（UV）
- 视图层集成阅读统计功能，每次访问自动更新数据

### 异步落库任务编写
- 引入 Celery，配置 Redis 作为 Broker
- 编写异步任务 [sync_blog_stats_to_db](file://E:\django\blog\mycelery\blog_stats\tasks.py#L0-L26)，定期将 Redis 中的数据写入 MySQL
- 使用 `BlogView.objects.create()` 同步记录
- 删除旧缓存 key，确保数据一致性
- 配置定时命令 [log_cache_stats](file://E:\django\blog\myblog\management\commands\log_cache_stats.py#L0-L0)，输出命中率日志

### 缓存命中率监控模块
- 实现缓存命中率统计逻辑
- 提供接口 `/myblogs/stats/` 返回当前缓存状态
- 日志文件记录命中率变化趋势
- 提升性能可观测性，便于后期调优

