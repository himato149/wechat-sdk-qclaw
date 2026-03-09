"""
工具调用演示 — 展示 tool_call 状态更新。

用法:
    python examples/tool_call_demo.py
"""

import asyncio

from qclaw import QChat, content

bot = QChat()


@bot.msg_register(content.TEXT)
async def handle(msg, reply):
    # 1. 启动一个工具调用（用户侧会看到"执行中"的状态）
    tool = await reply.tool_call("分析用户消息", kind="think")
    await asyncio.sleep(1)

    # 2. 推送进度
    await tool.update(f"正在分析：{msg.text[:20]}…")
    await asyncio.sleep(0.5)

    # 3. 完成
    await tool.complete(f"分析完成，共 {len(msg.text)} 个字符")

    # 4. 发送流式文本回复
    await reply.send_chunk("分析结果：")
    await asyncio.sleep(0.2)
    await reply.send_chunk(f"你发了一条 {len(msg.text)} 字的消息。")

    return f"分析完成：你的消息共 {len(msg.text)} 个字符。"


bot.auto_login()
bot.run()
