# app/models/user.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MT5Credentials(BaseModel):
    account: int
    password: str
    server: str
    
class MT5LoginResponse(BaseModel):
    success: bool
    session_id: Optional[str] = None
    balance: Optional[float] = None
    equity: Optional[float] = None
    currency: Optional[str] = None
    error: Optional[str] = None

class UserSession(BaseModel):
    session_id: str
    account: int
    server: str
    connected_at: datetime
    last_active: datetime
    is_active: bool = True
    balance: Optional[float] = None
    equity: Optional[float] = None
    currency: Optional[str] = None
