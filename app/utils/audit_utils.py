"""
Audit utils
"""
from app.db.models.audit_logs import AuditLog


def log_action(session, user_id: int = None, action: str = None, description: str = None):
    audit_log = AuditLog(user_id=user_id, action=action, description=description)
    session.add(audit_log)
    session.commit()