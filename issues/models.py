from datetime import datetime
from typing import Optional

from abc import ABC, abstractmethod

class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value.isoformat() if isinstance(value, datetime) else value
            for key, value in self.__dict__.items()
        }
    
class Reporter(BaseEntity):
    def __init__(self,id,name,email,team):
        self.id=id
        self.name=name
        self.email=email
        self.team=team

    def validate(self):
        if not self.name:
            raise ValueError('Name cannot be empty')
        if '@' not in self.email:
            raise ValueError('Invalid email')


class Issue(BaseEntity):
    def __init__(self,id,title,description,status,priority,reporter_id,created_at: Optional[datetime] = None):
        self.id=id
        self.title=title
        self.description=description
        self.status=status
        self.priority=priority
        self.reporter_id=reporter_id
        self.created_at=created_at if created_at else datetime.now()

    def validate(self):
        if not self.title:
            raise ValueError('Title cannot be empty')
        if self.status not in ['open', 'in_progress', 'closed', 'resolved']:
            raise ValueError('Invalid status')
        if self.priority not in ['low', 'medium', 'high', 'critical']:
            raise ValueError('Invalid priority')
    
    def describe(self):
        return f"{self.title} [{self.priority}]"


class CriticalIssue(Issue):

    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"

class HighPriorityIssue(Issue):

    def describe(self):
        return f"{self.title} — high priority, address as soon as possible"
    
class MediumPriorityIssue(Issue):
    
    def describe(self):
        return f"{self.title} — medium priority, handle in due course"
        
class LowPriorityIssue(Issue):

    def describe(self):
        return f"{self.title} — low priority, handle when free"

    