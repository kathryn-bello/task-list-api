from flask import make_response, Response, abort
from app.db import db
import requests
import os

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except Exception:
        response = {"details": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"details": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except Exception as e:
        response = {"details": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def send_slack_notification(task_title):
    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACK_API_TOKEN")

    payload = {
        "channel": "C09QW7ZQ8CX", 
        "text": f"Someone just completed the task {task_title}"
    }

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(response.json())
        return response.json()
    except Exception as e:
        return {"details": f"Failed to send slack message {e}"}