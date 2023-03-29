from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

import models
import schemas


#################### USER ####################


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, user_username: str):
    return db.query(models.User).filter(models.User.username == user_username).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


def get_all_users(db: Session, page: int = 0, limit: int = 100):
    return db.query(models.User).offset(page).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        token=user.token,
        username=user.username,
        name=user.name,
        email=user.email,
        avatar=user.avatar,
        phone=user.phone,
        location=user.location
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#################### ITEM ####################


def get_all_items(db: Session, category: int = None, page: int = 0, limit: int = 100, sort: str = 'id', order: str = 'asc'):
    sort_values = ['id', 'title', 'date', 'price']
    order_values = ['asc', 'desc']
    if sort not in sort_values or order not in order_values:
        if category is None:
            return db.query(models.Item).offset(page).limit(limit).all()
        return db.query(models.Item).filter(models.Item.category_id == category).offset(page).limit(limit).all()
    if category is None:
        return db.query(models.Item).order_by(text(sort + ' ' + order)).offset(page).limit(limit).all()
    return db.query(models.Item).filter(models.Item.category_id == category).order_by(text(sort + ' ' + order)).offset(page).limit(limit).all()


def get_items_by_owner_id(db: Session, owner_id: int, page: int = 0, limit: int = 100):
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).offset(page).limit(limit).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def count_items(db: Session):
    return db.query(func.count(models.Item.id)).scalar()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
