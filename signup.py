import customtkinter as ctk

root = ctk.CTk()

# Setting appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root.geometry("1366x768")
root.title("Log In")

# Empty space to center content horizontally
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

logIn = ctk.CTkLabel(root, text="CREATE YOUR ACCOUNT", font=('Poppins Medium', 50))
logIn.grid(row=1, column=1, pady=50)

# Creating login frame
SingupFrame = ctk.CTkFrame(master=root, corner_radius=8, border_width=1, border_color="black", fg_color="white")
SingupFrame.grid(row=2, column=1, pady=20)

# Creating userentry and passentry for username and password
userEntry = ctk.CTkEntry(master=SingupFrame, placeholder_text="username", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
userEntry.grid(row=0, column=0, pady=20, padx=10)

emailEntry = ctk.CTkEntry(master=SingupFrame, placeholder_text="email", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
emailEntry.grid(row=1, column=0, pady=20, padx=10)

def validate_numeric_ageInput():
    input_text = ageEntry.get()
    if not input_text.isdigit():
        error_popup = ctk.CTkToplevel(SingupFrame)
        error_popup.geometry("200x200")
        error_popup.title("Error")
        error_label = ctk.CTkLabel(error_popup, text="Only numbers are allowed", text_color="red")
        error_label.grid(row=0, column=0, padx=20, pady=50)
    elif int(input_text) >= 100:
        error_popup = ctk.CTkToplevel(SingupFrame)
        error_popup.geometry("200x200")
        error_popup.title("Error")
        error_label = ctk.CTkLabel(error_popup, text="Enter Valid Age", text_color="red")
        error_label.grid(row=0, column=0, padx=20, pady=20)
    else:
        error_label.configure(text="")

ageEntry = ctk.CTkEntry(master=SingupFrame, placeholder_text="age", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
ageEntry.grid(row=2, column=0, pady=20, padx=10)

contactEntry = ctk.CTkEntry(master=SingupFrame, placeholder_text="Contact No.", width=400, font=('calibri', 25), corner_radius=10, border_color="grey", fg_color="white", border_width=2)
contactEntry.grid(row=3, column=0, pady=20, padx=10)

# login button
button = ctk.CTkButton(master=SingupFrame, text='Sign Up', font=('inter', 23), fg_color="grey", command=validate_numeric_ageInput)
button.grid(row=4, column=0, pady=20, padx=200)

# Forget password and create a new account
createAccount = ctk.CTkLabel(master=SingupFrame, text="Already have an account, Login Here", font=('Inter', 20))
createAccount.grid(row=5, column=0, pady=30, padx=10)

root.mainloop()
