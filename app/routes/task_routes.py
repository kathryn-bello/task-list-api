from flask import Blueprint, request, make_response, Response, abort
from app.models.task import Task
from app.db import db
from sqlalchemy import desc, asc
from datetime import datetime
from app.routes.route_utilities import validate_model, create_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    new_task = create_model(request_body)

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201


@tasks_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")
    query = db.select(Task)

    if sort_param == "asc":
        query = query.order_by(asc(Task.title))
    elif sort_param == "desc":
        query = query.order_by(desc(Task.title))
    else:
        query = query.order_by(Task.id)
    
    tasks = db.session.scalars(query)
    task_response = [task.to_dict() for task in tasks]

    return task_response, 200


@tasks_bp.get("/<id>")
def get_task_by_id(id):
    task = validate_model(Task, id)

    return task.to_dict(), 200


@tasks_bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@tasks_bp.patch("/<id>/mark_complete")
def mark_task_complete(id):
    task = validate_model(Task, id)
    
    now = datetime.now()
    task.completed_at = now
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


@tasks_bp.patch("/<id>/mark_incomplete")
def mark_task_incomplete(id):
    task = validate_model(Task, id)

    task.completed_at = None
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


@tasks_bp.delete("/<id>")
def delete_task_by_id(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")