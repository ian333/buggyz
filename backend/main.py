from typing import List
import fastapi
from fastapi import FastAPI, security, status


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
    db_user = await services.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    user=await services.create_user(user, db)

    return await services.create_token(user)


@app.post("/api/token")
async def generate_token(form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
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
    user = await services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="invalid credentials")

    return await services.create_token(user)


@app.get("/api/users/me", response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    return user


@app.post("/api/leads", response_model=schemas.Lead)
async def create_lead(lead: schemas.LeadCreate,
                      user: schemas.User = fastapi.Depends(
                          services.get_current_user),
                      db: orm.Session = fastapi.Depends(services.get_db)):
    return await services.create_lead(user=user, db=db, lead=lead)


@app.get("/api/leads", response_model=List[schemas.Lead])
async def get_leads(
        user: schemas.User = fastapi.Depends(services.get_current_user),
        db: orm.Session = fastapi.Depends(services.get_db)):

    return await services.get_leads(user=user, db=db)


@app.get("/api/leads/{lead_id}", status_code=status.HTTP_200_OK, response_model=schemas.Lead)
async def get_lead(
    lead_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.get_lead(user=user, db=db, lead_id=lead_id)


@app.delete("/api/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: int,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    """_summary_

    Args:
        lead_id (int): _description_
        user (schemas.User, optional): _description_. Defaults to fastapi.Depends(services.get_current_user).
        db (orm.Session, optional): _description_. Defaults to fastapi.Depends(services.get_db).

    Returns:
        _type_: _description_
    """
    await services.delete_lead(user=user, db=db, lead_id=lead_id)

    


@app.put("/api/leads/{lead_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_lead(
    lead_id: int,
    lead:schemas.LeadCreate,
    user: schemas.User = fastapi.Depends(services.get_current_user),
    db: orm.Session = fastapi.Depends(services.get_db),
):
    lead_updated =await services.update_lead(user=user, db=db, lead_id=lead_id,lead=lead)
    
    return{f"message","Succesfully updated {lead_updated}"}


@app.get("/api")
async def root():
    return {"message": "BUGGYZ"}
