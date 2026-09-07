import httpx

from config import settings


class SupabaseAdminError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        self.status_code = status_code
        super().__init__(message)


async def create_user(email: str, password: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.supabase_url}/auth/v1/admin/users",
            headers={
                "apikey": settings.supabase_secret_key,
                "Authorization": f"Bearer {settings.supabase_secret_key}",
            },
            json={"email": email, "password": password, "email_confirm": True},
        )

    if response.status_code == 201:
        data = response.json()
        return {"id": data["id"], "email": data["email"]}

    detail = response.json().get("msg", "Could not create the account.")
    if response.status_code in (400, 422) and "already" in detail.lower():
        raise SupabaseAdminError("An account with that email already exists.", status_code=409)
    if response.status_code in (400, 422):
        raise SupabaseAdminError(detail, status_code=400)
    raise SupabaseAdminError("Could not create the account. Try again later.", status_code=502)
