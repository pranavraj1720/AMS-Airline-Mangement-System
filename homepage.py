
import customtkinter as ctk
from screeninfo import get_monitors
import re
import mysql.connector
from datetime import datetime
import ttkbootstrap as ttk
from tkcalendar import DateEntry
from indigo_api import INDIGO_DB
from data import cities_data
from datetime import datetime
from session_manager import sessionManager
import subprocess
# from login import user_info
resolution = get_monitors()[0]
screenWidth = resolution.width
screenHeight = resolution.height


currentUsername = sessionManager().get_current_user()
# Setting appearance mode and color theme
root = ttk.Window(themename='lumen')
root.geometry(f"{screenWidth}x{screenHeight}")
root.maxsize(False, False)
root.title("Book Tickets")

# Creating SideBar
sideBar = ctk.CTkCanvas(root, width=350, height=screenHeight, bg="white")
sideBar.grid(row=0, column=0, rowspan=2)  # Adjusting row and rowspan

sideBar.create_line(350, 0, 350, screenHeight, fill="grey", width=3)

sideBar.create_aa_circle(180, 100, 70, fill="light grey")
userName = ctk.CTkLabel(sideBar, text=f"{currentUsername}", text_color="black", font=('Poppins Medium', 20), bg_color="white")
sideBar.create_window(175, 200, window=userName)

manageBookings = ctk.CTkButton(sideBar, text="Manage Bookings", text_color="white", font=('Inter', 15),
                               bg_color="white", fg_color="#5790DF", corner_radius=25, width=120, height=50)
sideBar.create_window(175, 280, window=manageBookings)

sideBar.create_line(350, 230, 0, 230, fill="grey", width=2)

faqS = ctk.CTkButton(sideBar, text="FAQs", text_color="white", fg_color="#5790DF", font=('Inter', 15),
                     bg_color="white", corner_radius=25, width=120, height=50)
sideBar.create_window(175, 350, window=faqS)

def logout():
    if currentUsername:
        sessionManager().remove_session(currentUsername)
    root.destroy()

logOut = ctk.CTkButton(sideBar, text="Log Out", text_color="white", font=('Inter', 18), fg_color="red",hover_color="#EA4E4C", corner_radius=25, width=120, height=50, command=logout)
sideBar.create_window(175, 650, window=logOut)


def optionmenu_callback():

    error_label = ctk.CTkLabel(root, text="", text_color="red",  font=('Inter', 15))
    error_label.grid(row=1, column=0, pady=(0, 0)) 
    from_city = fromCity.get().strip().capitalize()
    to_city = toCity.get().strip().capitalize()
    from_city_code = get_city_code(from_city)
    to_city_code = get_city_code(to_city)


    if not any(city['name'] == from_city for city in cities_data) or not any(city['name'] == to_city for city in cities_data):
        error_label.configure(text="Please enter correct cities names")
    else:
        error_label.grid_forget()
        show_flights(from_city_code, to_city_code)



    


    

# Creating the search frame at the top 
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


    

searchFlights = ctk.CTkButton(searchFrame, text="Search Flights",fg_color="#5790DF" ,text_color="white", font=('Inter', 18), corner_radius=25, width=120, height=50, command=optionmenu_callback)
searchFlights.grid(row=0, column=5, pady=(30, 30), padx=15)




# Recomended flights label centered
recommendedFlights = ctk.CTkScrollableFrame(master=root, fg_color="light grey")
recommendedFlights.grid(row=1, column=1, sticky="nsew", pady=(20, 0), padx=20)



def convert_time_format(input_time):
    # Parse input time string
    parsed_time = datetime.strptime(input_time, "%Y-%m-%dT%H:%M:%S")
    
    # Format as "dd-mm-yy"
    formatted_time = parsed_time.strftime("%H:%M")
    
    return formatted_time


