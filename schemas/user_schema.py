from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=20))
    password = fields.Str(required=True, validate=validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", flags=0, error="Password is not strong enough."))
    role_id = fields.Int(dump_only=True)