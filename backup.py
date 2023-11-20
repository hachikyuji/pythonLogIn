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
import re

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


def dashboard_pres():
    global root
    root.withdraw()

    adm_db_window = tk.Toplevel(root)
    adm_db_window.title("PLM Admin Dashboard")
    adm_db_window.geometry('1366x768')

    db_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\dashboard.png'

    tk_dashboard_image = Image.open(db_photoimg)
    tk_dashboard_image = tk_dashboard_image.resize((1366, 768))
    tk_dashboard_image = ImageTk.PhotoImage(tk_dashboard_image)
    db_label = tk.Label(adm_db_window, image=tk_dashboard_image)

    def notifications():
        messagebox.showinfo("Notice", "Notifications can be found here.")
        notif_window = tk.Toplevel()
        notif_window.title("Notification")
        notif_window.geometry('1366x768')

        notif_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\notif.png'

        tk_db_image = Image.open(notif_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        notif_label = tk.Label(notif_window, image=tk_db_image)

        notif_label.place(x=0, y=0, relheight=1, relwidth=1)
        notif_window.mainloop()

    def profile():
        messagebox.showinfo("Notice", "Profile can be found here.")
        profile_window = tk.Toplevel()
        profile_window.title("Profile")
        profile_window.geometry('1366x768')

        profile_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\profile.png'

        tk_db_image = Image.open(profile_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        profile_label = tk.Label(profile_window, image=tk_db_image)

        profile_label.place(x=0, y=0)
        profile_window.mainloop()

    def account_settings():
        messagebox.showinfo("Notice", "Settings can be found here.")
        accset_window = tk.Toplevel()
        accset_window.title("Account Settings")
        accset_window.geometry('1366x768')

        accset_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\accset.png'

        tk_db_image = Image.open(accset_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        accset_label = tk.Label(accset_window, image=tk_db_image)

        def change_username():
            accset_current_username = acc_entry.get()
            new_username = acc_new_entry.get()
            accset_confirm_password = acc_password.get()
            mycursor.execute("SELECT username FROM logindatabase WHERE username = %s AND password = %s",
                             (accset_current_username, accset_confirm_password))
            current_password = mycursor.fetchone()

            if current_password:
                mycursor.execute("UPDATE logindatabase SET username = %s WHERE username = %s",
                                 (new_username, accset_current_username))
                db.commit()
            else:
                messagebox.showinfo("Notice", "Credentials does not have a match.")

        acc_entry = tk.Entry(accset_window, width=40)
        acc_new_entry = tk.Entry(accset_window, width=40)
        acc_password = tk.Entry(accset_window, width=40)
        acc_button = tk.Button(accset_window, text="Confirm", bg="white", command=change_username)

        acc_entry.place(x=820, y=350)
        acc_new_entry.place(x=825, y=400)
        acc_password.place(x=825, y=450)
        acc_button.place(x=895, y=480)
        accset_label.place(x=0, y=0)
        accset_window.mainloop()


    def admin_settings():
        messagebox.showinfo("Notice", "Admin settings can be found here.")
        admin_window = tk.Toplevel()
        admin_window.title("Admin Settings")
        admin_window.geometry('1366x768')

        admin_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\admin.png'

        tk_db_image = Image.open(admin_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        admin_label = tk.Label(admin_window, image=tk_db_image)

        def add_account():
            new_username = add_entry.get()
            query = "INSERT INTO logindatabase (username, account_type) VALUES (%s, 'student')"
            data = (new_username,)
            mycursor.execute(query, data)
            db.commit()
            messagebox.showinfo("Notice",f"Account {new_username} has been added to the database.")

        def delete_account():
            current_username = delete_entry.get()

            mycursor.execute("SELECT account_type FROM logindatabase WHERE username = %s", (current_username,))
            account_type = mycursor.fetchone()

            if current_username:
                current_type = account_type[0]
                if current_type == 'student':
                    messagebox.showinfo("Notice", f"Account {current_username} has been deleted in the database")
                    query = "DELETE FROM logindatabase WHERE username = %s"
                    data = (current_username,)
                    mycursor.execute(query, data)
                    db.commit()
                elif current_type == 'admin':
                    messagebox.showinfo("Notice", "You do not have the authorization to delete an admin.")
                elif current_type == 'president':
                    messagebox.showinfo("Notice", "You do not have the authorization to delete the president.")
                else:
                    messagebox.showinfo("Notice", "No account type found in for this username.")
            else:
                messagebox.showinfo("Notice", "Username does not have a match in the database.")

        add_entry = tk.Entry(admin_window, width=30)
        add_button = tk.Button(admin_window, text="Enter", command=add_account)
        delete_entry = tk.Entry(admin_window, width=30)
        delete_button = tk.Button(admin_window, text="Enter", command=delete_account)

        add_entry.place(x=775, y=335)
        add_button.place(x=850, y=365)
        delete_entry.place(x=775, y=490)
        delete_button.place(x=850, y=520)
        admin_label.place(x=0, y=0, relheight=1, relwidth=1)
        admin_window.mainloop()

    def president_settings():
        messagebox.showinfo("Notice", "Admin settings can be found here.")
        admin_window = tk.Toplevel()
        admin_window.title("Admin Settings")
        admin_window.geometry('1366x768')

        admin_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\president.png'

        tk_db_image = Image.open(admin_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        admin_label = tk.Label(admin_window, image=tk_db_image)

        def add_account():
            new_username = pres_add_entry.get()
            query = "INSERT INTO logindatabase (username, account_type) VALUES (%s, 'admin')"
            data = (new_username,)
            mycursor.execute(query, data)
            db.commit()
            messagebox.showinfo("Notice", f"Account {new_username} has been added to the database.")

        def delete_account():
            current_username = pres_delete_entry.get()

            if current_username:
                messagebox.showinfo("Notice", f"Account {current_username} has been deleted in the database")
                query = "DELETE FROM logindatabase WHERE username = %s"
                data = (current_username,)
                mycursor.execute(query, data)
                db.commit()
            else:
                messagebox.showinfo("Notice", "Username does not have a match in the database.")

        pres_add_entry = tk.Entry(admin_window, width=30)
        add_button = tk.Button(admin_window, text="Enter", command=add_account)
        pres_delete_entry = tk.Entry(admin_window, width=30)
        delete_button = tk.Button(admin_window, text="Enter", command=delete_account)

        pres_add_entry.place(x=775, y=335)
        add_button.place(x=850, y=365)
        pres_delete_entry.place(x=775, y=490)
        delete_button.place(x=850, y=520)
        admin_label.place(x=0, y=0, relheight=1, relwidth=1)
        admin_window.mainloop()

    sections_frame = tk.Frame(adm_db_window, bg="white", height=1, bd=0)
    sections_frame.pack(side="left", padx=10, pady=10)

    header_label = tk.Label(sections_frame, text="PLM Dashboard", font=("Helvetica", 16), bg="white")
    header_label.pack(pady=10)

    separator1 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator1.pack(fill="x")

    section1_label = tk.Label(sections_frame, text="Notifications", font=("Helvetica", 14), bg="white")
    section1_label.pack(pady=10)

    button1 = tk.Button(sections_frame, text="View", bg="white", command=notifications)
    button1.pack()

    separator2 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator2.pack(fill="x")

    section2_label = tk.Label(sections_frame, text="Profile", font=("Helvetica", 14), bg="white")
    section2_label.pack(pady=10)

    button2 = tk.Button(sections_frame, text="View", bg="white", command=profile)
    button2.pack()

    separator3 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator3.pack(fill="x")

    section3_label = tk.Label(sections_frame, text="Account Settings", font=("Helvetica", 14), bg="white")
    section3_label.pack(pady=10)

    button3 = tk.Button(sections_frame, text="View", bg="white", command=account_settings)
    button3.pack()

    separator4 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator4.pack(fill="x")

    section4_label = tk.Label(sections_frame, text="Admin Settings", font=("Helvetica", 14), bg="white")
    section4_label.pack(pady=10)

    button4 = tk.Button(sections_frame, text="View", bg="white", command=admin_settings)
    button4.pack()

    separator5 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator5.pack(fill="x")

    section5_label = tk.Label(sections_frame, text="President Settings", font=("Helvetica", 14), bg="white")
    section5_label.pack(pady=10)

    button5 = tk.Button(sections_frame, text="View", bg="white", command=president_settings)
    button5.pack()

    db_label.place(x=0, y=0)
    adm_db_window.mainloop()

def dashboardadm():
    global root
    root.withdraw()

    adm_db_window = tk.Toplevel(root)
    adm_db_window.title("PLM Admin Dashboard: Dean")
    adm_db_window.geometry('1366x768')

    db_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\dashboard.png'

    tk_dashboard_image = Image.open(db_photoimg)
    tk_dashboard_image = tk_dashboard_image.resize((1366, 768))
    tk_dashboard_image = ImageTk.PhotoImage(tk_dashboard_image)
    db_label = tk.Label(adm_db_window, image=tk_dashboard_image)

    def notifications():
        messagebox.showinfo("Notice", "Notifications can be found here.")
        notif_window = tk.Toplevel()
        notif_window.title("Notification")
        notif_window.geometry('1366x768')

        notif_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\notif.png'

        tk_db_image = Image.open(notif_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        notif_label = tk.Label(notif_window, image=tk_db_image)

        notif_label.place(x=0, y=0, relheight=1, relwidth=1)
        notif_window.mainloop()

    def profile():
        messagebox.showinfo("Notice", "Profile can be found here.")
        profile_window = tk.Toplevel()
        profile_window.title("Profile")
        profile_window.geometry('1366x768')

        profile_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\profile.png'

        tk_db_image = Image.open(profile_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        profile_label = tk.Label(profile_window, image=tk_db_image)

        profile_label.place(x=0, y=0)
        profile_window.mainloop()

    def account_settings():
        messagebox.showinfo("Notice", "Settings can be found here.")
        accset_window = tk.Toplevel()
        accset_window.title("Account Settings")
        accset_window.geometry('1366x768')

        accset_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\accset.png'

        tk_db_image = Image.open(accset_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        accset_label = tk.Label(accset_window, image=tk_db_image)

        def change_username():
            accset_current_username = acc_entry.get()
            new_username = acc_new_entry.get()
            accset_confirm_password = acc_password.get()
            mycursor.execute("SELECT username FROM logindatabase WHERE username = %s AND password = %s",
                             (accset_current_username, accset_confirm_password))
            current_password = mycursor.fetchone()

            if current_password:
                mycursor.execute("UPDATE logindatabase SET username = %s WHERE username = %s",
                                 (new_username, accset_current_username))
                db.commit()
            else:
                messagebox.showinfo("Notice", "Credentials does not have a match.")

        acc_entry = tk.Entry(accset_window, width=40)
        acc_new_entry = tk.Entry(accset_window, width=40)
        acc_password = tk.Entry(accset_window, width=40)
        acc_button = tk.Button(accset_window, text="Confirm", bg="white", command=change_username)

        acc_entry.place(x=820, y=350)
        acc_new_entry.place(x=825, y=400)
        acc_password.place(x=825, y=450)
        acc_button.place(x=905, y=480)
        accset_label.place(x=0, y=0)
        accset_window.mainloop()


    def admin_settings():
        messagebox.showinfo("Notice", "Admin settings can be found here.")
        admin_window = tk.Toplevel()
        admin_window.title("Admin Settings")
        admin_window.geometry('1366x768')

        admin_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\admin.png'

        tk_db_image = Image.open(admin_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        admin_label = tk.Label(admin_window, image=tk_db_image)

        def add_account():
            new_username = add_entry.get()
            query = "INSERT INTO logindatabase (username, account_type) VALUES (%s, 'student')"
            data = (new_username,)
            mycursor.execute(query, data)
            db.commit()
            messagebox.showinfo("Notice",f"Account {new_username} has been added to the database.")

        def delete_account():
            current_username = delete_entry.get()

            mycursor.execute("SELECT account_type FROM logindatabase WHERE username = %s", (current_username,))
            account_type = mycursor.fetchone()

            if current_username:
                current_type = account_type[0]
                if current_type == 'student':
                    messagebox.showinfo("Notice", f"Account {current_username} has been deleted in the database")
                    query = "DELETE FROM logindatabase WHERE username = %s"
                    data = (current_username,)
                    mycursor.execute(query, data)
                    db.commit()
                elif current_type == 'admin':
                    messagebox.showinfo("Notice", "You do not have the authorization to delete an admin.")
                else:
                    messagebox.showinfo("Notice", f"No account type found in for this username. is it getting the account type {current_type}")
            else:
                messagebox.showinfo("Notice", "Username does not have a match in the database.")

        add_entry = tk.Entry(admin_window, width=30)
        add_button = tk.Button(admin_window, text="Enter", command=add_account)
        delete_entry = tk.Entry(admin_window, width=30)
        delete_button = tk.Button(admin_window, text="Enter", command=delete_account)

        add_entry.place(x=775, y=335)
        add_button.place(x=850, y=365)
        delete_entry.place(x=775, y=490)
        delete_button.place(x=850, y=520)
        admin_label.place(x=0, y=0, relheight=1, relwidth=1)
        admin_window.mainloop()

    sections_frame = tk.Frame(adm_db_window, bg="white", height=1, bd=0)
    sections_frame.pack(side="left", padx=10, pady=10)

    header_label = tk.Label(sections_frame, text="PLM Dashboard", font=("Helvetica", 16), bg="white")
    header_label.pack(pady=10)

    separator1 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator1.pack(fill="x")

    section1_label = tk.Label(sections_frame, text="Notifications", font=("Helvetica", 14), bg="white")
    section1_label.pack(pady=10)

    button1 = tk.Button(sections_frame, text="View", bg="white", command=notifications)
    button1.pack()

    separator2 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator2.pack(fill="x")

    section2_label = tk.Label(sections_frame, text="Profile", font=("Helvetica", 14), bg="white")
    section2_label.pack(pady=10)

    button2 = tk.Button(sections_frame, text="View", bg="white", command=profile)
    button2.pack()

    separator3 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator3.pack(fill="x")

    section3_label = tk.Label(sections_frame, text="Account Settings", font=("Helvetica", 14), bg="white")
    section3_label.pack(pady=10)

    button3 = tk.Button(sections_frame, text="View", bg="white", command=account_settings)
    button3.pack()

    separator4 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator4.pack(fill="x")

    section4_label = tk.Label(sections_frame, text="Admin Settings", font=("Helvetica", 14), bg="white")
    section4_label.pack(pady=10)

    button4 = tk.Button(sections_frame, text="View", bg="white", command=admin_settings)
    button4.pack()

    db_label.place(x=0, y=0)
    adm_db_window.mainloop()


def dashboardstu():
    global root
    root.withdraw()

    stu_db_window = tk.Toplevel(root)
    stu_db_window.title("PLM Student Dashboard Dashboard")
    stu_db_window.geometry('1366x768')

    db_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\dashboard.png'

    tk_dashboard_image = Image.open(db_photoimg)
    tk_dashboard_image = tk_dashboard_image.resize((1366, 768))
    tk_dashboard_image = ImageTk.PhotoImage(tk_dashboard_image)
    db_label = tk.Label(stu_db_window, image=tk_dashboard_image)

    def notifications():
        messagebox.showinfo("Notice", "Notifications can be found here.")
        notif_window = tk.Toplevel()
        notif_window.title("Notification")
        notif_window.geometry('1366x768')

        notif_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\notif.png'

        tk_db_image = Image.open(notif_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        notif_label = tk.Label(notif_window, image=tk_db_image)

        notif_label.place(x=0, y=0, relheight=1, relwidth=1)
        notif_window.mainloop()

    def profile():
        messagebox.showinfo("Notice", "Profile can be found here.")
        profile_window = tk.Toplevel()
        profile_window.title("Profile")
        profile_window.geometry('1366x768')

        profile_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\profile.png'

        tk_db_image = Image.open(profile_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        profile_label = tk.Label(profile_window, image=tk_db_image)

        profile_label.place(x=0, y=0)
        profile_window.mainloop()

    def account_settings():
        messagebox.showinfo("Notice", "Settings can be found here.")
        accset_window = tk.Toplevel()
        accset_window.title("Account Settings")
        accset_window.geometry('1366x768')

        accset_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\accset.png'

        tk_db_image = Image.open(accset_photoimg)
        tk_db_image = tk_db_image.resize((1366, 768))
        tk_db_image = ImageTk.PhotoImage(tk_db_image)
        accset_label = tk.Label(accset_window, image=tk_db_image)

        def change_username():
            accset_current_username = acc_entry.get()
            new_username = acc_new_entry.get()
            accset_confirm_password = acc_password.get()
            mycursor.execute("SELECT username FROM logindatabase WHERE username = %s AND password = %s", (accset_current_username, accset_confirm_password))
            current_password = mycursor.fetchone()

            if current_password:
                mycursor.execute("UPDATE logindatabase SET username = %s WHERE username = %s", (new_username, accset_current_username))
                db.commit()
            else:
                messagebox.showinfo("Notice", "Credentials does not have a match.")

        acc_entry = tk.Entry(accset_window, width=40)
        acc_new_entry = tk.Entry(accset_window, width=40)
        acc_password = tk.Entry(accset_window, width=40)
        acc_button = tk.Button(accset_window, text="Confirm", bg="white", command=change_username)

        acc_entry.place(x=820, y=350)
        acc_new_entry.place(x=825, y=400)
        acc_password.place(x=825, y=450)
        acc_button.place(x=895, y=480)
        accset_label.place(x=0, y=0)
        accset_window.mainloop()

    sections_frame = tk.Frame(stu_db_window, bg="white", height=1, bd=0)
    sections_frame.pack(side="left", padx=10, pady=10)

    header_label = tk.Label(sections_frame, text="PLM Dashboard", font=("Helvetica", 16), bg="white")
    header_label.pack(pady=10)

    separator1 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator1.pack(fill="x")

    section1_label = tk.Label(sections_frame, text="Notifications", font=("Helvetica", 14), bg="white")
    section1_label.pack(pady=10)

    button1 = tk.Button(sections_frame, text="View", bg="white", command=notifications)
    button1.pack()

    separator2 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator2.pack(fill="x")

    section2_label = tk.Label(sections_frame, text="Profile", font=("Helvetica", 14), bg="white")
    section2_label.pack(pady=10)

    button2 = tk.Button(sections_frame, text="View", bg="white", command=profile)
    button2.pack()

    separator3 = ttk.Separator(sections_frame, orient="horizontal", style="TSeparator")
    separator3.pack(fill="x")

    section3_label = tk.Label(sections_frame, text="Account Settings", font=("Helvetica", 14), bg="white")
    section3_label.pack(pady=10)

    button3 = tk.Button(sections_frame, text="View", bg="white", command=account_settings)
    button3.pack()

    db_label.place(x=0, y=0)
    stu_db_window.mainloop()


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
        if verify_qr:
            verifycredadm_window.destroy()
            dashboardadm()
        else:
            messagebox.showinfo("Notice", "Please input the correct OTP from your email.")

    global verifycredadm_window

    verifycredadm_window = Toplevel(root)
    verifycredadm_window.title("QR Code Verification")
    verifycredadm_window.geometry("1366x768")

    verstu_image = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\qrcodescreenadm.png'

    verstu_img = Image.open(verstu_image)
    verstu_img = verstu_img.resize((1366, 768))
    verstu_img = ImageTk.PhotoImage(verstu_img)

    verstu_label = tk.Label(verifycredadm_window, image=verstu_img)
    verstu_label.image = verstu_img

    userinput_enter = tk.Entry(verifycredadm_window, show="*", width=40)
    create_but = tk.Button(verifycredadm_window, text="Enter", command=verifyqr)

    userinput_enter.place(x=555, y=400)
    create_but.place(x=660, y=430)
    verstu_label.place(x=0, y=0, relheight=1, relwidth=1)
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
        if verify_qr:
            verifycredstu_window.destroy()
            dashboardstu()
        else:
            messagebox.showinfo("Notice", "Please input the correct OTP from your email.")

    global verifycredstu_window

    verifycredstu_window = Toplevel(root)
    verifycredstu_window.title("QR Code Verification")
    verifycredstu_window.geometry("1366x768")

    verstu_image = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\qrcodescreenstu.png'

    verstu_img = Image.open(verstu_image)
    verstu_img = verstu_img.resize((1366, 768))
    verstu_img = ImageTk.PhotoImage(verstu_img)

    verstu_label = tk.Label(verifycredstu_window, image=verstu_img)
    verstu_label.image = verstu_img

    userinput_enter = tk.Entry(verifycredstu_window, show="*", width=40)
    create_but = tk.Button(verifycredstu_window, text="Enter", command=verifyqr)

    userinput_enter.place(x=555, y=400)
    create_but.place(x=660, y=430)
    verstu_label.place(x=0, y=0, relheight=1, relwidth=1)
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
            uppercase_pattern = r'[A-Z]'
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.search(uppercase_pattern, password) and re.match(email_pattern, email):
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
                messagebox.showinfo("Notice", "Account successfully created!")
                admsignup_window.destroy()
            else:
                messagebox.showinfo("Notice", "Please input the credentials based on the given restrictions.")
                admsignup_window.destroy()
        else:
            messagebox.showinfo("Notiice", "Contact an administrator for a properly issued username before proceeding.")
            admsignup_window.destroy()

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
    tk_signup_image = tk_signup_image.resize((1366, 768))
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
            uppercase_pattern = r'[A-Z]'
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.search(uppercase_pattern, password) and re.match(email_pattern, email):
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
                messagebox.showinfo("Notice", "Account successfully created!")
                signup_window.destroy()
            else:
                messagebox.showinfo("Notice", "Please input the credentials based on the given restrictions.")
                signup_window.destroy()
        else:
            messagebox.showinfo("Notiice", "Contact an administrator for a properly issued username before proceeding.")
            signup_window.destroy()

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

    mycursor.execute("SELECT account_type FROM logindatabase WHERE username = %s AND password = %s",
                     (username, password))
    account_type = mycursor.fetchall()

    mycursor.execute("SELECT email FROM logindatabase WHERE username = %s AND password = %s", (username, password))
    email = mycursor.fetchone()

    if existing_account:
        if account_type:
            account_type = account_type[0][0]
            if account_type == 'student':
                verifycredstu(username, password, email, handle_verification_result)
            elif account_type == 'admin':
                verifycredadm(username, password, email, handle_verification_result)
            elif account_type == 'president':
                dashboard_pres()
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

result_label = tk.Label(root, text="", bg='#ADD8E6', fg='#FFFFFF', font=ui_font)

username_entry = tk.Entry(root, bg='#FFFFFF', fg="#000000", font=ui_font)
password_entry = tk.Entry(root, show="*", bg='#FFFFFF', fg="#000000", font=ui_font)
login_button = tk.Button(root, text="Login", command=login, bg='#FFFFFF', fg="#000000", font=ui_font)
new_account_button = tk.Button(root, text="Sign Up", command=new_credentialstu, bg='#FFFFFF', fg="#000000",
                               font=ui_font)

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
    dashboard functionalities -- done?
    user credential restrictions -- done
    president account insertion -- done
'''