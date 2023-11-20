import pyotp
import qrcode

key = "NeuralNineMySuperSecretKey"

#uri = pyotp.totp.TOTP(key).provisioning_uri(name="MikeSmith123", issuer_name="NeuralNine App")

#print(uri)

#qrcode.make(uri).save("totp.png")

totp = pyotp.TOTP(key)

while True:
    print(totp.verify(input("Enter Code:")))