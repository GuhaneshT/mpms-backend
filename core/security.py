import httpx
import time
from jose import jwt, jwk, JWTError
from fastapi import HTTPException, status
from core.config import settings

# Simple JWKS Cache
_jwks_cache: dict = {"keys": [], "last_updated": 0.0}

def get_jwks() -> list:
    global _jwks_cache
    now = time.time()
    # Cache for 1 hour
    if not _jwks_cache["keys"] or (now - _jwks_cache["last_updated"] > 3600):
        try:
            # Construct JWKS URL from Supabase URL
            jwks_url = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"
            response = httpx.get(jwks_url)
            response.raise_for_status()
            _jwks_cache["keys"] = response.json().get("keys", [])
            _jwks_cache["last_updated"] = now
        except Exception as e:
            print(f"Error fetching JWKS from Supabase: {e}")
    return _jwks_cache["keys"]

def verify_token(token: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
        algorithm = header.get("alg")
        
        if algorithm == "HS256":
            return jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
        elif algorithm == "ES256":
            kid = header.get("kid")
            jwks = get_jwks()
            key_dict = next((k for k in jwks if k["kid"] == kid), None)
            
            if not key_dict:
                raise JWTError(f"Matching key for kid {kid} not found in JWKS")
                
            # Construct the key object from JWK dict
            key = jwk.construct(key_dict)
            
            return jwt.decode(
                token,
                key,
                algorithms=["ES256"],
                options={"verify_aud": False}
            )
        else:
            raise JWTError(f"Unsupported algorithm: {algorithm}")
            
    except JWTError as e:
        print(f"JWT Verification Error: {type(e).__name__} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Unexpected Auth Error: {type(e).__name__} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal authentication error"
        )
