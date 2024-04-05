from fastapi import FastAPI, HTTPException

app = FastAPI()

# Endpoint for user login (GET request)
@app.get("/login")
async def login(username: str, password: str):
    # Perform authentication logic here
    if username == "salimsouidi7" and password == "1234":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# Endpoint for user login (POST request)
@app.post("/login")
async def login_post(username: str, password: str):
    # Perform authentication logic here
    if username == "salimsouidi7" and password == "1234":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

# Endpoint for updating user information (PUT request)
@app.put("/user/{user_id}")
async def update_user(user_id: int, username: str, password: str):
    # Example logic for updating user information
    # This endpoint is typically used to completely replace existing user data
    # You might want to implement proper authentication and authorization checks here
    # For simplicity, we're not performing any checks in this example
    return {"message": f"User {user_id} updated successfully"}

# Endpoint for partially updating user information (PATCH request)
@app.patch("/user/{user_id}")
async def partial_update_user(user_id: int, username: str = None, password: str = None):
    # Example logic for partially updating user information
    # This endpoint is used to update only the provided fields
    # You might want to implement proper authentication and authorization checks here
    # For simplicity, we're not performing any checks in this example
    updated_fields = {}
    if username is not None:
        updated_fields["username"] = username
    if password is not None:
        updated_fields["password"] = password
    return {"message": f"User {user_id} updated successfully", "updated_fields": updated_fields}
