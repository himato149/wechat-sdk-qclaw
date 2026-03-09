"""
对接 OpenAI 兼容 API — 让微信机器人接入大模型。

需要额外安装: pip install openai

用法:
    export OPENAI_API_KEY="sk-..."
    export OPENAI_BASE_URL="https://api.openai.com/v1"   # 可选
    python examples/llm_chat.py
"""

import asyncio
import os

from qclaw import QChat, content

bot = QChat()

# ---- OpenAI 配置 ----

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = "你是一个友好的微信助手，回答简洁明了。"

# 简单的会话记忆（按 user_id 存储）
conversations: dict[str, list[dict]] = {}
MAX_HISTORY = 20


@bot.msg_register(content.TEXT)
async def chat(msg, reply):
    if not API_KEY:
        return "请先设置 OPENAI_API_KEY 环境变量。"

    # 特殊命令
    if msg.text.strip() in ("清除记忆", "reset", "/reset"):
        conversations.pop(msg.user_id, None)
        return "对话记忆已清除。"

    # 构建消息历史
    history = conversations.setdefault(msg.user_id, [])
    history.append({"role": "user", "content": msg.text})

    # 截断过长历史
    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    # 调用 LLM（流式）
    try:
        import openai

        client = openai.AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)
        stream = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )

        full_reply = []
        async for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                full_reply.append(delta)
                await reply.send_chunk(delta)

        result = "".join(full_reply)
        history.append({"role": "assistant", "content": result})
        return result

    except ImportError:
        return "请安装 openai: pip install openai"
    except Exception as e:
        return f"调用 LLM 出错: {e}"


if __name__ == "__main__":
    if not API_KEY:
        print("警告: OPENAI_API_KEY 未设置，LLM 功能将不可用")
        print("设置方法: export OPENAI_API_KEY='sk-...'")
        print()

    bot.auto_login()
    bot.run()
