from fastapi import FastAPI, HTTPException, Depends 
from fastapi.security import OAuth2PasswordBearer 
from pydantic import BaseModel 
import redis 
import random 
import smtplib 
from passlib.context import CryptContext
app = FastAPI() 
r = redis.Redis() 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel): 
    email: str
class Verification(BaseModel): 
    email: str 
    code: int 
    name: str 
    password: str
class Login(BaseModel): 
    email: str 
    password: str
class RefreshToken(BaseModel): 
    email: str 
    refresh_token: str
@app.post("/create_user")
def create_user(user: User):
    code = random.randint(1000, 9999) 
    r.set(user.email, code) 
    send_email(user.email, code) 
    return {"message": "Verification code sent to email"}
def send_email(email: str, code: int):
    pass
@app.post("/verify_and_register") 
def verify_and_register(verification: Verification):
    stored_code = r.get(verification.email) 
    if stored_code and int(stored_code) == verification.code: 
        # Регистрация пользователя 
        r.delete(verification.email) 
        return {"message": "User registered successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid code")

@app.post("/login")
def login(login: Login):
    hashed_password = pwd_context.hash(login.password) 
    access_token = "access_token_example" 
    refresh_token = "refresh_token_example" 
    r.set(f"access_{login.email}", access_token) 
    r.set(f"refresh_{login.email}", refresh_token) 
    return {"access_token": access_token, "refresh_token": refresh_token}
@app.post("/refresh_token")
def refresh_token(refresh: RefreshToken):
    stored_refresh_token = r.get(f"refresh_{refresh.email}")
    if stored_refresh_token and stored_refresh_token.decode() == refresh.refresh_token:
        new_access_token = "new_access_token_example" 
        r.set(f"access_{refresh.email}", new_access_token)
        return {"access_token": new_access_token}
    else:
        raise HTTPException(status_code=400, detail="Invalid refresh token")

@app.get("/user")
def get_user(token: str = Depends(oauth2_scheme)):
    pass

@app.put("/user")
def update_user(token: str = Depends(oauth2_scheme)):
    pass

@app.delete("/user")
def delete_user(token: str = Depends(oauth2_scheme)):
    pass

if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=8000)