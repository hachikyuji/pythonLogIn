import smtplib
import os
from email.message import EmailMessage
import ssl
import pyotp
import qrcode
import random
import string

length = 16

random_key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567') for _ in range(length))

padding = (8 - (len(random_key) % 8)) % 8
random_key += '=' * padding

otp_key = f"SoftwareEngineeringQRCodeKeyAdmi{random_key}"

otp_uri = pyotp.totp.TOTP(otp_key).provisioning_uri(name=random_key, issuer_name='PLMDasboard')

print(otp_uri)

qr = qrcode.make(otp_uri)
qr.save("random_qr.png")

email_sender = 'muringjohncarlo@gmail.com'
email_password = 'ubbktwppsmkvfsdf'
email_receiver = 'thorfin036@gmail.com'

subject = 'Account Verification'
body = """
Verify your account with this QR Code:
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

qr_code_img = "random_qr.png"

with open(qr_code_img, 'rb') as image_file:
    image_file = image_file.read()
    image_name = os.path.basename(qr_code_img)
    em.add_attachment(
        image_file,
        maintype='image',
        subtype='png',
        filename=image_name
    )

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

    timedotp = pyotp.TOTP(otp_key)

    while True:
        userinput = input("Enter the code from the QR (Or type 'quit' to exit): ")

        print(userinput)

        if userinput.lower() == 'quit':
            break

        verifyqr = timedotp.verify(userinput)

        if verifyqr:
            print("Login Successful.")
        else:
            print("Login Failed.")
