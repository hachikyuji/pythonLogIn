import sqlite3
import hashlib
import threading
import socket
#  import pyotp

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

    attemptresult = cursor.fetchall()

    if attemptresult:
        '''
        otp_key = "SoftwareEngineeringQRCodeKey"
        timedotp = pyotp.TOTP(otp_key)
        while True:
            userinput = input("Enter the code from the QR (Or type 'quit' to exit): ")

            if userinput.lower() == 'quit':
                break

            verifyqr = timedotp.verify(userinput)

            if verifyqr:
                print("Login Successful.")
            else:
                print("Login Failed.")
         '''
        c.send("Login Successful!".encode())  # to be changed

    else:
        c.send("Login Failed.".encode())  # to be changed

#    conn.close()
#    c.close()

# Main loop for client connections allows for multiple connections simultaneously
    while True:
        c, address = loginserver.accept()
#        print(f"Connected to the {address}")

        threading.Thread(target=handle, args=(c,)).start()


#  input('Press ENTER to exit')
