from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from passlib.context import CryptContext

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["users_db"]
collection = db["users"]

# Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define a Pydantic model for user
class User(BaseModel):
    id: str
    username: str
    password: str

# Initialize FastAPI app
app = FastAPI()

# Endpoint for user login
@app.post("/login")
async def login(user: User):
    # Retrieve user from database
    fetched_user = collection.find_one({"username": user.username})

    # Check if user exists and verify password
    if fetched_user and pwd_context.verify(user.password, fetched_user["password"]):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# Endpoint for user registration
@app.post("/register")
async def register(user: User):
    # Check if username already exists
    if collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Insert new user into database with hashed password
    new_user = {"username": user.username, "password": hashed_password}
    result = collection.insert_one(new_user)
    
    # Get the last inserted id
    inserted_id = str(result.inserted_id)

    return {"message": "User registered successfully","inserted_id":inserted_id}

# Endpoint to get user by ID
@app.get("/user")
async def get_user(user_id: str = Query(..., description="User ID")):
    # Retrieve user from database
    fetched_user = collection.find_one({"_id": ObjectId(user_id)})

    if fetched_user:
        user_dict = {"id": str(fetched_user["_id"]), "username": fetched_user["username"], "password": fetched_user["password"]}
        return user_dict
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to update user information
@app.put("/user")
async def update_user(user: User, user_id: str = Query(..., description="User ID")):
    # Update user information in database
    updated_user = {"username": user.username, "password": pwd_context.hash(user.password)}
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user_id} updated successfully"}

# Endpoint to partially update user information
@app.patch("/user")
async def partial_update_user(user: User, user_id: str = Query(..., description="User ID")):
    # Update user information in database
    updated_fields = {}
    if user.username:
        updated_fields["username"] = user.username
    if user.password:
        updated_fields["password"] = pwd_context.hash(user.password)
    
    if updated_fields:
        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_fields})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user_id} updated successfully"}

# Endpoint to delete user
@app.delete("/user")
async def delete_user(user_id: str = Query(..., description="User ID")):
    # Delete user from database
    result = collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User {user_id} deleted successfully"}
