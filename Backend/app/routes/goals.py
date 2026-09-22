from fastapi import APIRouter
from pydantic import BaseModel

from app.models import db, cursor


router = APIRouter()


class GoalData(BaseModel):
    goal_name: str
    category: str
    target_amount: float
    duration_months: int
    monthly_saving: float
    saved_amount: float = 0
    status: str = "In Progress"


class SavedAmountData(BaseModel):
    saved_amount: float


@router.post("/save-goal")
def save_goal(goal: GoalData):

    query = """
        INSERT INTO goals
        (
            goal_name,
            category,
            target_amount,
            duration_months,
            monthly_saving,
            saved_amount,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        goal.goal_name,
        goal.category,
        goal.target_amount,
        goal.duration_months,
        goal.monthly_saving,
        goal.saved_amount,
        goal.status
    )

    cursor.execute(query, values)
    db.commit()

    return {
        "success": True,
        "message": "Goal saved successfully!",
        "goal_id": cursor.lastrowid
    }


@router.get("/goal/{goal_id}")
def get_goal(goal_id: int):

    query = """
        SELECT
            id,
            goal_name,
            category,
            target_amount,
            duration_months,
            monthly_saving,
            saved_amount,
            status
        FROM goals
        WHERE id = %s
    """

    cursor.execute(query, (goal_id,))

    result = cursor.fetchone()

    if result is None:
        return {
            "success": False,
            "message": "Goal not found."
        }

    return {
        "success": True,
        "goal": {
            "id": result[0],
            "goal_name": result[1],
            "category": result[2],
            "target_amount": float(result[3]),
            "duration_months": result[4],
            "monthly_saving": float(result[5]),
            "saved_amount": float(result[6]),
            "status": result[7]
        }
    }


@router.put("/goal/{goal_id}/saved-amount")
def update_saved_amount(goal_id: int, data: SavedAmountData):

    query = """
        UPDATE goals
        SET saved_amount = %s
        WHERE id = %s
    """

    cursor.execute(
        query,
        (data.saved_amount, goal_id)
    )

    db.commit()

    if cursor.rowcount == 0:
        return {
            "success": False,
            "message": "Goal not found."
        }

    return {
        "success": True,
        "message": "Saved amount updated successfully!"
    }