from fastapi import FastAPI, Depends, HTTPException
import requests

from sqlalchemy.orm import Session

import crud_team,crud_user, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    '''Criação de Usuário'''
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    '''Lista todos os Usuários'''
    users = crud_user.get_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    '''Mostra os dados do usuário'''
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/teams/", response_model=schemas.Team)
def create_team_for_user(
    user_id: int, team: schemas.CreateTeam, db: Session = Depends(get_db)
):
    '''Criação de Time para um Usuário'''
    return crud_team.create_user_team(db=db, team=team, user_id=user_id)


@app.get("/teams/", response_model=list[schemas.Time])
def read_teams(db: Session = Depends(get_db)):
    '''Mostra a Lista de Times'''
    teams = crud_team.get_teams(db)
    return teams

@app.put("/teams/{team_id}", response_model=schemas.Team)
def update_team(
    team_id: int, time: schemas.Team,
    db: Session = Depends(get_db)):
    '''Atualiza o time desejado'''
    return crud_team.update_team(db=db, team_id=team_id, team=time)

@app.delete("/teams/{team_id}", response_model=schemas.Team)
def delete_team(team_id:int, db:Session = Depends(get_db)):
    '''Deleta Time'''
    return crud_team.delete_team(db=db, team_id=team_id)

@app.get("/pokemon")
def get_pokemon(pokemon:str):
    '''Consome a PokeAPI, mostrando os dados do pokemon desejado'''
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}/'
    r = requests.get(url)
    dados = r.json()
    return {"name" : dados['name'],
            "id" : dados['id'],
            "weight" : dados['weight'],
            "type" : dados["types"][0]["type"]["name"]}
