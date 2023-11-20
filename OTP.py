import pyotp
import time
import qrcode
import base64


otp_key = "SoftwareEngineeringQRCodeKeyAdmin"
'''
otp_uri = pyotp.totp.TOTP(otp_key).provisioning_uri(name='softwareeng', issuer_name='Mr.Morano')

print(otp_uri)

qr = qrcode.make(otp_uri)
qr.save("otpqr.png")
'''

otp_uri = pyotp.totp.TOTP(otp_key).provisioning_uri(name='softwareeng', issuer_name='PLMAdmin')

print(otp_uri)

qr = qrcode.make(otp_uri)
qr.save("admin_otp_qr.png")

'''
timedotp = pyotp.TOTP(otp_key)

#   while True:

#   print(timedotp.verify(input("Enter the code from the QR:")))

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

