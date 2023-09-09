from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.main import app
from app.models.article import Article
from app.data_mock.article_mock import article_mock, article_edit_mock
from app.tests.endpoints import handle_data_article

client = TestClient(app)

def test_create_article(db: Session = next(get_db())):
    # Perform the creation
    response = client.post("/api/v1/articles", data=article_mock)
    assert response.status_code == 201

    # Verify that the title is not exist
    assert db.query(Article).filter(Article.title == article_mock.get('title')).first() is not None, f"{article_mock.get('title')} still exists in the database"

def test_create_article_exist():
    # Perform the creation
    response = client.post("/api/v1/articles", data=article_mock)
    assert response.status_code == 400

def test_read_all_article():
    # Perform the reading
    response = client.get("/api/v1/articles?article_status=all&article_lang=eng")
    data = response.json()
    handle_data_article(response, data, 'multiple')

    # Perform the reading
    response = client.get("/api/v1/articles?article_status=archived&article_lang=ind")
    data = response.json()
    handle_data_article(response, data, 'multiple')

def test_read_article(db: Session = next(get_db())):
    # Check if the article exists before attempting deletion
    article_exist = db.query(Article).filter(Article.title == article_mock.get('title')).first()
    assert article_exist is not None, f"Article {article_mock.get('slug')} does not exist in the database"

    # Perform the reading
    response = client.get(f"/api/v1/articles/{article_exist.slug}")
    data = response.json()
    handle_data_article(response, data, 'single')

def test_update_article(db: Session = next(get_db())):
    # Check if the article exists before attempting deletion
    article_exist = db.query(Article).filter(Article.title == article_mock.get('title')).first()
    assert article_exist is not None, f"Article {article_mock.get('id')} does not exist in the database"

    # Perform the reading
    response = client.patch(f"/api/v1/articles/{article_exist.id}", data=article_edit_mock)
    assert response.status_code == 200

def test_change_article_status(db: Session = next(get_db())):
    # Check if the article exists before attempting deletion
    article_exist = db.query(Article).filter(Article.title == article_edit_mock.get('title')).first()
    assert article_exist is not None, f"Article {article_edit_mock.get('id')} does not exist in the database"

    # Perform the reading
    response = client.put(f"/api/v1/articles/{article_exist.id}/status?article_status=flagged")
    assert response.status_code == 200

def test_delete_article(db: Session = next(get_db())):
    # Check if the article exists before attempting deletion
    article_exist = db.query(Article).filter(Article.title == article_edit_mock.get('title')).first()
    assert article_exist is not None, f"Article {article_edit_mock.get('id')} does not exist in the database"

    # Perform the deletion
    response = client.delete(f"/api/v1/articles/{article_exist.id}")
    assert response.status_code == 200

    # Perform the after deletion to check data already deleted
    response = client.delete(f"/api/v1/articles/{article_exist.id}")
    assert response.status_code == 404

    db.commit()
