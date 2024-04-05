from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
import sqlite3

# Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define a Pydantic model for user
class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str

# Initialize FastAPI app
app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
conn.commit()

# Endpoint for user login
@app.post("/login")
async def login(user: User):
    # Retrieve user from database
    cursor.execute("SELECT * FROM users WHERE username=?", (user.username,))
    fetched_user = cursor.fetchone()

    # Check if user exists and verify password
    if fetched_user and pwd_context.verify(user.password, fetched_user[2]):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

#perform CRUD (Create, Read, Update, Delete) operations on user data
    
# Endpoint for user registration
@app.post("/register")
async def register(user: User):
    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (user.username,))
    existing_user = cursor.fetchone()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Insert new user into database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_password))
    conn.commit()

    return {"message": "User registered successfully"}

# Endpoint to get user by ID
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    # Retrieve user from database
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    fetched_user = cursor.fetchone()

    if fetched_user:
        user_dict = {"id": fetched_user[0], "username": fetched_user[1], "password": fetched_user[2]}
        return user_dict
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Endpoint to update user information
@app.put("/user/{user_id}")
async def update_user(user_id: int, user: User):
    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Update user information in database
    cursor.execute("UPDATE users SET username=?, password=? WHERE id=?", (user.username, hashed_password, user_id))
    conn.commit()

    return {"message": f"User {user_id} updated successfully"}

# Endpoint to partially update user information
@app.patch("/user/{user_id}")
async def partial_update_user(user_id: int, user: User):
    # Update user information in database
    if user.username:
        cursor.execute("UPDATE users SET username=? WHERE id=?", (user.username, user_id))
    if user.password:
        hashed_password = pwd_context.hash(user.password)
        cursor.execute("UPDATE users SET password=? WHERE id=?", (hashed_password, user_id))
    conn.commit()

    return {"message": f"User {user_id} updated successfully"}

# Endpoint to delete user
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    # Delete user from database
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

    return {"message": f"User {user_id} deleted successfully"}
