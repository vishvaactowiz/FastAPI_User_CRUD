import mysql.connector

# MYSQL CONNECTION
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="userdb"
)

cursor = mydb.cursor()


# CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),
    surname VARCHAR(100),
    email VARCHAR(100)
)
""")

mydb.commit()