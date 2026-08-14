from marshmallow import Schema, fields, validate, ValidationError, post_load


class UserSchema(Schema):
    """User schema for responses"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    role = fields.Str(validate=validate.OneOf(['user', 'admin']))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserRegisterSchema(Schema):
    """User registration schema"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255),
        load_only=True
    )
    password_confirm = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255),
        load_only=True
    )
    
    @post_load
    def validate_passwords(self, data, **kwargs):
        """Validate that passwords match"""
        if data.get('password') != data.get('password_confirm'):
            raise ValidationError('Passwords do not match.')
        return data


class UserLoginSchema(Schema):
    """User login schema"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
