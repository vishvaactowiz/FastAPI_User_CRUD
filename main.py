from fastapi import FastAPI
from pydantic import BaseModel
from db import mydb, cursor
from typing import Optional
app = FastAPI()


# Pydantic Model
class User(BaseModel):
    username: str
    password: str
    surname: str
    email: str

class UpdateUser(BaseModel):
    email: str
    username: Optional[str] = None
    password: Optional[str] = None
    surname: Optional[str] = None
# CREATE USER
@app.post("/create_users/")
def create_user(user: User):

    # CHECK USER EXISTS
    check_query = "SELECT * FROM users WHERE email = %s OR username = %s"
    cursor.execute(check_query, (user.email, user.username))
    existing_user = cursor.fetchone()
    if existing_user:
        return {"message": "User already exists"}
    query = "INSERT INTO users (username, password, surname, email) VALUES (%s, %s, %s, %s)"
    values = (
        user.username,
        user.password,
        user.surname,
        user.email
    )
    cursor.execute(query, values)
    mydb.commit()
    return {"message": "User created successfully"}


# GET ALL USERS
@app.get("/users/")
def get_users():
    query = "SELECT * FROM users"
    cursor.execute(query)
    data = cursor.fetchall()
    users = []
    for row in data:
        users.append({
            "id": row[0],
            "username": row[1],
            "password": row[2],
            "surname": row[3],
            "email": row[4]
        })

    return users


# UPDATE USER USING EMAIL
@app.put("/update_users/")
def update_user(user: UpdateUser):
    check_query = "SELECT * FROM users WHERE email=%s"
    cursor.execute(check_query, (user.email,))
    existing_user = cursor.fetchone()
    if not existing_user:
        return {"message": "User not found"}
    if user.username:
        query = "UPDATE users SET username=%s WHERE email=%s"
        cursor.execute(query, (user.username, user.email))
    if user.password:
        query = "UPDATE users SET password=%s WHERE email=%s"
        cursor.execute(query, (user.password, user.email))
    if user.surname:
        query = "UPDATE users SET surname=%s WHERE email=%s"
        cursor.execute(query, (user.surname, user.email))
    mydb.commit()

    return {"message": "User updated successfully"}

# DELETE USER USING EMAIL
@app.delete("/delete_users/")
def delete_user(email: str):
    check_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(check_query, (email,))
    existing_user = cursor.fetchone()
    if not existing_user:
        return {"message": "User not found"}
    query = "DELETE FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    mydb.commit()
    return {"message": "User deleted successfully"}