def create_box_frame(recommended_flights_frame, journey_data, row_index):
    boxFrame = ctk.CTkFrame(recommended_flights_frame, fg_color="#fff", )
    boxFrame.grid(row=row_index, column=0, sticky="new", pady=(10, 10), padx=(10, 10))

    departureTime = ctk.CTkLabel(boxFrame, text=f"{convert_time_format(journey_data['designator']['departure'])}", font=('Inter Bold', 25), text_color="black",)
    departureTime.grid(row=0, column=0, pady=(20, 0), padx=(20, 0), sticky="w")

    cityOriginCodeLabel = ctk.CTkLabel(boxFrame, text=f"{journey_data['designator']['origin']}", font=('Inter', 18), text_color="black", )
    cityOriginCodeLabel.grid(row=1, column=0, pady=(0,10), padx=(20,0), sticky="w")

    cityDepartureCodeLabel = ctk.CTkLabel(boxFrame, text=f"{journey_data['designator']['destination']}", font=('Inter', 18), text_color="black", )
    cityDepartureCodeLabel.grid(row=1, column=0, pady=(0,10), padx=(160,0), sticky="w")

    arrivalTime = ctk.CTkLabel(boxFrame, text=f"{convert_time_format(journey_data['designator']['arrival'])}", font=('Inter Bold', 25), text_color="black", )
    arrivalTime.grid(row=0, column=0, pady=(20, 0), padx=(160, 0), sticky="w")

    layOverLabel = ctk.CTkLabel(boxFrame, text=f"{journey_data['flightType']}", font=('Inter Bold', 23), text_color="black" )
    layOverLabel.grid(row=0, column=0, pady=(20, 0), padx=(250, 0), sticky="w")

    passengerFares = ctk.CTkLabel(boxFrame, text=f"₹ {convert_amount_format(journey_data['passengerFares'][0]['totalFareAmount'])}", font=('Inter Bold', 23), text_color="black", )
    passengerFares.grid(row=0, column=0, pady=(20, 0), padx=(380, 0), sticky="w")

    


    def flight():
        selectedOriginCode = f"{journey_data['designator']['origin']}"
        selectedDepartureCode = f"{journey_data['designator']['destination']}"
        selectedDepartureTime = f"{convert_time_format(journey_data['designator']['departure'])}"
        selectedArrivalTime = f"{convert_time_format(journey_data['designator']['arrival'])}"
        flightType = f"{journey_data['flightType']}" 
        economyFair = f"{convert_amount_format(journey_data['passengerFares'][0]['totalFareAmount'])}"
        businessFair = f"{convert_amount_format(journey_data['passengerFares'][1]['totalFareAmount'])}"
        firstClassFair = f"{convert_amount_format(journey_data['passengerFares'][2]['totalFareAmount'])}"
        sessionManager().set_flights_data(selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime, flightType, economyFair, businessFair, firstClassFair)
        subprocess.run(["python", "bookings.py"])  

    details_button = ctk.CTkButton(boxFrame, text="Book", text_color="#fff", font=('Inter', 18), corner_radius=25, width=150, height=40, fg_color="#5790DF", command=flight)
    details_button.grid(row=0, column=0, pady=(20, 0), padx=(750, 10), sticky="w")


    recommendedFlights.grid_rowconfigure(1, weight=1)
    recommendedFlights.grid_columnconfigure(0, weight=1)




def convert_amount_format(amount):
    formatted_amount = '{:,.2f}'.format(amount)
    return formatted_amount

def get_city_code(city_name):

    city = [city for city in cities_data if city['name'] == city_name]
    if len(city) != 0:
        return city[0].get('cityCode')
        
    else:
        return 
    
        
        

        



def convert_date_format(selectedDate):
    parsed_date = datetime.strptime(selectedDate, "%d-%m-%Y")
    formatted_date = parsed_date.strftime("%Y-%m-%d")

    return formatted_date



def show_flights(src, dest, date=None):
    flightDate = convert_date_format(myDate.entry.get())
    for widget in recommendedFlights.winfo_children():
        widget.grid_remove()


    row_index = 0
    alljourneys = INDIGO_DB().get_fligits(src, dest, flightDate)
    for index in range(0, len(alljourneys)):
        create_box_frame(recommendedFlights, alljourneys[index], row_index)
        row_index+=1



# # # Dropdown Menu
# cityMenu_var = ctk.StringVar(value="City")
# cityMenu = ctk.CTkOptionMenu(recommendedFlights, values=["Vadodara", "Mumbai"], variable=cityMenu_var, font=('Inter', 18), width=30, height=30, fg_color="#5790DF", button_color="#5790DF")
# cityMenu.grid(row=0, column=3, pady=(0, 0), padx=(0, 10))
# cityMenu.set("Vadodara")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)


root.mainloop()