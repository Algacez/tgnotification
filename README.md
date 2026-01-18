# Telegram 消息通知机器人

Telegram机器人会将收到的消息转发到 ntfy webhook。

## 功能特点

- 监听机器人加入的所有群组和私聊消息
- 支持多种消息类型：文本、图片、视频、音频、语音、文件、贴纸、动画、位置、联系人等
- 文本消息超过32个字符时自动截取前32个字符
- 非文本消息显示"你收到了一条XX信息"
- 自动获取发送人信息并添加到请求头
- 使用HTTP密码认证

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取 Bot Token

1. 在Telegram中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按提示设置机器人名称
4. 复制获得的 Bot Token

### 3. 配置机器人

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的配置：
```bash
BOT_TOKEN=你的实际Token
WEBHOOK_URL=https://ntfy.282994.xyz/telegram
WEBHOOK_USER=ntfyadmin
WEBHOOK_PASSWORD=你的密码
```

3. 运行机器人：
```bash
python bot_env.py
```

### 4. 将机器人加入群组

1. 在Telegram中打开你的群组
2. 点击群组名称进入群组信息
3. 点击"添加成员"或"邀请"
4. 搜索你的机器人用户名
5. 将机器人添加到群组
6. **重要**: 给予机器人管理员权限，确保能读取消息

## 支持的消息类型

- **文本消息**: 显示前32个字符
- **图片**: "你收到了一条图片信息"
- **视频**: "你收到了一条视频信息"
- **音频**: "你收到了一条音频��息"
- **语音**: "你收到了一条语音信息"
- **文件**: "你收到了一条文件信息"
- **贴纸**: "你收到了一条贴纸信息"
- **动画**: "你收到了一条动画信息"
- **位置**: "你收到了一条位置信息"
- **联系人**: "你收到了一条联系人信息"

## 请求格式

```bash
curl -u '用户名:密码' -H "Title: @username" -d "消息内容" https://ntfy.282994.xyz/telegram
```

## 后台运行

### 使用 nohup

```bash
nohup python bot_env.py > bot.log 2>&1 &
```

### 使用 screen

```bash
screen -S telegram-bot
python bot_env.py
# 按 Ctrl+A, 然后按 D 来分离会话
```

### 使用 systemd（推荐生产环境）

创建 `/etc/systemd/system/telegram-bot.service`：

```ini
[Unit]
Description=Telegram Notification Bot
After=network.target

[Service]
Type=simple
User=你的用户名
WorkingDirectory=/Users/rock/Projects/tgnotification
ExecStart=/usr/bin/python3 /Users/rock/Projects/tgnotification/bot_env.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

## 检查日志

```bash
tail -f bot.log
```

## 注意事项

- 确保机器人有权限读取群组消息
- Bot Token 和密码不要泄露或提交到公开仓库
- `.env` 文件已在 `.gitignore` 中，不会被提交
