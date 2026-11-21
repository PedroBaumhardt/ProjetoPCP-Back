import re

from pydantic import BaseModel, EmailStr, Field, field_validator

PASSWORD_MIN_LEN = 8
# -- limite do bcrypt, em bytes utf-8 (nao em caracteres)
PASSWORD_MAX_BYTES = 72


# -- body cru da requisicao; as regras de email/senha ficam no AuthSchema, validado pelo controller
class AuthRequest(BaseModel):
    email: str
    password: str


class AuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=PASSWORD_MIN_LEN)

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password.encode("utf-8")) > PASSWORD_MAX_BYTES:
            raise ValueError(f"a senha deve ter no maximo {PASSWORD_MAX_BYTES} bytes")
        errors = []
        if not re.search(r"[A-Z]", password):
            errors.append("1 letra maiuscula")
        if not re.search(r"[a-z]", password):
            errors.append("1 letra minuscula")
        if not re.search(r"\d", password):
            errors.append("1 numero")
        if not re.search(r"[^A-Za-z0-9\s]", password):
            errors.append("1 caractere especial")
        if errors:
            raise ValueError(f"a senha deve conter ao menos: {', '.join(errors)}")
        return password
