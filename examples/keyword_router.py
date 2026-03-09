"""
关键词路由机器人 — 根据消息内容分发到不同处理逻辑。

用法:
    python examples/keyword_router.py
"""

from qclaw import QChat, content

bot = QChat()

# 定义关键词和对应回复
ROUTES = {
    "帮助": "可用命令：帮助 / 时间 / 关于 / echo <内容>",
    "关于": "QChat 微信机器人 SDK v0.1.0\nhttps://github.com/example/wechat-sdk-qclaw",
}


@bot.msg_register(content.TEXT)
def router(msg):
    text = msg.text.strip()

    # 精确匹配
    if text in ROUTES:
        return ROUTES[text]

    # 前缀匹配
    if text == "时间":
        from datetime import datetime
        return f"现在是 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    if text.startswith("echo "):
        return text[5:]

    # 默认回复
    return f"你好！你说了：{text}\n\n发送「帮助」查看可用命令。"


bot.auto_login()
bot.run()
