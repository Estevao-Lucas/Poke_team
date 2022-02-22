from fastapi import status, HTTPException
from app import models, schemas
from sqlalchemy.orm import Session


def get_teams(db: Session):
    '''Lista todos os Times'''
    return db.query(models.Team).all()


def create_user_team(db: Session, team: schemas.CreateTeam, user_id: int):
    '''Criação de um time para o usuário'''
    db_team = models.Team(**team.dict(), owner_id=user_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(db: Session, team_id: int, team:schemas.Team, owner_id:int):
    '''Atualiza um time'''
    team_to_update = db.query(models.Team).filter(models.Team.id == team_id).first()
    team_to_update.name = team.name
    team_to_update.pokemon = team.pokemon
    team_to_update.pokemon2 = team.pokemon2
    team_to_update.pokemon3 = team.pokemon3
    team_to_update.owner_id = team.owner_id
    db.commit()
    return team_to_update

def delete_team(db: Session, team_id:int):
    '''Deleta um time'''
    team_to_delete = db.query(models.Team).filter(models.Team.id == team_id).first()

    if team_to_delete is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Team Not Found")

    db.delete(team_to_delete)
    db.commit()

    return team_to_delete