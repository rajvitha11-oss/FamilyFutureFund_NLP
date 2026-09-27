import os
import mysql.connector

db = mysql.connector.connect(

    host="familyfuturefund-db-family-future-fund.c.aivencloud.com",

    port=28994,

    user="avnadmin",

    password=os.getenv("AIVEN_DB_PASSWORD"),

    database="defaultdb"

)

cursor = db.cursor()