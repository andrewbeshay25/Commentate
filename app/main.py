from enum import Enum

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Annotated

import db.models as models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session 

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

class Categories(Enum):
    ROAST = "roast"
    COMPLIMENT = "compliment"

class CommentCreate(BaseModel):
    message: str
    name: str
    category: Categories

class Comment(CommentCreate):
    id: int
    message: str
    name: str
    category: Categories

comments = {
    0: Comment(id=0, message="You are so handsome", name="Andrew", category=Categories.COMPLIMENT),
    2: Comment(id=2, message="You are so ulgy", name="Mark", category=Categories.ROAST),
    1: Comment(id=1, message="You are so weak", name="Derek", category=Categories.ROAST),
    3: Comment(id=3, message="You smell good", name="Kate", category=Categories.COMPLIMENT)
}



@app.get("/")
def index() -> dict[str, dict[int, Comment]]:
    return {"comments" : comments}

@app.get("/comments/{item_id}")
def query_comment_by_catetgory(item_id: int) -> Comment:
    if item_id not in comments:
        HTTPException(status_code=404, detail=f"Itenm with id: {item_id} does not exist.")
    return comments[item_id]

Selection = dict[
    str, str | int | Categories | None
]

@app.get("/comments/")
def query_comment_by_parameters(
    name: str | None = None,
    message: str | None = None,
    category: Categories | None = None
) -> dict[str, Selection | list[Comment]]:
    def check_comment(comment: Comment):
        return all((
            (name is None or comment.name == name),
            (message is None or comment.message == message),
            (category is None or comment.category == category)
        ))

    selection = [comment for comment in comments.values() if check_comment(comment)]

    return {"query": {"name": name, "message": message, "category": category},
            "selection" : selection}

@app.post("/")
def add_comment(comment_create: CommentCreate) -> dict:
    # Auto-generate an ID
    new_id = max(comments.keys(), default=0) + 1
    comment = Comment(id=new_id, **comment_create.dict())
    comments[new_id] = comment
    return {"Added": comment}


@app.post("/comments/")
async def create_comment(
    comment: models.Comments, db: db_dependency
):
    # Create and save a new comment
    db_comment = models.Comments(
        comment_message=comment.comment_message,
        comment_name=comment.comment_name,
        comment_category=comment.comment_category,
    )
    db.add(db_comment)  # Add the new comment
    db.commit()  # Commit the transaction
    db.refresh(db_comment)  # Refresh to fetch auto-generated ID

    # Return the created comment with its new ID
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
