import sqlite3
import hashlib
import threading
import socket

loginserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
loginserver.bind(("localhost", 9999))

loginserver.listen()

def handle(c):
    c.send("Input username: ".encode())
    userna = c.recv(1024).decode()
    c.send("Password: ".encode())
    passwo = c.recv(1024).decode()
    passwo = hashlib.sha256(passwo).hexdigest()

    conn = sqlite3.connect("logindatabase.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logindatabase WHERE userna = ? AND password = ?", (userna, passwo))

    if cursor.fetchall():
        c.send("Login Successful!".encode())
    else:
        c.send("Login Failed.".encode())

    while True:
        client, address = loginserver.accept()
#        print(f"Connected to the {address}")
        threading.Thread(target=handle, args=(client,)).start()

#  input('Press ENTER to exit')
