import tkinter
import tkinter as tk
from tkinter import *
from tkinter import font, messagebox, ttk
from PIL import Image, ImageTk
import pyotp
import mysql.connector
import smtplib
import random
import qrcode
import os
from email.message import EmailMessage
import ssl
import subprocess

db = mysql.connector.connect(
    host='localhost',
    password='password',
    user='root',
    database='testdb'
)

mycursor = db.cursor()

root = None
pass_window = None
smtp_window = None
signup_window = None
verifycredstu_window = None
verifycredadm_window = None

otp_key = ""
login_otp_key = ""
admin_login_otp_key = ""

def verifyemail():
    def verifyemailqr():
        global otp_key
        email = smtp_email_entry.get()
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
        email_receiver = email

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

    def verifyqr():
        global otp_key
        timedotp = pyotp.TOTP(otp_key)
        verification = timedotp.verify(smtp_qr_entry.get())
        if verification:
            messagebox.showinfo("Notice", "Admin account creation successful!")
        if verification:
            new_credentialadm()
            smtp_window.destroy()
        else:
            messagebox.showinfo("Notice", "Please check the QR code again properly.")

        global smtp_window

    smtp_window = Toplevel()
    smtp_window.title("DASHBOARD ADMIN ACCESSS")
    smtp_window.geometry("1366x768")

    smtp_image = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\adminverifyemail.png'

    smtp_img = Image.open(smtp_image)
    smtp_img = smtp_img.resize((1366, 768))
    smtp_img = ImageTk.PhotoImage(smtp_img)
    smtp_label = tk.Label(smtp_window, image=smtp_img)

    smtp_email_entry = tk.Entry(smtp_window)
    smtp_qr_entry = tk.Entry(smtp_window)
    smtp_button = tk.Button(smtp_window, text="Enter", command=verifyemailqr)
    smtp_qr_button = tk.Button(smtp_window, text="Enter", command=verifyqr)

    smtp_email_entry.place(x=600, y=330)
    smtp_qr_entry.place(x=600, y=430)
    smtp_button.place(x=650, y=360)
    smtp_qr_button.place(x=650, y=460)
    smtp_label.place(x=0, y=0, relwidth=1, relheight=1)
    smtp_window.mainloop()


def verifyemailpass():
    global signup_window

    if signup_window:
        signup_window.destroy()

    def ververifyemailpass():
        password = pw_userenter.get()
        admin_password = 'Shu>@B_^5j6,?ws=a,7Hm!<W5t~*pe{8B{c`&)x4="nsDX/VD#XV?p:=WGkv6S7Y!6@DNs=wtP8)7*5'
        if password == admin_password:
            messagebox.showinfo("Notice", "Success! Proceed in email verification.")
            pass_window.destroy()

        else:
            messagebox.showinfo("WARNING", "Access Denied!")
        if password == admin_password:
            verifyemail()

    global pass_window

    pass_window = Toplevel()
    pass_window.title("DASHBOARD ADMIN ACCESSS")
    pass_window.geometry("1366x768")

    pw_photoimage = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\notrespass.png'

    pw_photoimg = Image.open(pw_photoimage)
    pw_photoimg = pw_photoimg.resize((1366, 768))
    pw_photoimg = ImageTk.PhotoImage(pw_photoimg)
    pw_label = tk.Label(pass_window, image=pw_photoimg)

    #    pw_userlabel = tk.Label(pass_window, text="Give the password provided by administrators to authorized personnel:")
    pw_userenter = tk.Entry(pass_window, show="*", width=30)
    pw_button = tk.Button(pass_window, text="Enter", command=ververifyemailpass)

    #    pw_userlabel.place(x=260, y=150)
    pw_userenter.place(x=580, y=380)
    pw_button.place(x=650, y=410)
    pw_label.place(x=0, y=0, relwidth=1, relheight=1)
    pass_window.mainloop()


def run_code():
    try:
        # Replace 'your_script.py' with the name of your Python script
        subprocess.run(["python", "your_script.py"])
    except Exception as e:
        print(f"An error occurred: {e}")


'''
test codes above
'''

def switch_frame(frame):
    frame.tkraise()

