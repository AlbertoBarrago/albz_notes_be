from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.db.models.users import User

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestUser:

    def setup_class(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        Base.metadata.create_all(engine)
        self.session = SessionLocal()
        self.new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=user_data["password"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_register_user(self):
        self.session.add(self.new_user)
        self.session.commit()

        created_user = self.session.query(User).filter(User.username == "testuser").first()
        assert created_user is not None
        assert created_user.username == "testuser"
        assert created_user.email == "test@example.com"

