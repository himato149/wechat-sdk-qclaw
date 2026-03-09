"""
最简单的回声机器人 — 收到什么回什么。

用法:
    python examples/echo_bot.py
"""

from qclaw import QChat, content

bot = QChat()


@bot.msg_register(content.TEXT)
def echo(msg):
    return f"你说的是：{msg.text}"


bot.auto_login()
bot.run()
