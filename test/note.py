from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.models.note import Base, Note
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestNote:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()
        self.valid_note = Note(
            title="Test Note",
            content="This is a test note.",
            created_at=datetime.now(),
            updated_at=datetime.now()
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
        note = self.session.query(Note).filter_by(title="Test Note").first()
        self.session.delete(note)
        self.session.commit()

        deleted_note = self.session.query(Note).filter_by(title="Test Note").first()
        assert deleted_note is None
