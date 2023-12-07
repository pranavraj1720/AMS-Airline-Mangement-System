import customtkinter as ctk
from screeninfo import get_monitors
from session_manager import sessionManager
import re
import mysql.connector
import subprocess
root = ctk.CTk()
# Setting appearance mode and color theme 
ctk.set_appearance_mode("black")
ctk.set_default_color_theme("blue") 

resoultion = get_monitors()[0]
screenWidth = resoultion.width
screenHeight = resoultion.height


root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Bookings")




bookings = ctk.CTkScrollableFrame(master=root, fg_color="white", border_color="#fff", border_width=2, corner_radius=10)
bookings.grid(row=1, column=1, sticky="nsew", padx=(15, 15), pady=20)

PassengerNo = ctk.CTkLabel(bookings, text="No. of Passenger", font=('Poppins Medium', 20), fg_color="transparent", text_color="#000")
PassengerNo.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="w")

fair = ctk.CTkLabel(bookings, text="Select Your Fair:", font=('Poppins Medium', 20), fg_color="transparent", text_color="#000")
fair.grid(row=3, column=0, pady=(0, 0), padx=20, sticky="w")

flight_data = sessionManager().get_flights_data()




boxFrame = ctk.CTkFrame(bookings, fg_color="light grey")
boxFrame.grid(row=0, column=0, sticky="nsew", pady=(10, 10), padx=0)

originCity = ctk.CTkLabel(boxFrame, text=f"{flight_data[0]}", font=('Poppins Bold', 27), text_color="#000")
originCity.grid(row=0, column=0, pady=(20, 0), padx=(20, 0), sticky="w")

originTime = ctk.CTkLabel(boxFrame, text=f"{flight_data[2]}", font=('Inter ', 19), text_color="#000", )
originTime.grid(row=1, column=0, pady=(0, 20), padx=(20, 0), sticky="w")

departureCity = ctk.CTkLabel(boxFrame, text=f"{flight_data[1]}", font=('Poppins Bold', 27), text_color="#000")
departureCity.grid(row=0, column=1, pady=(20, 0), padx=(100, 0), sticky="w")

departureTime = ctk.CTkLabel(boxFrame, text=f"{flight_data[3]}", font=('Inter Bold', 19), text_color="#000", )
departureTime.grid(row=1, column=1, pady=(0, 20), padx=(100, 0), sticky="w")

flightType = ctk.CTkLabel(boxFrame, text=f"{flight_data[6]}", font=('Poppins Bold', 27), text_color="#000", )
flightType.grid(row=0, column=1, pady=(20, 0), padx=(350, 0), sticky="w")

flightTypeLabel = ctk.CTkLabel(boxFrame, text="Flight Type", font=('Inter Bold', 19), text_color="#000", )
flightTypeLabel.grid(row=1, column=1, pady=(0, 20), padx=(350, 0), sticky="w")

economyFair = ctk.CTkLabel(boxFrame, text=f"{flight_data[7]}", font=('Poppins Bold', 27), text_color="#000", )
economyFair.grid(row=0, column=1, pady=(20, 0), padx=(600, 0), sticky="w")

economyFairLabel = ctk.CTkLabel(boxFrame, text="Economy", font=('Inter Bold', 19), text_color="#000", )
economyFairLabel.grid(row=1, column=1, pady=(0, 20), padx=(600, 0), sticky="w")

businessFair = ctk.CTkLabel(boxFrame, text=f"{flight_data[8]}", font=('Poppins Bold', 27), text_color="#000", )
businessFair.grid(row=0, column=1, pady=(20, 0), padx=(800, 0), sticky="w")

businessFairLabel = ctk.CTkLabel(boxFrame, text="Business Class", font=('Inter Bold', 19), text_color="#000", )
businessFairLabel.grid(row=1, column=1, pady=(0, 20), padx=(800, 0), sticky="w")

firstClassFair = ctk.CTkLabel(boxFrame, text=f"{flight_data[9]}", font=('Poppins Bold', 27), text_color="#000", )
firstClassFair.grid(row=0, column=1, pady=(20, 0), padx=(1000, 20), sticky="w")

firstClassFairLabel = ctk.CTkLabel(boxFrame, text="First Class", font=('Inter Bold', 19), text_color="#000", )
firstClassFairLabel.grid(row=1, column=1, pady=(0, 20), padx=(1000, 20), sticky="w")





def on_city_menu_change(none):
        num_passengers = int(cityMenu_var.get())
        row = 5
        for i in range(num_passengers):
            generate_passenger_details(row, i)
            row += 1




# Dropdown Menu
cityMenu_var = ctk.StringVar(value="No. of Passenger:")
cityMenu = ctk.CTkOptionMenu(bookings, values=["1", "2", "3", "4", "5"], variable=cityMenu_var, font=('Inter', 18), width=30, height=30, fg_color="#5790DF", button_color="#5790DF", command=on_city_menu_change)
cityMenu.grid(row=2, column=0, padx=(200,0), sticky="w", pady=(20, 0))
cityMenu.set("0")

