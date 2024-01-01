from tkinter import NO
import mysql.connector
from data import cities_data
class sessionManager:
    def __init__(self, host="localhost", user="root", password="pranavmysql", database="newuserdb"):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.create_table()

        

    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                username VARCHAR(255) NOT NULL,
                selectedOriginCode VARCHAR(255),
                selectedDepartureCode VARCHAR(255),
                selectedDepartureTime VARCHAR(255),
                selectedArrivalTime VARCHAR(255),
                flightType VARCHAR(255),
                economyFair VARCHAR(255),
                businessFair VARCHAR(255),
                firstClassFair VARCHAR(255),    
                flightDate VARCHAR(50)
            )
        ''')      
        self.db.commit()

    def set_current_user(self, username):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO sessions (username) VALUES (%s)", (username, ))
        self.db.commit()

    def get_current_user(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT username FROM sessions ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            print(result[0])
            return result[0]
        else:
            return None
    
    def set_flights_data(self, selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime, flightType, economyFair, businessFair, firstClassFair, flightDate):
        username = self.get_current_user()
        cursor = self.db.cursor()
        cursor.execute("""
        UPDATE sessions
        SET selectedOriginCode = %s, selectedDepartureCode = %s, selectedDepartureTime = %s, selectedArrivalTime = %s, flightType = %s, economyFair = %s, businessFair = %s, firstClassFair = %s, flightDate = %s
        WHERE username = %s
    """, (selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime , flightType, economyFair, businessFair, firstClassFair, flightDate, username)) # type: ignore
        self.db.commit()

    def set_view_flight_data(self, username,name, gender, age, contact, email, idProof, selectedFair, selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime, flightType, flightDate):
        cursor = self.db.cursor()

        query = "INSERT INTO viewflight (username, name, gender, age, contact, email, idProof, selectedFair, selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime, flightType, flightDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (username, name, gender, age, contact, email, idProof, selectedFair, selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime, flightType, flightDate)

        cursor.execute(query, values) # type: ignore
        self.db.commit() 

    
    def get_flights_data(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime, flightType, economyFair, businessFair, firstClassFair, flightDate  FROM sessions ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        
        selectedDepartureCode = None
        selectedOriginCode = None
        selectedDepartureTime = None
        selectedArrivalTime = None
        flightType = None
        economyFair = None
        businessFair = None
        firstClassFair = None
        flightDate = None
        if result: 
            selectedOriginCode, selectedDepartureCode, selectedDepartureTime, selectedArrivalTime, flightType, economyFair, businessFair, firstClassFair, flightDate = result


        departure_name = "".join([city['name'] for city in cities_data if selectedDepartureCode == city['cityCode']])
        origin_name = "".join([city['name'] for city in cities_data if selectedOriginCode == city['cityCode']])

        return origin_name, departure_name , selectedArrivalTime, selectedDepartureTime, selectedOriginCode, selectedDepartureCode, flightType, economyFair, businessFair, firstClassFair, flightDate
                
    def remove_session(self, username):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM sessions WHERE username = %s", (username,))
        self.db.commit()

    def remove_booked_flights(self, username):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM bookedflights WHERE username = %s", (username,))
        self.db.commit()
    def remove_view_flight(self, username):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM viewflight WHERE username = %s", (username,))
        self.db.commit()
