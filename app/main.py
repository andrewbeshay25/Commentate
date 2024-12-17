from enum import Enum

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Annotated, List
from app.categories import Categories
import db.models as models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session 
from sqlalchemy import func

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# DB STUFF
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommentCreate(BaseModel):
    message: str
    name: str
    category: Categories

class Comment(CommentCreate):
    id: int

class CommentResponse(BaseModel):
    id: int
    comment_message: str
    comment_name: str
    comment_category: Categories

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic V2

# GET endpoint for fetching comments with filters
@app.get("/comments/", response_model=List[CommentResponse])
def get_filtered_comments(
    name: Optional[str] = None,
    category: Optional[Categories] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Comments)

        # Apply filters dynamically
        if name:
            query = query.filter(func.lower(models.Comments.comment_name) == func.lower(name))
        if category:
            query = query.filter(models.Comments.comment_category == category)

        # Fetch results
        results = query.all()

        # Return a friendly response when no data is found
        if not results:
            return []

        return results

    except Exception as e:
        # Handle unexpected errors (e.g., DB connection issues)
        raise HTTPException(status_code=500, detail="An internal server error occurred.") from e


@app.post("/comments/")
async def create_comment(
    comment: CommentCreate, db: db_dependency
):
    # Create a new comment instance for the database
    db_comment = models.Comments(
        comment_message=comment.message,
        comment_name=comment.name,
        comment_category=comment.category,
    )
    db.add(db_comment)  # Add the new comment to the session
    db.commit()  # Commit the transaction
    db.refresh(db_comment)  # Refresh to get the auto-generated ID

    # Return the newly created comment
    return {
        "id": db_comment.id,
        "message": "Comment created successfully!",
        "comment": {
            "id": db_comment.id,
            "comment_message": db_comment.comment_message,
            "comment_name": db_comment.comment_name,
            "comment_category": db_comment.comment_category.value,
        },
    }

