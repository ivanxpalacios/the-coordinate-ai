import jwt
from fastapi import Header, HTTPException

from config import settings

_jwks_client = jwt.PyJWKClient(settings.supabase_jwks_url)


async def require_user(authorization: str = Header(default="")) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token.")
    token = authorization.removeprefix("Bearer ")

    try:
        unverified_header = jwt.get_unverified_header(token)
        signing_key = _jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=[unverified_header["alg"]],
            audience="authenticated",
        )
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired session.") from e

    return claims["sub"]
