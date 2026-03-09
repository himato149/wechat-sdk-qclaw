"""
流式回复演示 — 逐段发送文本，模拟打字效果。

用法:
    python examples/streaming_reply.py
"""

import asyncio

from qclaw import QChat, content

bot = QChat()


@bot.msg_register(content.TEXT)
async def stream(msg, reply):
    chunks = [
        f"收到你的消息：「{msg.text}」\n\n",
        "让我想想……\n\n",
        "好的，这是我的回答：\n",
        "微信机器人开发其实很简单，",
        "用 qclaw 几行代码就搞定了！",
    ]

    for chunk in chunks:
        await reply.send_chunk(chunk)
        await asyncio.sleep(0.3)  # 模拟思考延迟

    return "".join(chunks)


bot.auto_login()
bot.run()
