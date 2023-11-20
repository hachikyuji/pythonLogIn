import tkinter as tk
from tkinter import ttk

def switch_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.geometry('400x300')
root.title('School Dashboard')

# Create a container frame to hold all the pages
container = ttk.Frame(root)
container.pack(fill='both', expand=True)

# Create the Home page
home_frame = ttk.Frame(container)
ttk.Label(home_frame, text='Welcome to Home Page').pack()
ttk.Button(home_frame, text='Profile', command=lambda: switch_frame(profile_frame)).pack()
ttk.Button(home_frame, text='Account Settings', command=lambda: switch_frame(account_settings_frame)).pack()

# Create the Profile page
profile_frame = ttk.Frame(container)
ttk.Label(profile_frame, text='User Profile').pack()
ttk.Button(profile_frame, text='Home', command=lambda: switch_frame(home_frame)).pack()
ttk.Button(profile_frame, text='Account Settings', command=lambda: switch_frame(account_settings_frame)).pack()

# Create the Account Settings page
account_settings_frame = ttk.Frame(container)
ttk.Label(account_settings_frame, text='Account Settings').pack()
ttk.Button(account_settings_frame, text='Home', command=lambda: switch_frame(home_frame)).pack()
ttk.Button(account_settings_frame, text='Profile', command=lambda: switch_frame(profile_frame)).pack()

# Pack all frames into the container
for frame in (home_frame, profile_frame, account_settings_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Show the Home page initially
switch_frame(home_frame)

root.mainloop()
