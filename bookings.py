from cgitb import text
import customtkinter as ctk
from mysqlx import Column
from screeninfo import get_monitors
import ttkbootstrap as ttk

root = ctk.CTk()
# Setting appearance mode and color theme 
ctk.set_appearance_mode("black")
ctk.set_default_color_theme("blue") 

resoultion = get_monitors()[0]
screenWidth = resoultion.width
screenHeight = resoultion.height


root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Bookings")

bookings = ctk.CTkFrame(master=root, fg_color="white", border_color="#fff", border_width=2, corner_radius=10)
bookings.grid(row=1, column=1, sticky="nsew", padx=(15, 15), pady=20)

PassengerNo = ctk.CTkLabel(bookings, text="No. of Passenger", font=('Poppins Medium', 20), fg_color="transparent", text_color="#000")
PassengerNo.grid(row=2, column=0, pady=(20, 20), padx=20, sticky="w")

# Dropdown Menu
cityMenu_var = ctk.StringVar(value="No. of Passenger:")
cityMenu = ctk.CTkOptionMenu(bookings, values=["1", "2", "3", "4", "5"], variable=cityMenu_var, font=('Inter', 18), width=30, height=30, fg_color="#5790DF", button_color="#5790DF", )
cityMenu.grid(row=2, column=0, padx=(200,0), sticky="w")
cityMenu.set("0")

passengerName = ctk.CTkEntry(master=bookings ,placeholder_text="Name of Passenger", width=450, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
passengerName.grid(row=4, column=0, sticky="w", padx=(20,0))

passengerGender = ctk.CTkEntry(master=bookings ,placeholder_text="Gender", width=200, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
passengerGender.grid(row=5, column=0, sticky="w", padx=(20,0), pady=(20,0))

passengerAge = ctk.CTkEntry(master=bookings ,placeholder_text="Age", width=150, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
passengerAge.grid(row=5, column=0, sticky="w", padx=(250,0), pady=(20,0))

passengerMobileNo = ctk.CTkEntry(master=bookings ,placeholder_text="Mobile No.", width=200, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
passengerMobileNo.grid(row=6, column=0, sticky="w", padx=(20,0), pady=(20,0))

passengerEmail = ctk.CTkEntry(master=bookings ,placeholder_text="Email ID", width=350, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
passengerEmail.grid(row=7, column=0, sticky="w", padx=(20,0), pady=(20,0))

passengerIdProof = ctk.CTkEntry(master=bookings ,placeholder_text="ID Proof", width=350, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
passengerIdProof.grid(row=8, column=0, sticky="w", padx=(20,0), pady=(20,0))

def checkbox_event():
    print("checkbox toggled, current value:", check_var.get())

check_var = ctk.StringVar(value="of")
checkbox = ctk.CTkCheckBox(bookings, text="PERSON WITH CARE", command=checkbox_event, variable=check_var, onvalue="on", offvalue="off", font=('Poppins Medium', 20), text_color="#000")
checkbox.grid(row=9, column=0, sticky="w", padx=(20,0), pady=(20,0))
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)


bookingsLabel = ctk.CTkLabel(bookings, text="Bookings", font=('Poppins Medium', 40), fg_color="transparent", text_color="#000" )
bookingsLabel.grid(row=0, column=0, pady=(20, 20), padx=600)


confirmButton = ctk.CTkButton(bookings, text="Confirm",fg_color="#5790DF" ,text_color="white", font=('Inter', 18), corner_radius=25, width=120, height=50)
confirmButton.grid(row=13, column=0, pady=(20, 0), padx=(0, 70), sticky="e")



root.mainloop()