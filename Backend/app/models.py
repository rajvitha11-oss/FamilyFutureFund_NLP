import mysql.connector


db = mysql.connector.connect(

    host="localhost",
    user="root",
    password="1234",
    database="family_future_fund"

)


cursor = db.cursor()