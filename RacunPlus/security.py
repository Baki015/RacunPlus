from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer = HTTPBearer(auto_error=True)
async def get_current_user_id(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> int:
    token = creds.credentials.strip()
    if not token.isdigit():
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(token)