def dashboardadm():
    global root
    root.withdraw()
    db_window = Toplevel()
    db_window.title("PLM Dashboard: ADMIN")
    db_window.geometry("1366x768")

    db_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\dashboard.png'

    tk_dashboard_image = Image.open(db_photoimg)
    tk_dashboard_image = tk_dashboard_image.resize((1366, 768))
    tk_dashboard_image = ImageTk.PhotoImage(tk_dashboard_image)
    db_label = tk.Label(db_window, image=tk_dashboard_image)

    db_label.place(x=0, y=0, relwidth=1, relheight=1)

    db_window.mainloop()

def dashboardstu():
    global root
    root.withdraw()
    adm_db_window = Toplevel()
    adm_db_window.title("PLM Dashboard: STUDENT")
    adm_db_window.geometry("1366x768")

    db_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\dashboard.png'

    tk_dashboard_image = Image.open(db_photoimg)
    tk_dashboard_image = tk_dashboard_image.resize((1366, 768))
    tk_dashboard_image = ImageTk.PhotoImage(tk_dashboard_image)
    db_label = tk.Label(adm_db_window, image=tk_dashboard_image)

    adm_container = ttk.Frame(root)
    adm_container.place(fill='both', expand=True)

    adm_home = ttk.Frame(adm_container)
    ttk.Label(adm_home, text="Test Home Page").pack()
    ttk.Button(adm_home, text="Profile", command=lambda: switch_frame(adm_profile)).pack()

    adm_profile = ttk.Frame(adm_container)
    ttk.Label(adm_profile, text="Test Profile Page").pack()
    ttk.Button(adm_home, text="Home", command=lambda :switch_frame(adm_home)).pack()

    db_label.place(x=0, y=0, relwidth=1, relheight=1)
    adm_db_window.mainloop()

    for frame in (adm_home, adm_profile):
        frame.grid(row=0, column=0, sticky="nsew")

    switch_frame(adm_home)

def verifycredadm(username, password, email, callback):
    global admin_login_otp_key
    length = 16

    random_key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567') for _ in range(length))

    padding = (8 - (len(random_key) % 8)) % 8
    random_key += '=' * padding

    admin_login_otp_key = f"SoftwareEngineeringQRCodeKeyAdmi{random_key}"

    otp_uri = pyotp.totp.TOTP(admin_login_otp_key).provisioning_uri(name=random_key, issuer_name='PLMDasboard')

    print(otp_uri)

    qr = qrcode.make(otp_uri)
    qr.save("random_qr.png")

    email_sender = 'muringjohncarlo@gmail.com'
    email_password = 'ubbktwppsmkvfsdf'
    email_receiver = email

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

    def verifyqr():
        global admin_login_otp_key
        timedotp = pyotp.TOTP(admin_login_otp_key)
        verify_qr = timedotp.verify(userinput_enter.get())
        callback(verify_qr)
        verifycredadm_window.destroy()
        dashboardadm()
    global verifycredadm_window

    verifycredadm_window = Toplevel(root)
    verifycredadm_window.title("QR Code Verification")
    verifycredadm_window.geometry("1366x768")

    verstu_image = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\qrcodescreenadm.png'

    verstu_img = Image.open(verstu_image)
    verstu_img = verstu_img.resize((1366 ,768))
    verstu_img = ImageTk.PhotoImage(verstu_img)

    verstu_label = tk.Label(verifycredadm_window, image=verstu_img)
    verstu_label.image = verstu_img

    userinput_enter = tk.Entry(verifycredadm_window, show="*", width=40)
    create_but = tk.Button(verifycredadm_window, text="Enter", command=verifyqr)

    userinput_enter.place(x=555, y=400)
    create_but.place(x=660, y=430)
    verstu_label.place(x=0, y=0, relheight=1, relwidth =1)
    verifycredadm_window.mainloop()

