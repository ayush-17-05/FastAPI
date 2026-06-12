from todo_app.auth import hash_password, verify_password, verify_token, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from todo_app.schemas import UserCreate
from todo_app.database import user_collection
from fastapi import HTTPException, status, APIRouter, Depends

router=APIRouter(prefix="/api/v1/users",tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

@router.post("/register")
async def register(user: UserCreate):
    existing = await user_collection.find_one({"email":user.email})
    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    hashed=hash_password(user.password)
    await user_collection.insert_one({
        "email":user.email,
        "password":hashed
    })
    return {"message":"User registered successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_access_token({"sub":user["email"]})
    return {"access_token":token,"token_type":"bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid Token")
    user = await user_collection.find_one({"email":payload.get("sub")})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

