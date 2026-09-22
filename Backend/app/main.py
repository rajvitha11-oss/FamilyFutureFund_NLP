from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.nlp import understand_goal
from app.routes.goals import router as goals_router

# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="Family Future Fund NLP API"
)
app.include_router(goals_router)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# =========================================================
# REQUEST MODEL
# =========================================================

class GoalRequest(BaseModel):

    text: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Family Future Fund NLP Backend is running!"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "success",

        "project": "Family Future Fund"
    }


# =========================================================
# NLP GOAL UNDERSTANDING
# =========================================================

@app.post("/understand-goal")
def understand_user_goal(request: GoalRequest):

    result = understand_goal(
        request.text
    )

    return result