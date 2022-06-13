from pyexpat import model
import fastapi
from fastapi import HTTPException, security, status
import database as _database
import sqlalchemy.orm as orm
import models
import schemas
import passlib.hash as hash
import jwt
from decouple import config
import datetime as dt

oauth2schema = security.OAuth2PasswordBearer(tokenUrl="/api/token")


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    """This function creates a class Session and it's used to make request to the DB
    and get the data

    Yields:
        database: Return a local session of the DB to get the data
    """
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: orm.Session):
    """this function search an user in the Database by the email

    Args:
        email (str): user email
        db (orm.Session): Database

    Returns:
        User: return the user 

    """
    return db.query(models.User).filter(models.User.email == email).first()


async def create_user(user: schemas.UserCreate, db: orm.Session):
    """This function Create the user in the database with an email 
    and encrypt the password 

    Args:
        user (schemas.UserCreate): schema of userCreate hashed password
        db (orm.Session): _description_

    Returns:
        _type_: return a user Object

    """
    user_obj = models.User(
        email=user.email,
        hashed_password=hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db=orm.Session):
    """This function is to authenticate the user verify the password

    Args:
        email (str): User Email
        password (str): User Email
        db (_type_, optional):  Defaults to orm.Session.
    Returns :
        if the user Doesn't exists 
        return a boolean False
        if the password doesn't match 
        return a boolean False
        if the user & the password match
        return the User

    """
    user = await get_user_by_email(email=email, db=db)
    if not user:
        return False
    if not user.verify_password(password):
        return False

    return user


async def create_token(user: models.User):
    """This function creates a bearer token with a User model converted in a dict


    Args:
        user (models.User): A user model to covert into a dict

    Returns:
        dict: returns a dict with the bearer token created with the User 
    """
    user_obj = schemas.User.from_orm(user)
    token = jwt.encode(user_obj.dict(), config("JWT_SECRET"))

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: orm.Session = fastapi.Depends(get_db), token: str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, config("JWT_SECRET"), algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid Email or password")

    return schemas.User.from_orm(user)


async def create_lead(user: schemas.User, db: orm.Session, lead: schemas.LeadCreate):
    lead = models.Lead(**lead.dict(), owner_id=user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return schemas.Lead.from_orm(lead)


async def get_leads(user: schemas.User, db: orm.Session):
    leads = db.query(models.Lead).filter_by(owner_id=user.id)
    return list(map(schemas.Lead.from_orm, leads))


async def lead_selector(user: schemas.User, db: orm.Session, lead_id: int):
    lead = db.query(models.Lead).filter_by(
        owner_id=user.id).filter(models.Lead.id == lead_id).first()

    if lead is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=" The lead Doesn't Exist")
    return lead


async def get_lead(user: schemas.User, db: orm.Session, lead_id: int):
    lead = await lead_selector(user=user, db=db, lead_id=lead_id)
    return schemas.Lead.from_orm(lead)


async def delete_lead(user: schemas.User, db: orm.Session, lead_id: int):
    lead = await lead_selector(user=user, db=db, lead_id=lead_id)
    db.delete(lead)
    db.commit()


async def update_lead(user: schemas.User, db: orm.Session, lead_id: int, lead: schemas.LeadCreate):

    lead_db = await lead_selector(user=user, db=db, lead_id=lead_id)

    lead_db.first_name = lead.first_name
    lead_db.last_name = lead.last_name
    lead_db.email = lead.email
    lead_db.company = lead.company
    lead_db.note = lead.note
    lead_db.last_updated = dt.datetime.utcnow()
    db.commit()
    db.refresh(lead_db)
    return schemas.Lead.from_orm(lead_db)

