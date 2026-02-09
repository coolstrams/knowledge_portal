# app/core/permissions.py
USER_KB_PERMISSION = {
    "user_1": ["kb_a"],
    "admin": ["*"]
}


def allowed_kbs(user_id: str):
    return USER_KB_PERMISSION.get(user_id, [])
