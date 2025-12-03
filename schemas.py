from marshmallow import Schema, fields, validate, ValidationError, validates_schema
import re

class RegistrationSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email обязателен"})
    password = fields.String(
        required=True, 
        validate=[
            validate.Length(min=8, error="Пароль должен быть минимум 8 символов"),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
                error="Пароль должен содержать хотя бы одну заглавную букву, одну строчную букву и одну цифру"
            )
        ]
    )
    confirm_password = fields.String(required=True)
    name = fields.String(
        required=True,
        validate=[validate.Length(min=2, max=80, error="Имя должно быть от 2 до 80 символов")]
    )
    
    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("Пароли не совпадают", "confirm_password")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RefreshTokenSchema(Schema):
    refresh_token = fields.String(required=True)


class UserUpdateSchema(Schema):
    name = fields.String(validate=[validate.Length(min=2, max=80)])
    email = fields.Email()