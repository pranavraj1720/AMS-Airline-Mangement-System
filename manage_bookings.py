from datetime import datetime, timedelta
import customtkinter as ctk
from screeninfo import get_monitors
import re
import mysql.connector
from datetime import datetime, timedelta
import ttkbootstrap as ttk
import subprocess
from session_manager import sessionManager
import json
root = ctk.CTk()
resoultion = get_monitors()[0]
screenWidth = resoultion.width
screenHeight = resoultion.height


bookedFlights = ctk.CTkScrollableFrame(master=root, fg_color="light grey")
bookedFlights.grid(row=1, column=1, sticky="nsew", pady=(20, 0), padx=20)


managebookingsLabel = ctk.CTkLabel(bookedFlights, text="Manage Bookings", font=('Poppins Bold', 27), text_color="#000")

managebookingsLabel.grid(row=0, column=0, pady=(20, 20), padx=(530, 0), sticky="w")


def create_box_frame(bookedflights, row_index, data):
    def get_flight_time_date():
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="pranavmysql",
            database="newuserdb"
        )

        mycursor = db.cursor()
        mycursor.execute("SELECT selectedDepartureTime, flightDate FROM bookedflights")
        result = mycursor.fetchall()
        db.close()
        print(f"result is {result} \n")
        return result
    
    def is_booking_open(flight_data, current_datetime):
        data = flight_data[row_index - 2]
        flight_datetime = datetime.combine(
                datetime.strptime(data[1], '%Y-%m-%d').date(),
                datetime.strptime(data[0], '%H:%M').time()
            )


        time_difference = flight_datetime - current_datetime
        print(f"time difference is {time_difference} \n")

        if timedelta(hours=3) <= time_difference and flight_datetime.date() >= current_datetime.date():
            return True

        return False
    
    boxFrame = ctk.CTkFrame(bookedflights, fg_color="#fff", )
    boxFrame.grid(row=row_index, column=0, sticky="new", pady=(10, 10), padx=(10, 10))

    originCity = ctk.CTkLabel(boxFrame, text=f"{data.get('selectedOriginCode')}", font=('Poppins Bold', 27), text_color="#000")
    originCity.grid(row=0, column=0, pady=(20, 0), padx=(20, 0), sticky="w")

    originTime = ctk.CTkLabel(boxFrame, text=f"{data.get('selectedDepartureTime')}", font=('Inter ', 19), text_color="#000", )
    originTime.grid(row=1, column=0, pady=(0, 20), padx=(20, 0), sticky="w")

    departureCity = ctk.CTkLabel(boxFrame, text=f"{data.get('selectedDepartureCode')}", font=('Poppins Bold', 27), text_color="#000")
    departureCity.grid(row=0, column=1, pady=(20, 0), padx=(100, 0), sticky="w")

    departureTime = ctk.CTkLabel(boxFrame, text=f"{data.get('selectedArrivalTime')}", font=('Inter Bold', 19), text_color="#000", )
    departureTime.grid(row=1, column=1, pady=(0, 20), padx=(100, 0), sticky="w")

    flightType = ctk.CTkLabel(boxFrame, text=f"{data.get('flightType')}", font=('Poppins Bold', 27), text_color="#000", )
    flightType.grid(row=0, column=1, pady=(20, 0), padx=(250, 0), sticky="w")

    flightTypeLabel = ctk.CTkLabel(boxFrame, text="Flight Type", font=('Inter Bold', 19), text_color="#000", )
    flightTypeLabel.grid(row=1, column=1, pady=(0, 20), padx=(250, 0), sticky="w")

    selectedFair = ctk.CTkLabel(boxFrame, text=f"{data.get('selectedFair')}", font=('Poppins Bold', 27), text_color="#000", )
    selectedFair.grid(row=0, column=1, pady=(20, 0), padx=(500, 0), sticky="w")

    selectedFairLabel = ctk.CTkLabel(boxFrame, text="Fair", font=('Inter Bold', 19), text_color="#000", )
    selectedFairLabel.grid(row=1, column=1, pady=(0, 20), padx=(500, 0), sticky="w")

    def convert_flight_date(flight_date):
        date_object = datetime.strptime(flight_date, '%Y-%m-%d')

        formatted_date = date_object.strftime('%d %b %Y')
        return formatted_date

    selectedFlightDate = ctk.CTkLabel(boxFrame, text=f"{convert_flight_date(data.get('flightDate'))}", font=('Poppins Bold', 27), text_color="#000", )
    selectedFlightDate.grid(row=0, column=1, pady=(20, 0), padx=(700, 0), sticky="w")

    selectedFlightDateLabel = ctk.CTkLabel(boxFrame, text="Flight Date", font=('Inter Bold', 19), text_color="#000", )
    selectedFlightDateLabel.grid(row=1, column=1, pady=(0, 20), padx=(700, 0), sticky="w")

    def cancel_flight_button_state():
        flight_data = get_flight_time_date()
        print(f" flight data is {flight_data} \n")
        current_datetime = datetime.now()

        # Extracting the flight data from the GUI library object
        flight_data_list = [(str(item[0]), str(item[1])) for item in flight_data]

        print(flight_data_list)

        if is_booking_open(flight_data_list, current_datetime):
            cancelFlight = ctk.CTkButton(boxFrame, text="Cancel Flight", fg_color="#5790DF",font=('Inter Bold', 18), text_color="#fff", corner_radius=25, width=120, height=40)
            cancelFlight.grid(row=0, column=1, pady=(20, 0), padx=(900,0), sticky="w")
        else:
            cancelFlight = ctk.CTkButton(boxFrame, text="Cancel Flight", fg_color="#5790DF",font=('Inter Bold', 18), text_color="#fff", corner_radius=25, width=120, height=40, state="disabled")
            cancelFlight.grid(row=0, column=1, pady=(20, 0), padx=(900,0), sticky="w")
    cancel_flight_button_state()


    def view_flight_callback():

        username = sessionManager().get_current_user()
    
        selected_origin_code = f"{data.get('selectedOriginCode')}"
        selected_departure_code = f"{data.get('selectedDepartureCode')}"
        selected_departure_time = f"{data.get('selectedDepartureTime')}"
        selected_arrival_time = f"{data.get('selectedArrivalTime')}"
        flight_type = f"{data.get('flightType')}"

        print(selected_origin_code, selected_departure_code, selected_departure_time, selected_arrival_time, flight_type)
            
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="pranavmysql",
            database="newuserdb"
        )

        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM bookedflights WHERE username = %s AND selectedOriginCode = %s AND selectedDepartureCode = %s AND selectedDepartureTime = %s AND selectedArrivalTime  = %s AND flightType = %s", (username, selected_origin_code, selected_departure_code, selected_departure_time, selected_arrival_time, flight_type)) #type: ignore
        rows = mycursor.fetchall()
        print(f"this is rows: {rows}")
        db.close()

        for row in rows:
            print(f"this is row {row}")
            name = row[1] 
            gender = row[2]  
            age = row[3] 
            contact = row[4]  
            email = row[5]  
            idProof = row[6] 
            selected_fair = row[7]  
            selected_origin_code = row[8]  
            selected_departure_code = row[9] 
            selected_departure_time = row[10] 
            selected_arrival_time = row[11]  
            flight_type = row[12]  
            flight_date = row[13]  
        
            sessionManager().set_view_flight_data(username, name, gender, age, contact, email, idProof, selected_fair, selected_origin_code, selected_departure_code,selected_departure_time,selected_arrival_time,flight_type, flight_date)  
        subprocess.run(["python", "view_flight.py"]) 

    viewFlight = ctk.CTkButton(boxFrame, text="View", fg_color="#5790DF",font=('Inter Bold', 18), text_color="#fff", corner_radius=25, width=120, height=40, command=view_flight_callback)
    viewFlight.grid(row=0, column=1, pady=(20, 0), padx=(1070,0), sticky="w")

    bookedFlights.grid_rowconfigure(1, weight=1)
    bookedFlights.grid_columnconfigure(0, weight=1)


