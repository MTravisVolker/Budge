from typing import Optional, Union
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from .database import get_user_db
from .models import User
from .config import get_settings

settings = get_settings()

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User manager for handling user operations"""
    reset_password_token_secret = settings.JWT_SECRET_KEY
    verification_token_secret = settings.JWT_SECRET_KEY

    async def oauth_callback(
        self,
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: Optional[int] = None,
        refresh_token: Optional[str] = None,
        request: Optional[Request] = None,
        *,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
    ) -> models.UP:
        """Handle OAuth callback"""
        try:
            user = await self.get_by_oauth_account(oauth_name, account_id)
        except exceptions.UserNotExists:
            try:
                # Try to get user by email
                user = await self.get_by_email(account_email)
                if not associate_by_email:
                    raise exceptions.UserAlreadyExists()
                # Update user with OAuth info
                user.oauth_provider = oauth_name
                user.oauth_account_id = account_id
                await self.user_db.update(user)
            except exceptions.UserNotExists:
                # Create new user
                user = await self.create(
                    {
                        "email": account_email,
                        "oauth_provider": oauth_name,
                        "oauth_account_id": account_id,
                        "is_verified": is_verified_by_default,
                    }
                )

        return user

    async def get_by_oauth_account(
        self, oauth_name: str, account_id: str
    ) -> models.UP:
        """Get user by OAuth account"""
        user = await self.user_db.get_by_oauth_account(oauth_name, account_id)
        if user is None:
            raise exceptions.UserNotExists()
        return user

    async def create(
        self,
        user_create: Union[schemas.UC, dict],
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """Create a new user"""
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if isinstance(user_create, schemas.BaseUserCreate)
            else user_create
        )
        password = user_dict.pop("password", None)
        if password is not None:
            user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)
        return created_user

async def get_user_manager(user_db=Depends(get_user_db)):
    """Get user manager"""
    yield UserManager(user_db)
