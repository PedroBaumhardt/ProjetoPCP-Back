import re

from pydantic import BaseModel, EmailStr, Field, field_validator

PASSWORD_MIN_LEN = 8


class AuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=PASSWORD_MIN_LEN)

    @field_validator("password")
    @classmethod
    def validar_password(cls, password: str) -> str:
        erros = []
        if not re.search(r"[A-Z]", password):
            erros.append("1 letra maiuscula")
        if not re.search(r"[a-z]", password):
            erros.append("1 letra minuscula")
        if not re.search(r"\d", password):
            erros.append("1 numero")
        if not re.search(r"[^A-Za-z0-9\s]", password):
            erros.append("1 caractere especial")
        if erros:
            raise ValueError(f"a senha deve conter ao menos: {', '.join(erros)}")
        return password