fairMenu_var = ctk.StringVar(value="Select Your Fair:")
fairMenu = ctk.CTkOptionMenu(bookings, values=[f"{flight_data[7]}", f"{flight_data[8]}", f"{flight_data[9]}"], variable=fairMenu_var, font=('Inter', 18), width=30, height=30, fg_color="#5790DF", button_color="#5790DF", )
fairMenu.grid(row=3, column=0, padx=(200,0), sticky="w", pady=(0, 0))
fairMenu.set("Select")

def is_valid_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email)
def open_new_file():
    root.destroy()
    subprocess.run(["python", "payment.py"]) 
def generate_passenger_details(row_index, index):
    passengerFields = ctk.CTkFrame(bookings, fg_color="light grey", height=400)
    passengerFields.grid(row=row_index, column=0, sticky="ew" ,  padx=(10,20), pady=(20,20))
        

    passengerName = ctk.CTkEntry(master=passengerFields ,placeholder_text=f"Name of Passenger {index + 1}", width=450, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    passengerName.grid(row=0, column=0, sticky="w", padx=(20,0) , pady=(30, 0))

    passengerGender = ctk.CTkEntry(master=passengerFields ,placeholder_text="Gender", width=200, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    passengerGender.grid(row=1, column=0, sticky="w", padx=(20,0), pady=(20,0))

    passengerAge = ctk.CTkEntry(master=passengerFields ,placeholder_text="Age", width=150, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    passengerAge.grid(row=1, column=0, sticky="w", padx=(250,0), pady=(20,0))

    passengerMobileNo = ctk.CTkEntry(master=passengerFields ,placeholder_text="Mobile No.", width=200, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    passengerMobileNo.grid(row=3, column=0, sticky="w", padx=(20,0), pady=(20,0))

    passengerEmail = ctk.CTkEntry(master=passengerFields ,placeholder_text="Email ID", width=350, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    passengerEmail.grid(row=4, column=0, sticky="w", padx=(20,0), pady=(20,0))

    passengerIdProof = ctk.CTkEntry(master=passengerFields ,placeholder_text="ID Proof", width=350, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    passengerIdProof.grid(row=5, column=0, sticky="w", padx=(20,0), pady=(20,0))


    passengerMedicalAssistance_var = ctk.StringVar(value="of")
    passengerMedicalAssistance = ctk.CTkCheckBox(passengerFields, text="PERSON WITH MEDICAL ASSISTANCE", variable=passengerMedicalAssistance_var, onvalue="on", offvalue="off", font=('Poppins Medium', 20), text_color="#000")
    passengerMedicalAssistance.grid(row=6, column=0, sticky="w", padx=(20,0), pady=(20,20))

    def booked_flights():
        username = sessionManager().get_current_user()
        name = passengerName.get()
        gender = passengerGender.get()
        age = int(passengerAge.get())
        contact = int(passengerMobileNo.get())
        email = passengerEmail.get()
        idProof = int(passengerIdProof.get())
        fair = str( fairMenu.get())
        db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="pranavmysql",
        database="newuserdb"
)
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO bookedFlights (username, name, gender, age, contact, email, idProof, selectedFair) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, name, gender, age, contact, email, idProof, fair))


        db.commit()

    def validate_passenger_details():
        passenger_name = passengerName.get()
        passenger_gender = passengerGender.get().capitalize()
        passenger_age = passengerAge.get()
        passenger_mobile = passengerMobileNo.get()
        passenger_email = passengerEmail.get()
        passenger_id = passengerIdProof.get()

        if passenger_name == "":
            error_label.configure(text="Please enter name of passenger")
        elif passenger_gender not in ["Male", "Female"]:
            error_label.configure(text="Please enter correct gender")
        elif not passenger_age.isdigit() or int(passenger_age) > 100:
            error_label.configure(text="Please enter valid age")
        elif not (passenger_mobile.isdigit() and len(passenger_mobile) == 10):    
            error_label.configure(text="Please enter valid contact no.")
        elif not is_valid_email(passenger_email):
            error_label.configure(text="Please enter valid email")
        elif not (passenger_id.isdigit() and len(passenger_id) == 12):
            error_label.configure(text="aadhar card must be a 12 digit number") 
        else:
                # All fields are valid, clear the error message and proceed with signup
            error_label.configure(text="")
            error_label.grid_forget()
            booked_flights()
            open_new_file()

    def delete_passenger_widget():
        passengerFields.destroy()

    confirmButton = ctk.CTkButton(passengerFields, text="Confirm",fg_color="#5790DF" ,text_color="white", font=('Inter', 18), corner_radius=25, width=120, height=50, command=validate_passenger_details)
    confirmButton.grid(row=6, column=0, pady=(20, 20), padx=(1150, 20), sticky="w")

    if index > 0:
        deletePassenger = ctk.CTkButton(passengerFields, text="Delete",fg_color="#EA4E4C" ,text_color="white", font=('Inter', 18), corner_radius=25, width=120, height=50, command=delete_passenger_widget)
        deletePassenger.grid(row=6, column=0, pady=(20, 20), padx=(1000, 20), sticky="w")

    error_label = ctk.CTkLabel(passengerFields, text="", text_color="red",  font=('Inter', 15))
    error_label.grid(row=7, column=0, columnspan=1, pady=(0, 10))  
        

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)






root.mainloop()