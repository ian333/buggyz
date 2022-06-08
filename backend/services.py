import database as _database
import sqlalchemy.orm as orm
import models
import schemas
import passlib.hash as hash
import jwt


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


async def authenticate_user(email:str,password:str , db=orm.Session):
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
    user = await get_user_by_email(email,db)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    
    return user
    
async def create_token(user:models.User):
    user_obj= schemas.User.from_orm(user)
    token = jwt.encode
    