def get_table_headers():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="pranavmysql",
        database="newuserdb"
    )
    
    cursor = db.cursor()
    query = "DESCRIBE bookedflights"
    cursor.execute(query)
    headers = [row[0] for row in cursor.fetchall()]
    return headers

def get_flight_data():
    username = sessionManager().get_current_user()
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="pranavmysql",
        database="newuserdb"
    )

    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM bookedflights WHERE username = %s", (username, )) # type: ignore
    result = mycursor.fetchall()
    db.close()

    
    table_headers = get_table_headers()
    
    data_list = []

    for row in result:
        row_data = {}

        key_list = [row[8], row[9], row[10], row[11]]
        if not any(item['selectedOriginCode'] == key_list[0] and item['selectedDepartureCode'] == key_list[1] and item['selectedDepartureTime'] == key_list[2] and item['selectedArrivalTime'] == key_list[3] for item in data_list):
            for index in range(len(table_headers)):
                row_data[table_headers[index]] = row[index]

            data_list.append(row_data)
        
        
    row = 2

    for content in data_list:
        # print(content)
        create_box_frame(bookedFlights, row, content)
        row += 1
    print(json.dumps(data_list, indent = 2))

# Call the function to generate unique blocks
get_flight_data()
# print(get_table_headers())

# print(flight_data)
# Setting appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Manage Bookings")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.mainloop()
