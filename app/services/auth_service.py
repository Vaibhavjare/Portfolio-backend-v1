# auth_service.py

from fastapi import HTTPException, status
from app.models.user_model import User, UserRole
from app.core.security import (
    verify_password,
    create_access_token,
    hash_password,
)


class AuthService:

    # =====================================
    # REGISTER
    # =====================================
    @staticmethod
    async def register(email: str, password: str):

        # 🔍 Check existing user
        existing_user = await User.find_one(User.email == email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # 🔐 Create new user
        user = User(
            email=email,
            password=hash_password(password),
            role=UserRole.USER,
            is_active=True,
        )

        await user.insert()

        return {
            "message": "User registered successfully",
        }

    # =====================================
    # LOGIN
    # =====================================
    @staticmethod
    async def login(email: str, password: str):

        user = await User.find_one(User.email == email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # 🔐 Verify password
        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # 🚫 Check active status
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        # 🔥 FIXED: Store role as string
        access_token = create_access_token(
            {
                "sub": str(user.email),
                "role": user.role.value,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "role": user.role.value,
            },
        }

    # =====================================
    # UPDATE USER ROLE (ADMIN ONLY)
    # =====================================
    @staticmethod
    async def update_user_role(email: str, new_role: str):

        user = await User.find_one(User.email == email)

        if not user:
            return None

        # 🔥 Safe Enum conversion
        try:
            user.role = UserRole(new_role)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role",
            )

        await user.save()

        return user