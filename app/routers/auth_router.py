from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from fastapi.security import OAuth2PasswordRequestForm

from app.core.rbac import admin_required
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =====================================
# REQUEST SCHEMAS
# =====================================

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class RoleUpdateRequest(BaseModel):
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =====================================
# REGISTER
# =====================================

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    return await AuthService.register(
        email=data.email,
        password=data.password,
    )


# =====================================
# LOGIN (Swagger Compatible)
# =====================================

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible login for Swagger.
    Username field = email
    """
    return await AuthService.login(
        email=form_data.username,  # Swagger sends username
        password=form_data.password,
    )


# =====================================
# UPDATE ROLE (ADMIN ONLY)
# =====================================

@router.put("/update-role", dependencies=[Depends(admin_required)])
async def update_role(data: RoleUpdateRequest):
    user = await AuthService.update_user_role(
        email=data.email,
        new_role=data.role,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {"message": "Role updated successfully"}