from fastapi import APIRouter, HTTPException
from database import users_collection
from models import UserCreate, UserResponse, EmailSchema, VerifyOTPSchema
from auth import hash_password
from bson import ObjectId
from utils.email_util import send_otp_email, generate_otp
from datetime import datetime, timedelta



router = APIRouter(
    prefix="/users",
     tags=["Users"]
)

otp_store = {}

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    existing =  users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)

    doc = {"name": user.name, "email": user.email, "password": hashed}

    result =  users_collection.insert_one(doc)

    return UserResponse(
        id=str(result.inserted_id),
        name=user.name,
        email=user.email
    )



@router.post("/send-otp")
async def send_otp(data: EmailSchema):
    otp = generate_otp()

    # send email
    send_otp_email(data.email, otp)
    print("OTP sent:", otp)

    # 🔥 Save OTP in DB if needed
    # await users_collection.update_one({"email": data.email}, {"$set": {"otp": otp}}, upsert=True)

    return {"message": "OTP sent successfully!", "otp": otp}




@router.post("/verify-otp")
def verify_otp(data: VerifyOTPSchema):
    record = otp_store.get(data.email)

    if not record:
        raise HTTPException(status_code=404, detail="OTP not found or expired")

    if record["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.utcnow() > record["expiry"]:
        otp_store.pop(data.email, None)
        raise HTTPException(status_code=400, detail="OTP expired")

    # OTP verified → remove it
    otp_store.pop(data.email, None)

    return {"message": "OTP verified successfully"}
