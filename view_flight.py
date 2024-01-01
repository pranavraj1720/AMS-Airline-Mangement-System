import customtkinter as ctk
from screeninfo import get_monitors
import re
import mysql.connector
from session_manager import sessionManager
import json
root = ctk.CTk()
resoultion = get_monitors()[0]
screenWidth = resoultion.width
screenHeight = resoultion.height


viewFlight = ctk.CTkScrollableFrame(master=root, fg_color="light grey")
viewFlight.grid(row=1, column=1, sticky="nsew", pady=(20, 0), padx=20)


viewFilghtLabel = ctk.CTkLabel(viewFlight, text="View Passenger Details", font=('Poppins Bold', 27), text_color="#000")
viewFilghtLabel.grid(row=0, column=0, pady=(20, 20), padx=(500, 0), sticky="w")


def gen_passenger_details(frame, row_index, data):

    boxFrame = ctk.CTkFrame(frame, fg_color="#fff")
    boxFrame.grid(row=row_index, column=0, sticky="new", pady=(10, 10), padx=(10, 10))

    flightLabel = ctk.CTkLabel(boxFrame, text=f"FROM {data.get('selectedOriginCode')} TO {data.get('selectedDepartureCode')}", font=('Poppins', 27), text_color="#000")
    flightLabel.grid(row=1, column=0, pady=(20, 0), padx=(300, 0), sticky="w")

    passengerNameLabel = ctk.CTkLabel(boxFrame, text="Passenger Name : ", font=('Poppins', 22), text_color="#000")
    passengerNameLabel.grid(row=2, column=0, pady=(20, 0), padx=(20, 0), sticky="w")

    passengerName = ctk.CTkLabel(boxFrame, text=f"{data.get('name')}", font=('Poppins', 22), text_color="#000")
    passengerName.grid(row=2, column=0, pady=(20, 0), padx=(230, 0), sticky="w")

    genderLabel = ctk.CTkLabel(boxFrame, text="Gender : ", font=('Poppins', 22), text_color="#000")
    genderLabel.grid(row=3, column=0, pady=(0, 0), padx=(20, 0), sticky="w")

    passengerGender = ctk.CTkLabel(boxFrame, text=f"{data.get('gender')}", font=('Poppins', 22), text_color="#000")
    passengerGender.grid(row=3, column=0, pady=(0, 0), padx=(120, 0), sticky="w")

    ageLabel = ctk.CTkLabel(boxFrame, text="Passenger Age : ", font=('Poppins', 22), text_color="#000")
    ageLabel.grid(row=4, column=0, pady=(0, 0), padx=(20, 0), sticky="w")

    passengerAge = ctk.CTkLabel(boxFrame, text=f"{data.get('age')}", font=('Poppins', 22), text_color="#000")
    passengerAge.grid(row=4, column=0, pady=(0, 0), padx=(210, 0), sticky="w")

    passengerContactLabel = ctk.CTkLabel(boxFrame, text="Contact No. : ", font=('Poppins', 22), text_color="#000")
    passengerContactLabel.grid(row=5, column=0, pady=(0, 20), padx=(20, 0), sticky="w")

    passengerContact = ctk.CTkLabel(boxFrame, text=f"{data.get('contact')}", font=('Poppins', 22), text_color="#000")
    passengerContact.grid(row=5, column=0, pady=(0, 20), padx=(175, 0), sticky="w")

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

def get_passenger_details():
    username = sessionManager().get_current_user()
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="pranavmysql",
        database="newuserdb"
    )

    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM viewflight WHERE username = %s", (username, )) # type: ignore
    result = mycursor.fetchall()
    db.close()

    
    table_headers = get_table_headers()
    
    data_list = []

    for row in result:
        row_data = {}

        
        
        for index in range(len(table_headers)):
            row_data[table_headers[index]] = row[index]

        data_list.append(row_data)
        
        
    row = 2

    for content in data_list:
        # print(content)
        gen_passenger_details(viewFlight, row, content)
        row += 1
    print(json.dumps(data_list, indent = 2))

get_passenger_details()

def on_win_closing():
    username = sessionManager().get_current_user()
    sessionManager().remove_view_flight(username)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_win_closing)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root.geometry(f"{screenWidth}x{screenHeight}")
root.title("View Flight")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.mainloop()