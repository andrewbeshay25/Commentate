from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

class Comment(BaseModel):
    id: int
    message: str
    name: str
    category: Categories

comments = {
    0: Comment(id=0, message="You are so handsome", name="Andrew", category=Categories.COMPLIMENT),
    2: Comment(id=2, message="You are so ulgy", name="Mark", category=Categories.ROAST),
    1: Comment(id=1, message="You are so weak", name="Derek", category=Categories.ROAST),
    2: Comment(id=2, message="You smell good", name="Andrew", category=Categories.COMPLIMENT)
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
def add_comment(comment: Comment) -> dict[str, Comment]:
    if (comment.id in comments):
        raise HTTPException(status_code=400, detail=f"Comment with id: {comment.id} already exists.")
    comments[comment.id] = comment
    return {"Added": comment}