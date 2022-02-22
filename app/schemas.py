from typing import Optional

from pydantic import BaseModel

class BaseTeam(BaseModel):
    name: Optional[str] = None
    pokemon: str
    pokemon2: str
    pokemon3: str

class CreateTeam(BaseTeam):
    pass

class Team(BaseTeam):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class BaseUser(BaseModel):
    username: str
    email: str


class CreateUser(BaseUser):
    password: str

class User(BaseUser):
    id: int
    is_active: bool
    teams: list[Team] = []

    class Config:
        orm_mode = True