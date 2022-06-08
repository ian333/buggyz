import database as _database
import sqlalchemy.orm as orm
import models
import schemas
import passlib.hash as hash


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
    return db.query(models.User).filter(models.User.email == email).first()


async def create_user(user: schemas.UserCreate, db: orm.Session):
    """_summary_

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