def verifycredstu(username, password, email, callback):
    global login_otp_key
    length = 16

    random_key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567') for _ in range(length))

    padding = (8 - (len(random_key) % 8)) % 8
    random_key += '=' * padding

    login_otp_key = f"SoftwareEngineeringQRCodeKeyAdmi{random_key}"

    otp_uri = pyotp.totp.TOTP(login_otp_key).provisioning_uri(name=random_key, issuer_name='PLMDasboard')

    print(otp_uri)

    qr = qrcode.make(otp_uri)
    qr.save("random_qr.png")

    email_sender = 'muringjohncarlo@gmail.com'
    email_password = 'ubbktwppsmkvfsdf'
    email_receiver = email

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

    def verifyqr():
        global login_otp_key
        timedotp = pyotp.TOTP(login_otp_key)
        verify_qr = timedotp.verify(userinput_enter.get())
        callback(verify_qr)
        verifycredstu_window.destroy()
        dashboardstu()
    global verifycredstu_window

    verifycredstu_window = Toplevel(root)
    verifycredstu_window.title("QR Code Verification")
    verifycredstu_window.geometry("1366x768")

    verstu_image = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\qrcodescreenstu.png'

    verstu_img = Image.open(verstu_image)
    verstu_img = verstu_img.resize((1366 ,768))
    verstu_img = ImageTk.PhotoImage(verstu_img)

    verstu_label = tk.Label(verifycredstu_window, image=verstu_img)
    verstu_label.image = verstu_img

    userinput_enter = tk.Entry(verifycredstu_window, show="*", width=40)
    create_but = tk.Button(verifycredstu_window, text="Enter", command=verifyqr)

    userinput_enter.place(x=555, y=400)
    create_but.place(x=660, y=430)
    verstu_label.place(x=0, y=0, relheight=1, relwidth =1)
    verifycredstu_window.mainloop()


def handle_verification_result(result):
    if result:
        result_label.config(text="Login Successful.")
    else:
        result_label.config(text="Login Failed.")


def new_credentialadm():
    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()

        if not username or not password or not email:
            messagebox.showinfo("Notice", "Please fill all of the fields.")
            return

        mycursor.execute("SELECT * FROM logindatabase WHERE username = %s", (username,))
        existing_data = mycursor.fetchone()

        if existing_data:
            query = "INSERT INTO logindatabase (username, password, email) VALUES (%s, %s, %s)"
            data = (username, password, email)
            mycursor.execute(query, data)

            otp = str(random.randint(100000, 999999))
            query = "UPDATE logindatabase SET otp = %s WHERE username = %s"
            data = (otp, username)
            mycursor.execute(query, data)
            db.commit()

            account_type = 'admin'
            query = "UPDATE logindatabase SET account_type = %s WHERE username = %s"
            data = (account_type, username)
            mycursor.execute(query, data)
            db.commit()
            admsignup_window.destroy()
        else:
            messagebox.showinfo("Notice", "Contact an administrator for a properly issued username before proceeding.")


    admsignup_window = Toplevel(root)
    admsignup_window.title("SignUp Screen: ADMIN")
    admsignup_window.geometry("1366x768")

    su_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\signup2.png'

    tk_signup_image = Image.open(su_photoimg)
    tk_signup_image = tk_signup_image.resize((1366, 768))
    tk_signup_image = ImageTk.PhotoImage(tk_signup_image)

    su_label = tk.Label(admsignup_window, image=tk_signup_image)
    su_label.image = tk_signup_image

    username_entry = tk.Entry(admsignup_window)
    password_entry = tk.Entry(admsignup_window, show="*")
    email_entry = tk.Entry(admsignup_window)
    run_button = tk.Button(root, text="Run Code", command=run_code)
    create_button = tk.Button(admsignup_window, text="Sign Up", command=create_account)

    username_entry.place(x=600, y=300, width=200)
    password_entry.place(x=600, y=360, width=200)
    email_entry.place(x=600, y=420, width=200)
    create_button.place(x=600, y=460, width=200)
    su_label.place(x=0, y=0, relwidth=1, relheight=1)
    run_button.grid(row=4, column=0)


