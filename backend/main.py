import fastapi
from fastapi import FastAPI, security,status


from sqlalchemy import orm

import services
import schemas

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
    db_user= await services.get_user_by_email(user.email,db)
    if db_user:
        raise fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already in use")

    return await services.create_user(user,db)

@app.post("/api/token")
async def generate_token(form_data:security.OAuth2PasswordRequestForm= fastapi.Depends(),db:orm.Session=fastapi.Depends(services.get_db())):
    pass
@app.get("/")
def hello_world():
    return {"hello":"world"}



