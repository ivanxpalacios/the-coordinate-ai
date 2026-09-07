import secrets

from fastapi import APIRouter, HTTPException

from config import settings
from models.auth import RegisterRequest, RegisterResponse
from services.supabase_admin import SupabaseAdminError, create_user

router = APIRouter()


@router.post("/auth/register", status_code=201)
async def register(request: RegisterRequest) -> RegisterResponse:
    if not secrets.compare_digest(request.access_code, settings.registration_access_code):
        raise HTTPException(status_code=403, detail="Invalid access code.")

    try:
        user = await create_user(request.email, request.password)
    except SupabaseAdminError as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) from e

    return RegisterResponse(**user)
