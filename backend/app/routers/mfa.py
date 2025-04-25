from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.user_manager import UserManager, get_user_manager
from app.schemas.mfa import MFAEnableResponse, MFAVerifyRequest, MFADisableRequest
from uuid import UUID
from typing import cast

router = APIRouter(prefix="/mfa", tags=["mfa"])

@router.post("/enable", response_model=MFAEnableResponse)
async def enable_mfa(
    user_manager: UserManager = Depends(get_user_manager)
):
    current_user = await user_manager.get_current_user()
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is already enabled"
        )

    secret, provisioning_uri = await user_manager.enable_mfa(cast(UUID, current_user.id))
    return MFAEnableResponse(
        secret=secret,
        provisioning_uri=provisioning_uri
    )

@router.post("/verify")
async def verify_mfa(
    request: MFAVerifyRequest,
    user_manager: UserManager = Depends(get_user_manager)
):
    current_user = await user_manager.get_current_user()
    if not current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )

    is_valid = await user_manager.verify_mfa(cast(UUID, current_user.id), request.code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA code"
        )

    return {"message": "MFA code verified successfully"}

@router.post("/disable")
async def disable_mfa(
    request: MFADisableRequest,
    user_manager: UserManager = Depends(get_user_manager)
):
    current_user = await user_manager.get_current_user()
    if not current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA is not enabled"
        )

    # Verify the code before disabling
    is_valid = await user_manager.verify_mfa(cast(UUID, current_user.id), request.code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA code"
        )

    await user_manager.disable_mfa(cast(UUID, current_user.id))
    return {"message": "MFA disabled successfully"}
