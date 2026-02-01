from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
import bcrypt

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # return pwd_context.hash(password)
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed : str) -> bool:
    # return pwd_context.verify(password, hashed)
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))



def create_access_token(data: dict):
    to_encode = data.copy()
    access_tocken_expiry_minutes: int = 60
    expire = datetime.utcnow() + timedelta(minutes=access_tocken_expiry_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorith)