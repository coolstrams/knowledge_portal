# app/core/auth.py
from fastapi import Header


def get_current_user(authorization: str = Header(None)):
    # 示例：真实环境用 JWT
    return {
        "user_id": "user_1",
        "role": "user"
    }
