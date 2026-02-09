# 小白个人记账本（Web 版）

> 从命令行走向 Web —— 一个 后端开发 学习者的进阶实践

这是一个基于 **Flask** 实现的 Web 版个人记账应用。它是我继「命令行个人记账本」之后的升级作品，在掌握 Python、Git 和 MySQL 基础后，为深入学习 Web 开发（并为后续 Django 打基础）而动手打造的全栈小项目。

用户可注册账号，登录后管理**专属的收支记录**，支持增、删、改、查及按日期筛选，界面简洁美观，功能完整可用。

---

## 🌟 核心功能
- ✅ **用户系统**：注册（用户名 + 手机号 + 密码）、登录（Session 认证）
- ✅ **记账管理**：
  - 添加收入/支出记录（含金额、分类、日期、备注）
  - 编辑或删除已有记录
  - 按日期查询特定记录
- ✅ **数据隔离**：每位用户只能查看和操作自己的记账数据
- ✅ **友好交互**：Bootstrap 模态框 + Flash 消息提示操作结果

---

## 🛠 技术栈
| 类别       | 技术/工具                     |
|------------|------------------------------|
| 后端框架   | Flask (Python)               |
| 数据库     | MySQL                        |
| 数据库驱动 | PyMySQL                      |
| 前端框架   | Bootstrap 5.3.8（本地引入）  |
| 图标库     | Font Awesome 6.4.0（本地）   |
| 模板引擎   | Jinja2                       |
| 版本控制   | Git                          |

> 💡 本项目**未使用 ORM**，直接通过原生 SQL 操作数据库，便于理解底层交互逻辑。

---

## 🗂 项目结构 
web_account/
├── app.py # 主应用：路由与业务逻辑
├── config.py # 数据库连接 & Flask 密钥（不提交）
├── models.py # 数据库操作函数（CRUD）
├── static/ # 静态资源
│ ├── img/ # 背景图：background.png, acct_backg.png
│ └── plugins/ # Bootstrap + Font Awesome（本地）
└── templates/ # HTML 模板
├── login.html # 登录页
├── register.html # 注册页
└── account.html # 记账主页（含模态框交互）


---

## 🚀 快速启动指南（复制以下全部内容到终端执行）
```bash
# 1. 创建并激活虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/macOS；Windows 用：.venv\Scripts\activate

# 2. 安装依赖
pip install flask pymysql

# 3. 初始化数据库（请先登录 MySQL 客户端执行以下 SQL）
# CREATE DATABASE web_account CHARACTER SET utf8;
# USE web_account;
# CREATE TABLE admin (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL, mobile VARCHAR(20) NOT NULL) COMMENT "用户登录表";
# CREATE TABLE account (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, amount DECIMAL(10,2) NOT NULL COMMENT "金额", type ENUM("income","expense") NOT NULL COMMENT "类型", category VARCHAR(100) NOT NULL COMMENT "种类", date DATE NOT NULL COMMENT "日期", description TEXT COMMENT "备注") COMMENT "用户记账表";

# 4. 创建配置文件（在项目根目录执行，Windows 用户请手动创建 config.py）
cat > config.py << 'EOF'
Wa_config = {
    "host": "localhost",
    "user": "root",
    "password": "你的MySQL密码",  # ← 务必修改为你的实际密码！
    "database": "web_account",
    "charset": "utf8"
}
Secret_key = "your_strong_secret_key_2026"  # ← 建议用随机字符串
EOF

# 5. 启动应用
python app.py

✅ 启动成功后，浏览器访问：
👉 http://127.0.0.1:5000/user/login