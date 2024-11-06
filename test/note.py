from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.main import app
from app.models.note import Base, Note

# Configurazione del database SQLite in-memory per i test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea tutte le tabelle nel database di test
Base.metadata.create_all(bind=engine)


# Fixture per gestire la sessione del DB per i test
@pytest.fixture(scope="module")
def setup_class():
    # Crea una sessione di test per ogni modulo
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client():
    return TestClient(app)


# Test per creare una nota
def test_create_note(client, setup_class):
    session = setup_class  # Ottieni la sessione dal fixture

    note_data = {
        "title": "Test Note",
        "content": "This is a test note.",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    # Fai la richiesta POST per creare una nuova nota
    response = client.post("/api/v1/notes", json=note_data)

    # Verifica che la risposta abbia lo status code 201 (Created)
    assert response.status_code == 201

    # Verifica che la risposta contenga i dati corretti
    created_note = response.json()
    assert created_note["title"] == note_data["title"]
    assert created_note["content"] == note_data["content"]
    assert created_note["created_at"] == note_data["created_at"]
    assert created_note["updated_at"] == note_data["updated_at"]
    assert "id" in created_note  # La nota deve avere un id

    # Verifica che la nota sia stata effettivamente salvata nel DB
    saved_note = session.query(Note).filter_by(id=created_note["id"]).first()
    assert saved_note is not None
    assert saved_note.title == note_data["title"]
    assert saved_note.content == note_data["content"]
    assert saved_note.created_at == note_data["created_at"]
    assert saved_note.updated_at == note_data["updated_at"]

    # Esegui il commit della sessione per salvare effettivamente nel DB
    session.commit()