def new_credentialstu():
    global signup_window

    signup_window = Toplevel(root)
    signup_window.title("SignUp Screen")
    signup_window.geometry("1366x768")

    su_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\signup.png'

    tk_signup_image = Image.open(su_photoimg)
    tk_signup_image = tk_signup_image.resize((1366 ,768))
    tk_signup_image = ImageTk.PhotoImage(tk_signup_image)
    su_label = tk.Label(signup_window, image=tk_signup_image)

    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()

        if not username or not password or not email:
            messagebox.showinfo("Notice", "Please fill all of the fields.")
            return

        mycursor.execute("SELECT * FROM logindatabase WHERE username = %s", (username,))
        existing_data = mycursor.fetchone()

        if existing_data:
            query = "INSERT INTO logindatabase (username, password, email) VALUES (%s, %s, %s)"
            data = (username, password, email)
            mycursor.execute(query, data)

            otp = str(random.randint(100000, 999999))
            query = "UPDATE logindatabase SET otp = %s WHERE username = %s"
            data = (otp, username)
            mycursor.execute(query, data)
            db.commit()

            account_type = 'student'
            query = "UPDATE logindatabase SET account_type = %s WHERE username = %s"
            data = (account_type, username)
            mycursor.execute(query, data)
            db.commit()
            signup_window.destroy()
        else:
            messagebox.showinfo("Notiice", "Contact an administrator for a properly issued username before proceeding.")



    username_entry = tk.Entry(signup_window)
    password_entry = tk.Entry(signup_window, show="*")
    email_entry = tk.Entry(signup_window)
    run_button = tk.Button(root, text="Run Code", command=run_code)
    create_button = tk.Button(signup_window, text="Sign Up", command=create_account)
    admin_signup_button = tk.Button(signup_window, text="Press here if you're an admin.", command=verifyemailpass)

    username_entry.place(x=600, y=300, width=200)
    password_entry.place(x=600, y=360, width=200)
    email_entry.place(x=600, y=420, width=200)
    create_button.place(x=600, y=460, width=200)
    admin_signup_button.place(x=600, y=500, width=200)
    su_label.place(x=0, y=0, relwidth=1, relheight=1)
    run_button.pack(row=4, column=0)
    signup_window.mainloop()


def login():
    username = username_entry.get()
    password = password_entry.get()

    mycursor.execute("SELECT * FROM logindatabase WHERE username = %s AND password = %s", (username, password))
    existing_account = mycursor.fetchone()

    mycursor.execute("SELECT account_type FROM logindatabase WHERE username = %s AND password = %s", (username, password))
    account_type = mycursor.fetchall()

    mycursor.execute("SELECT email FROM logindatabase WHERE username = %s AND password = %s", (username, password))
    email = mycursor.fetchone()

    if existing_account:
        if account_type:
            account_type = account_type[0][0]
            if account_type == 'student':
                verifycredstu(username, password, email, handle_verification_result)
            elif account_type == 'admin':
                verifycredadm(username, password, email,  handle_verification_result)
            else:
                messagebox.showinfo("HAHAHAHA", "You messed up bro")
        else:
            messagebox.showinfo("Notice", "No account type found for this user")
    else:
        messagebox.showinfo("Notice", "Account does not have a match in the database!")


root = tk.Tk()
root.title('LogIn Screen')
root.geometry("1366x768")

ui_font = font.Font(family="PressStart2P-Regular", size=12)
ui_font.actual()

photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\loginscreen.png'

image = Image.open(photoimg)
image = image.resize((1366, 768), Image.BILINEAR)
tk_image = ImageTk.PhotoImage(image)
label = tk.Label(root, image=tk_image)

result_label = tk.Label(root, text="" ,bg='#ADD8E6', fg='#FFFFFF', font=ui_font)

username_entry = tk.Entry(root ,bg='#FFFFFF', fg="#000000", font=ui_font)
password_entry = tk.Entry(root, show="*" ,bg='#FFFFFF', fg="#000000", font=ui_font)
login_button = tk.Button(root, text="Login", command=login ,bg='#FFFFFF', fg="#000000", font=ui_font)
new_account_button = tk.Button(root, text="Sign Up", command=new_credentialstu ,bg='#FFFFFF', fg="#000000", font=ui_font)

username_entry.place(x=940, y=230, width=200)
password_entry.place(x=940, y=290, width=200)
login_button.place(x=950, y=330)
new_account_button.place(x=1030, y=330)

label.place(x=0, y=0, relwidth=1, relheight=1)

root.mainloop()

'''
TTD:
    email verification for both student and admins -- (done) changed into pre-declared provided usernames for both admin and students
    admin privilege verification -- done
    randomized qr code sent via email when logging in - done
    dashboard functionalities (last)
    bug fixing
'''