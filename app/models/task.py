from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from typing import TYPE_CHECKING 
if TYPE_CHECKING: from .goal import Goal
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = None
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        is_complete = task_data.get("is_complete")
        
        if is_complete is True:
            completed_at = datetime
        else:
            completed_at = None

        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=completed_at)
        
        return new_task

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["goal_id"] = self.goal_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = True if self.completed_at else False

        return task_as_dict