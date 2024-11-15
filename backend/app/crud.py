from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, is_admin: int=0):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def edit_users(db: Session, user_info: schemas.UserEdit, is_admin: int=0):
    user = db.query(models.User).filter(models.User.id == user_info.id).first()
    if user:
        if is_admin == 1:
            user.username = user_info.username
            user.is_admin = user_info.is_admin
            if user_info.password is not None: 
                user.hashed_password = pwd_context.hash(user_info.password)
            db.commit()
            db.refresh(user)
            return {"message": "编辑成功！"}
    return {"message": "编辑失败！"}

def delete_user(db: Session, user_id: int, is_admin: int=0):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        if user.username != "admin" and is_admin == 1:
            db.delete(user)
            db.commit()
            return {"message": "删除成功！"}
    return {"message": "删除失败！"}
