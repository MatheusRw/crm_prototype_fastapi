from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    
    try:
        # Token simples: "user-token-1"
        if token.startswith("user-token-"):
            user_id = token.replace("user-token-", "")
            user = db.query(models.User).filter(models.User.id == int(user_id)).first()
            if user:
                return user
        
        raise HTTPException(status_code=401, detail="Token inválido")
    except:
        raise HTTPException(status_code=401, detail="Token inválido")