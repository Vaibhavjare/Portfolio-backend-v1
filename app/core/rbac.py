# rbac.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from app.core.security import decode_access_token


# =========================================
# OAuth2 Scheme (MATCHES YOUR ROUTER)
# =========================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =========================================
# Get Current Authenticated User
# =========================================

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Decode token and return user payload
    """

    try:
        payload = decode_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        email = payload.get("sub")
        role = payload.get("role")

        if not email or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        return {
            "email": email,
            "role": role,
        }

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# =========================================
# Admin Role Check
# =========================================

def admin_required(user: dict = Depends(get_current_user)):
    """
    Allow access only if role is ADMIN
    """
    if user["role"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user