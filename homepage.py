import customtkinter as ctk
from screeninfo import get_monitors
import re
import mysql.connector
from datetime import datetime
import ttkbootstrap as ttk


resolution = get_monitors()[0]
screenWidth = resolution.width
screenHeight = resolution.height

# Setting appearance mode and color theme
root = ttk.Window(themename='lumen')
root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Book Tickets")

# Creating SideBar
sideBar = ctk.CTkCanvas(root, width=350, height=screenHeight, bg="white")
sideBar.grid(row=0, column=0, rowspan=2)  # Adjusting row and rowspan


sideBar.create_line(350, 0, 350, screenHeight, fill="grey", width=3)

sideBar.create_aa_circle(180, 100, 70, fill="light grey")
userName = ctk.CTkLabel(sideBar, text="USERNAME", text_color="black", font=('Poppins Medium', 20), bg_color="white")
sideBar.create_window(175, 200, window=userName)

manageBookings = ctk.CTkButton(sideBar, text="Manage Bookings", text_color="white", font=('Inter', 15),
                                bg_color="white", corner_radius=25, width=120, height=50)
sideBar.create_window(175, 280, window=manageBookings)

sideBar.create_line(350, 230, 0, 230, fill="grey", width=2)

faqS = ctk.CTkButton(sideBar, text="FAQs", text_color="white", font=('Inter', 15),
                                bg_color="white", corner_radius=25, width=120, height=50)
sideBar.create_window(175, 280, window=manageBookings)
sideBar.create_window(175, 350, window=faqS)

logOut = ctk.CTkButton(sideBar, text="Log Out", text_color="white", font=('Inter', 18),fg_color="red", hover_color="red" , corner_radius=25, width=120, height=50)
sideBar.create_window(175, 280, window=manageBookings)
sideBar.create_window(175, 650, window=logOut)

# Creating the search frame at the top right
searchFrame = ttk.Frame(master=root, style='default.TFrame')
searchFrame.grid(row=0, column=1, sticky="n", pady=(20, 0), padx=20)
searchFrame['borderwidth'] = 1
searchFrame['relief'] = 'groove'

fromCity = ttk.Entry(master=searchFrame, width=13, font=('calibri', 25))
fromCity.grid(row=0, column=0, pady=(20, 20), padx=30)

toCity = ttk.Entry(master=searchFrame, width=13, font=('calibri', 25))
toCity.grid(row=0, column=3, pady=(20, 20), padx=20)

myDate = ttk.DateEntry(searchFrame, bootstyle="default")
myDate.grid(row=0, column=4, pady=(30, 30), padx=15)

searchFlights = ctk.CTkButton(searchFrame, text="Search Flights", text_color="white", font=('Inter', 18),
                               corner_radius=25, width=120, height=50)
searchFlights.grid(row=0, column=5, pady=(30, 30), padx=15)

# Recommended flights frame
recommendedFlights = ttk.Frame(master=root, style='default.TFrame')
recommendedFlights.grid(row=1, column=1, sticky="nsew", pady=(20, 0), padx=20)
recommendedFlights['borderwidth'] = 1
recommendedFlights['relief'] = 'groove'

# Add your recommended flights content to this frame

# Recomended flights label
recommendedFlightsLabel = ctk.CTkLabel(recommendedFlights, text="Featured Destinations From", font=('Poppins Medium', 25), text_color="black")
recommendedFlightsLabel.grid(row=0, column=2, pady=(20, 10), padx=(250,10), sticky="nsew")

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

cityMenu_var = ctk.StringVar(value="City")
cityMenu = ctk.CTkOptionMenu(recommendedFlights,values=["Vadodara", "Mumbai"], command=optionmenu_callback,variable=cityMenu_var, font=('Inter', 18), width=80, height=40)
cityMenu.grid(row=0, column=4)
cityMenu.set("City")





root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Run the Tkinter main loop
root.mainloop()