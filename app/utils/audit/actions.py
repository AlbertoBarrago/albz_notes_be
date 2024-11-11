"""
Audit utils
"""

from app.db.models.audit import Audit


def log_action(session,
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
    audit_log = Audit(user_id=user_id, action=action, description=description)
    session.add(audit_log)
    session.commit()
