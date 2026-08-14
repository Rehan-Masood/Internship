from app import db
from datetime import datetime


class Task(db.Model):
    """Task model"""
    __tablename__ = 'tasks'
    
    # Status constants
    STATUS_PENDING = 'Pending'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_COMPLETED = 'Completed'
    
    STATUSES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED]
    
    # Priority constants
    PRIORITY_LOW = 'Low'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_HIGH = 'High'
    
    PRIORITIES = [PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH]
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False, index=True)
    priority = db.Column(db.String(20), default=PRIORITY_MEDIUM, nullable=False, index=True)
    
    # Foreign keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_assignee=True):
        """Convert task to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_by': self.created_by,
            'assigned_to': self.assigned_to,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_assignee and self.assignee_user:
            data['assignee'] = {
                'id': self.assignee_user.id,
                'name': self.assignee_user.name,
                'email': self.assignee_user.email
            }
        
        if self.creator:
            data['creator'] = {
                'id': self.creator.id,
                'name': self.creator.name,
                'email': self.creator.email
            }
        
        return data
    
    def __repr__(self):
        return f'<Task {self.title}>'
