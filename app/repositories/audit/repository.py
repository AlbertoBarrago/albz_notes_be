"""
Audit repositories
"""

from app.db.models.audit.model import Audit


def log_audit_event(session,
                    user_id: str = None,
                    action: str = None,
                    description: str = None):
    """
    Log Action
    :param session:
    :param user_id:
    :param action:
    :param description:
    """
    try:
        audit_log = Audit(user_id=user_id, action=action, description=description)
        session.add(audit_log)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
