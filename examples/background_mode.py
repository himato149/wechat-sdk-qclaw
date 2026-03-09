"""
后台运行模式 — bot 在后台线程运行，主线程可以做其他事。

用法:
    python examples/background_mode.py
"""

import time

from qclaw import QChat, content

bot = QChat()


@bot.msg_register(content.TEXT)
def echo(msg):
    return f"[后台Bot] {msg.text}"


bot.auto_login()
bot.run(block=False)  # 不阻塞，在后台线程运行

print("机器人已在后台运行，主线程可以做其他事情。")
print("按 Ctrl+C 退出。")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    bot.stop()
    print("已停止。")
