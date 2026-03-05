from pydantic import BaseModel


class UserDTO(BaseModel):
    email: str
    password: str
    is_admin: bool
    needs_pw_change: bool

