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

adm_db_window = tk.Tk()
adm_db_window.title("PLM Admin Dashboard")
adm_db_window.geometry('1366x768')

db_photoimg = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\dashboard.png'

tk_dashboard_image = Image.open(db_photoimg)
tk_dashboard_image = tk_dashboard_image.resize((1366, 768))
tk_dashboard_image = ImageTk.PhotoImage(tk_dashboard_image)
db_label = tk.Label(adm_db_window, image=tk_dashboard_image)

popup_image = r'C:\Users\MuringFamily\PycharmProjects\pythonProject\window_popup.png'
popup_img = Image.open(popup_image)
popup_img = ImageTk.PhotoImage(popup_img)

def notifications():
    messagebox.showinfo("Notice", "Notifications can be found here.")
    notif_window = tk.Frame()
#    notif_window.title("Notification")
#    notif_window.geometry('708x714')

    notif_label = tk.Label(notif_window, image=popup_img)
    notif_label.place(x=0, y=0, relheight=1, relwidth=1)

def profile():
    messagebox.showinfo("Notice", "Profile can be found here.")
    profile_window = tk.Frame()
#    profile_window.title("Profile")
#    profile_window.geometry('708x714')

    profile_label = tk.Label(profile_window, image=popup_img)
    profile_label.place(x=0, y=0, relheight=1, relwidth=1)

def account_settings():
    messagebox.showinfo("Notice", "Settings can be found here.")
    accset_window = tk.Frame()
#    accset_window.title("Account Settings")
#    accset_window.geometry('708x714')

    accset_label = tk.Label(accset_window, image=popup_img)
    accset_label.place(x=0, y=0, relheight=1, relwidth=1)

def admin_settings():
    messagebox.showinfo("Notice", "Admin settings can be found here.")
    admin_window = tk.Frame()
#    admin_window.title("Admin Settings")
#    admin_window.geometry('708x714')

    add_entry = tk.Entry(admin_window, width=30)
    add_button = tk.Button(admin_window, text="Enter")
    delete_entry = tk.Entry(admin_window, width=30)
    delete_button = tk.Button(admin_window, text="Enter")
    admin_label = tk.Label(admin_window, image=popup_img)

    add_entry.place(x=580, y=380)
    add_button.place(x=580, y=400)
    delete_entry.place(x=600, y=420)
    delete_button.place(x=600, y=440)
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

db_label.place(x=0, y=0, relwidth=1, relheight=1)
adm_db_window.mainloop()
