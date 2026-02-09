import uuid
from datetime import datetime

def gen_datetime_uuid16() -> str:
    """
    yyyymmddHHMMSS + uuid(16 hex chars)

    Example:
    20260209173645a3f9c2d4e8b17f6a
    """
    time_part = datetime.now().strftime("%Y%m%d%H%M%S")
    uuid_part = uuid.uuid4().hex[:16]  # 16 位随机
    return f"{time_part}{uuid_part}"
