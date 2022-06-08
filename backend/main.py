import fastapi
from fastapi import FastAPI, security, status


from sqlalchemy import orm

import services,schemas

app = FastAPI()


@app.post("/api/users")
async def create_user(
        user: schemas.UserCreate,
        db: orm.Session = fastapi.Depends(services.get_db)):
    """Create user 
    Parameters:  user: schemas.UserCreate
                db: the function get_db is call by Depends 

    Raises:
        fastapi.HTTPException: Raise an error if the user already exists!!
    Returns:
        _type_: return the user object that was created 

    """
    db_user = await services.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    return await services.create_user(user, db)


@app.post("/api/token")
async def generate_token(form_data: security.OAuth2PasswordRequestForm =fastapi.Depends(),
                         db: orm.Session = fastapi.Depends(services.get_db),
                         ):
    """_summary_

    Args:
        form_data (security.OAuth2PasswordRequestForm, optional): _description_. Defaults to fastapi.Depends().
        db (orm.Session, optional): _description_. Defaults to fastapi.Depends(services.get_db).

    Raises:
        fastapi.HTTPException: _description_

    Returns:
        _type_: _description_
    """
    user= await services.authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials")
    
    return await services.create_token(user)

@app.get("/api/users/me",response_model = schemas.User)
async def get_user(user:schemas.User=fastapi.Depends(services.get_current_user)):
    return user

@app.get("/")
def hello_world():
    return {"hello": "world"}
