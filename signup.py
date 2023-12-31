import customtkinter as ctk
from screeninfo import get_monitors
import re
import mysql.connector
from datetime import datetime
import ttkbootstrap as ttk
import subprocess

def open_new_file():
    root.destroy()
    subprocess.run(["python", "login.py"]) 
    
def add_user():
    username = userEntry.get()
    email = emailEntry.get()
    age = ageEntry.get()
    contact = contactEntry.get()
    passwd = passEntry.get()

    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pranavmysql",
    database="newuserdb"
)

    mycursor = db.cursor()
    mycursor.execute("INSERT INTO newuser (name, email, password, age, contact, created) VALUES (%s, %s, %s,%s,%s, %s)", (username, email, passwd, age, contact, datetime.now()))
    db.commit()


root = ctk.CTk()
resoultion = get_monitors()[0]
screenWidth = resoultion.width
screenHeight = resoultion.height




# Setting appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Create Account")

# Empty space to center content horizontally
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)  # Make the second row taller
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

logIn = ctk.CTkLabel(root, text="CREATE YOUR ACCOUNT", font=('Poppins Medium', 50))
logIn.grid(row=1, column=1, pady=50)

# Creating login frame with more height
SignupFrame = ctk.CTkFrame(master=root, corner_radius=8, border_width=1, border_color="black", fg_color="white")
SignupFrame.grid(row=2, column=1, pady=(20, 30))  

# Creating userentry and passentry for username and password
userEntry = ctk.CTkEntry(master=SignupFrame, placeholder_text="username", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
userEntry.grid(row=0, column=0, pady=(30,15), padx=10)


def is_valid_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email)



emailEntry = ctk.CTkEntry(master=SignupFrame, placeholder_text="email", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
emailEntry.grid(row=1, column=0, pady=(10,15), padx=10)

passEntry = ctk.CTkEntry(master=SignupFrame, placeholder_text="password", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2,  show="*")
passEntry.grid(row=2, column=0, pady=(10,15), padx=10)



def validate_signupForm():
    username = userEntry.get()
    email = emailEntry.get()
    age = ageEntry.get()
    contact = contactEntry.get()

    if not username:
        error_label.configure(text="Please enter a username", text_color="red", font=('inter', 18))
        error_label.grid(row=6, column=0, columnspan=2, pady=(0, 30))
    elif not is_valid_email(email):
        error_label.configure(text="Invalid email format", text_color="red", font=('inter', 18))
        error_label.grid(row=6, column=0, columnspan=2, pady=(0, 30))
    elif not age.isdigit() or int(age) >= 100:
        error_label.configure(text="Enter a valid age (must be a number and less than 100)", text_color="red", font=('inter', 18))
        error_label.grid(row=6, column=0, columnspan=2, pady=(0, 30))
    elif not (contact.isdigit() and len(contact) == 10):
        error_label.configure(text="Contact number must be a number (must be a 10-digit-no)", text_color="red", font=('inter', 18))
        error_label.grid(row=6, column=0, columnspan=2, pady=(0, 30))
    else:
        # All fields are valid, clear the error message and proceed with signup
        error_label.configure(text="")
        error_label.grid_forget()
        add_user()
        open_new_file()




ageEntry = ctk.CTkEntry(master=SignupFrame, placeholder_text="age", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
ageEntry.grid(row=3, column=0, pady=(10,15), padx=10)

contactEntry = ctk.CTkEntry(master=SignupFrame, placeholder_text="Contact No.", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
contactEntry.grid(row=4, column=0, pady=(10,15), padx=10)

# login button
button = ctk.CTkButton(master=SignupFrame, text='Sign Up', font=('inter', 23), fg_color="#5790DF", command=validate_signupForm)
button.grid(row=5, column=0, pady=20, padx=200)


# Forget password and create a new account
createAccount = ctk.CTkLabel(master=SignupFrame, text="Already have an account, Login Here", font=('Inter', 20))
createAccount.grid(row=7, column=0, pady=(0, 20), padx=10)

# Error Label
error_label = ctk.CTkLabel(SignupFrame, text="", text_color="red",  font=('Inter', 15))
error_label.grid(row=8, column=0, columnspan=1, pady=(0, 0))  

root.mainloop()