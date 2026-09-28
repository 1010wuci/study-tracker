# 学习追踪器（Study Tracker）

一个用 Python + Flask 搭建的个人学习记录 Web 应用。

## 功能

- 📝 表单录入每日学习记录（日期、内容、时长、心情）
- 🗄️ 数据持久化到 SQLite 数据库
- 📊 自动生成每日学习时长柱状图
- 🗑️ 支持删除记录
- 📅 自动统计本周总学习时长

## 技术栈

| 技术 | 用途 |
|------|------|
| Flask | Web 框架 |
| SQLite | 数据存储 |
| pandas | 数据处理 |
| matplotlib | 数据可视化 |

## 运行方式

1. 安装依赖：
   ```bash
   pip install flask pandas matplotlib
