import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password',
    database='mfalogin',
    auth_plugin='password',
)