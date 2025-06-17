from fastapi import HTTPException


def admin_permissions(is_admin: bool = False) -> bool:
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin permissions required")

    return True
