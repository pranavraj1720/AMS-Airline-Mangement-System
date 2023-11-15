import customtkinter as ctk
from screeninfo import get_monitors
import re


root = ctk.CTk()
# Setting appearance mode and color theme 
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue") 

resoultion = get_monitors()[0]
screenWidth = resoultion.width
screenHeight = resoultion.height


root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Log In")


logIn = ctk.CTkLabel(root, text="LOGIN", font=('Poppins Medium', 50))
logIn.pack(pady=50, padx=20)


# Creating login frame 
loginFrame = ctk.CTkFrame(master=root, corner_radius=8, border_width=1, border_color="black", fg_color="white")
loginFrame.pack(pady=20)


def validateLogIn():
    username = userEntry.get()
    password = passEntry.get()
    if not username:
        error_label.configure(text="Please enter a username", text_color="red", font=('inter', 23))
        error_label.pack(pady = (20, 0))
    elif not password:
        error_label.configure(text="Please enter a password", text_color="red", font=('inter', 23))
        error_label.pack(pady = (20, 0))
    else:
        error_label.configure(text="")
        error_label.grid_forget()
        

# Creating userentry and passentry for username and password
userEntry = ctk.CTkEntry(master=loginFrame ,placeholder_text="username", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
userEntry.pack(pady=28, padx=10)

passEntry = ctk.CTkEntry(master=loginFrame, placeholder_text="password", show="*", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
passEntry.pack(pady=0, padx=10)



error_label = ctk.CTkLabel(loginFrame, text="")
error_label.pack()

# login button
button = ctk.CTkButton(master=loginFrame, 
                       text='Login', font=('inter', 25), fg_color="grey", command=validateLogIn) 
button.pack(pady=20,padx=200) 
  
#  Forget password and create new account
forgetPass = ctk.CTkLabel(master=loginFrame, text="Forget Password", font=('Inter', 20))
forgetPass.pack()

createAccount = ctk.CTkLabel(master=loginFrame, 
                           text="Don't have an account? Create One", font=('Inter', 20)) 
createAccount.pack(pady=30,padx=10)
root.mainloop()
