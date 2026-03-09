"""
模块级单例风格 — 和 ItChat 用法完全一致。

用法:
    python examples/singleton_style.py
"""

import qclaw


@qclaw.msg_register(qclaw.content.TEXT)
def on_text(msg):
    return f"[Bot] {msg.text}"


qclaw.auto_login()
qclaw.run()
