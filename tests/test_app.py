import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app
from db.database import Base, engine, SessionLocal
from db.models import Comments, Categories
from sqlalchemy.orm import sessionmaker

# Test database setup
@pytest.fixture(scope="function")
def test_db():
    # Start a database session
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()

    try:
        # Truncate all data in the Comments table
        db.query(Comments).delete()
        db.commit()
        yield db
    finally:
        db.close()

# Test client for the FastAPI app
@pytest.fixture(scope="function")
def client():
    return TestClient(app)

# Test cases
def test_get_comments_empty(client, test_db):
    # Verify the database is clean before testing
    existing_comments = test_db.query(Comments).all()
    print("Existing comments before test:", existing_comments)

    # Perform the GET request
    response = client.get("/comments/")
    assert response.status_code == 200
    assert response.json() == []  # Initially, no comments


def test_add_comment(client, test_db):
    # Add a comment
    data = {
        "message": "This is a test comment",
        "name": "Tester",
        "category": "compliment"
    }
    response = client.post("/comments/", json=data)
    assert response.status_code == 200
    comment = response.json()["comment"]
    assert comment["comment_message"] == "This is a test comment"
    assert comment["comment_name"] == "Tester"
    assert comment["comment_category"] == "compliment"

    # Verify it exists in the database
    db_query = test_db.query(Comments).filter(Comments.comment_message == "This is a test comment").first()
    assert db_query is not None

def test_get_comments_non_empty(client, test_db):
    # Add a comment
    comment = Comments(
        comment_message="Pre-existing comment",
        comment_name="ExistingTester",
        comment_category=Categories.COMPLIMENT
    )
    test_db.add(comment)
    test_db.commit()

    # Get comments
    response = client.get("/comments/")
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 1
    assert comments[0]["comment_message"] == "Pre-existing comment"
    assert comments[0]["comment_name"] == "ExistingTester"
    assert comments[0]["comment_category"] == "compliment"
