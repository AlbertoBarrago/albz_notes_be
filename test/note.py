from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from sqlalchemy import create_engine
from app.db.models.users import User
from app.db.models.notes import Note

# Using an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Test class for Note CRUD operations
class TestNote:
    def setup_class(self):
        Base.metadata.create_all(engine)

        self.session = SessionLocal()

        # Create a test user
        self.test_user = User(
            username="test_user",
            email="test_user@example.com",
            hashed_password="hashed_password",  # Assuming you set a valid password
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.session.add(self.test_user)
        self.session.commit()

        # Create a valid note and associate with the test user
        self.valid_note = Note(
            title="Test Note",
            content="This is a test note.",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            user_id=self.test_user.user_id  # Associate note with the test user
        )

        self.session.add(self.valid_note)
        self.session.commit()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_note_creation(self):
        note = self.session.query(Note).filter_by(title="Test Note").first()

        assert note is not None
        assert note.title == "Test Note"
        assert note.content == "This is a test note."

    def test_note_update(self):
        note = self.session.query(Note).filter_by(title="Test Note").first()

        note.content = "Updated content"
        self.session.commit()

        updated_note = self.session.query(Note).filter_by(title="Test Note").first()
        assert updated_note.content == "Updated content"

    def test_note_deletion(self):
        # Retrieve and delete the note
        note = self.session.query(Note).filter_by(title="Test Note").first()
        self.session.delete(note)
        self.session.commit()

        # Assert that the note is deleted from the database
        deleted_note = self.session.query(Note).filter_by(title="Test Note").first()
        assert deleted_note is None
