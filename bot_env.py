#!/usr/bin/env python3
"""
Telegram Bot - 消息转发到 ntfy（环境变量版本）
使用环境变量配置，更安全
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 从环境变量读取配置
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://ntfy.282994.xyz/telegram')
WEBHOOK_USER = os.getenv('WEBHOOK_USER', 'ntfyadmin')
WEBHOOK_PASSWORD = os.getenv('WEBHOOK_PASSWORD', '123')

if not BOT_TOKEN:
    raise ValueError("错误: BOT_TOKEN 环境变量未设置！")


def get_message_content(update: Update) -> str:
    """获取消息内容，支持多种消息类型"""
    message = update.effective_message

    # 文本消息
    if message.text:
        content = message.text
        if len(content) > 32:
            content = content[:32]
        return content

    # 图片消息
    if message.photo:
        return "你收到了一条图片信息"

    # 视频消息
    if message.video:
        return "你收到了一条视频信息"

    # 音频消息
    if message.audio:
        return "你收到了一条音频信息"

    # 语音消息
    if message.voice:
        return "你收到了一条语音信息"

    # 文档消息
    if message.document:
        return "你收到了一条文件信息"

    # 贴纸消息
    if message.sticker:
        return "你收到了一条贴纸信息"

    # 动画消息
    if message.animation:
        return "你收到了一条动画信息"

    # 位置信息
    if message.location:
        return "你收到了一条位置信息"

    # 联系人信息
    if message.contact:
        return "你收到了一条联系人信息"

    # 默认
    return "你收到了一条新信息"


def get_sender_name(update: Update) -> str:
    """获取发送人名称"""
    user = update.effective_user

    if user.username:
        return f"@{user.username}"

    if user.full_name:
        return user.full_name

    return "未知用户"


async def handle_message(update: Update, context) -> None:
    """处理收到的所有消息"""
    # 获取消息内容
    message_content = get_message_content(update)
    sender_name = get_sender_name(update)

    logger.info(f"收到来自 {sender_name} 的消息: {message_content}")

    # 发送到webhook
    try:
        # 使用用户名+密码认证，添加发送人header
        response = requests.post(
            WEBHOOK_URL,
            data=message_content.encode('utf-8'),
            auth=HTTPBasicAuth(WEBHOOK_USER, WEBHOOK_PASSWORD),
            headers={
                'Content-Type': 'text/plain; charset=utf-8',
                'Title': sender_name
            }
        )

        if response.status_code == 200:
            logger.info(f"消息已发送: {message_content}")
        else:
            logger.error(f"发送失败: HTTP {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"发送消息时出错: {e}")


def main() -> None:
    """启动机器人"""
    # 创建应用
    application = Application.builder().token(BOT_TOKEN).build()

    # 添加消息处理器 - 处理所有类型的消息
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    # 启动机器人
    logger.info("机器人已启动...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
