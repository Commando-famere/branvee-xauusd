# app/core/mt5_manager.py
import MetaTrader5 as mt5
from typing import Optional, Dict
import logging
from datetime import datetime
from app.config import MT5_TIMEOUT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MT5Manager:
    def __init__(self):
        self.active_sessions: Dict[str, dict] = {}
        self._initialized = False
        
    def initialize_mt5(self) -> bool:
        """Initialize MT5 terminal"""
        try:
            if not self._initialized:
                if not mt5.initialize():
                    logger.error("MT5 initialization failed")
                    return False
                self._initialized = True
                logger.info("✅ MT5 initialized successfully")
            return True
        except Exception as e:
            logger.error(f"MT5 init error: {e}")
            return False
    
    def connect(self, session_id: str, credentials: dict) -> dict:
        """Connect to MT5 account"""
        try:
            if not self.initialize_mt5():
                return {
                    "success": False,
                    "error": "Failed to initialize MT5"
                }
            
            # Convert account to int if it's string
            account = int(credentials['account']) if isinstance(credentials['account'], str) else credentials['account']
            
            authorized = mt5.login(
                login=account,
                password=credentials['password'],
                server=credentials['server'],
                timeout=MT5_TIMEOUT
            )
            
            if authorized:
                account_info = mt5.account_info()
                if not account_info:
                    return {
                        "success": False,
                        "error": "Failed to get account info"
                    }
                
                now = datetime.now()
                self.active_sessions[session_id] = {
                    "session_id": session_id,
                    "account": account,
                    "server": credentials['server'],
                    "connected_at": now,
                    "last_active": now,
                    "balance": account_info.balance,
                    "equity": account_info.equity,
                    "currency": account_info.currency
                }
                
                logger.info(f"✅ Account {account} connected successfully")
                
                return {
                    "success": True,
                    "session_id": session_id,
                    "balance": account_info.balance,
                    "equity": account_info.equity,
                    "currency": account_info.currency
                }
            else:
                error = mt5.last_error()
                logger.error(f"Login failed for {account}: {error}")
                return {
                    "success": False,
                    "error": f"Login failed: {error}"
                }
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def disconnect(self, session_id: str) -> dict:
        """Disconnect MT5 account"""
        if session_id in self.active_sessions:
            account = self.active_sessions[session_id]['account']
            del self.active_sessions[session_id]
            logger.info(f"✅ Account {account} disconnected")
            return {"success": True, "message": "Disconnected successfully"}
        return {"success": False, "error": "Session not found"}
    
    def get_account_info(self, session_id: str) -> Optional[dict]:
        """Get current account info"""
        if session_id in self.active_sessions:
            account_info = mt5.account_info()
            if account_info:
                return {
                    "balance": account_info.balance,
                    "equity": account_info.equity,
                    "profit": account_info.profit,
                    "margin": account_info.margin,
                    "margin_free": account_info.margin_free,
                    "currency": account_info.currency
                }
        return None
    
    def get_active_sessions(self) -> dict:
        """Get all active sessions"""
        sessions = {}
        for sid, session in self.active_sessions.items():
            sessions[sid] = {
                "account": session['account'],
                "server": session['server'],
                "connected_at": session['connected_at'].isoformat() if isinstance(session['connected_at'], datetime) else session['connected_at'],
                "last_active": session['last_active'].isoformat() if isinstance(session['last_active'], datetime) else session['last_active'],
                "balance": session['balance'],
                "equity": session['equity']
            }
        return sessions
    
    def update_activity(self, session_id: str):
        """Update session last active time"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_active'] = datetime.now()
