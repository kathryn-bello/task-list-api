from flask import Blueprint, request, make_response, Response, abort
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model
from app.db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    new_goal = create_model(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dict(), 201

@goals_bp.post("/<id>/tasks")
def assign_tasks_to_goal(id):
    resp_dict = {}
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    
    if "task_ids" not in request_body:
        return {"details": "task_ids is required"}, 400
        
    task_ids = request_body["task_ids"]
    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks.append(task)
    
    goal.tasks = tasks
    db.session.commit()

    resp_dict["id"] = goal.id
    resp_dict["task_ids"] = [task.id for task in goal.tasks]

    return resp_dict, 200


@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goal_response = [goal.to_dict() for goal in goals]
    return goal_response, 200


@goals_bp.get("/<id>")
def get_goal_by_id(id):
    goal = validate_model(Goal, id)

    return goal.to_dict(), 200

@goals_bp.get("/<id>/tasks")
def get_goal_tasks(id):
    goal = validate_model(Goal, id)

    return goal.to_dict(), 200


@goals_bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@goals_bp.delete("/<id>")
def delete_goal_by_id(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")