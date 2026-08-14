from marshmallow import Schema, fields, validate, ValidationError, pre_dump
from app.models.task import Task


class TaskSchema(Schema):
    """Task schema for responses"""
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    status = fields.Str(
        required=True,
        validate=validate.OneOf(Task.STATUSES)
    )
    priority = fields.Str(
        required=True,
        validate=validate.OneOf(Task.PRIORITIES)
    )
    created_by = fields.Int(dump_only=True)
    assigned_to = fields.Int(allow_none=True)
    due_date = fields.DateTime(format='iso', allow_none=True, dump_default=None)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Nested user info - use Method field to extract from relationship
    creator = fields.Method('get_creator', dump_only=True)
    assignee = fields.Method('get_assignee', dump_only=True)
    
    def get_creator(self, obj):
        """Get creator info from relationship"""
        if obj.creator:
            return {
                'id': obj.creator.id,
                'name': obj.creator.name,
                'email': obj.creator.email
            }
        return None
    
    def get_assignee(self, obj):
        """Get assignee info from relationship"""
        if obj.assignee_user:
            return {
                'id': obj.assignee_user.id,
                'name': obj.assignee_user.name,
                'email': obj.assignee_user.email
            }
        return None


class TaskCreateSchema(Schema):
    """Task creation schema"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(Task.STATUSES),
        allow_none=True
    )
    priority = fields.Str(
        validate=validate.OneOf(Task.PRIORITIES),
        allow_none=True
    )
    assigned_to = fields.Int(allow_none=True)
    due_date = fields.DateTime(format='iso', allow_none=True)


class TaskUpdateSchema(Schema):
    """Task update schema"""
    title = fields.Str(validate=validate.Length(min=1, max=255), allow_none=True)
    description = fields.Str(allow_none=True)
    status = fields.Str(
        validate=validate.OneOf(Task.STATUSES),
        allow_none=True
    )
    priority = fields.Str(
        validate=validate.OneOf(Task.PRIORITIES),
        allow_none=True
    )
    assigned_to = fields.Int(allow_none=True)
    due_date = fields.DateTime(format='iso', allow_none=True)
