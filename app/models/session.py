# app/models/session.py
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class SessionInfo(BaseModel):
    session_id: str
    account: int
    server: str
    connected_at: datetime
    status: str
    
class SessionList(BaseModel):
    active_sessions: Dict[str, SessionInfo]
    count: int
