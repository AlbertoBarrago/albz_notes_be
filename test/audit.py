from datetime import datetime
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.db.models.user.model import User
from app.db.models.audit.model import Audit

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestAuditLog:

    def setup_class(self):
        """
        Set up the test by creating a user and an audit log entry.
        """
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }

        Base.metadata.create_all(engine)

        self.session = SessionLocal()

        # Create and hash the user password
        hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        self.new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_password,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Add the user to the session and commit
        self.session.add(self.new_user)
        self.session.commit()

        # Create an audit log entry for the user
        self.audit_log = Audit(
            user_id=self.new_user.user_id,
            action="LOGIN",
            description="User logged in successfully",
            timestamp=datetime.now()
        )

        # Add the audit log entry to the session and commit
        self.session.add(self.audit_log)
        self.session.commit()

    def teardown_class(self):
        """
        Clean up after the test by rolling back the session and closing it.
        """
        self.session.rollback()
        self.session.close()

    def test_audit_log_creation(self):
        """
        Test that an audit log entry is correctly created for a user.
        Verifies that the audit log entry is saved and associated with the correct user.
        """
        audit_entry = self.session.query(Audit).filter(Audit.user_id == self.new_user.user_id).first()

        assert audit_entry is not None
        assert audit_entry.user_id == self.new_user.user_id
        assert audit_entry.action == "LOGIN"
        assert audit_entry.description == "User logged in successfully"
        assert audit_entry.timestamp is not None

    def test_audit_log_user_association(self):
        """
        Test that the audit log entry is correctly associated with the user.
        """
        audit_entry = self.session.query(Audit).filter(Audit.user_id == self.new_user.user_id).first()

        assert audit_entry.user is not None
        assert audit_entry.user.username == "testuser"
        assert audit_entry.user.email == "test@example.com"
