import pytest
from httpx import AsyncClient
from app.main import app  # Import the FastAPI app
from db.database import Base, engine, SessionLocal
from db.models import Comments, Categories

# Test database setup
@pytest.fixture(scope="function")
def test_db():
    # Use the same engine as your app but reset the database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()

# Test client for the FastAPI app
@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Test cases
@pytest.mark.asyncio
async def test_get_comments_empty(client):
    response = await client.get("/comments/")
    assert response.status_code == 200
    assert response.json() == []  # Initially, no comments

@pytest.mark.asyncio
async def test_add_comment(client, test_db):
    # Add a comment
    data = {
        "comment_message": "This is a test comment",
        "comment_name": "Tester",
        "comment_category": "compliment"
    }
    response = await client.post("/comments/", json=data)
    assert response.status_code == 200
    comment = response.json()["comment"]
    assert comment["comment_message"] == "This is a test comment"
    assert comment["comment_name"] == "Tester"
    assert comment["comment_category"] == "compliment"

    # Verify it exists in the database
    db_query = test_db.query(Comments).filter(Comments.comment_message == "This is a test comment").first()
    assert db_query is not None

@pytest.mark.asyncio
async def test_get_comments_non_empty(client, test_db):
    # Add a comment
    comment = Comments(
        comment_message="Pre-existing comment",
        comment_name="ExistingTester",
        comment_category=Categories.COMPLIMENT
    )
    test_db.add(comment)
    test_db.commit()

    # Get comments
    response = await client.get("/comments/")
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 1
    assert comments[0]["comment_message"] == "Pre-existing comment"
    assert comments[0]["comment_name"] == "ExistingTester"
    assert comments[0]["comment_category"] == "compliment"
