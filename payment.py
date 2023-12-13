from calendar import c
import re
import customtkinter as ctk
from screeninfo import get_monitors
import mysql.connector
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#root = Tk()
root = ctk.CTk()
resolution = get_monitors()[0]
screenWidth = resolution.width
screenHeight = resolution.height
root.title('Payment')
root.geometry(f"{screenWidth}x{screenHeight}")
root.maxsize(False, False)


def get_selected_fair():
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="pranavmysql",
    database="newuserdb"
)
    mycursor = db.cursor()
    mycursor.execute("SELECT selectedFair FROM bookedflights")
    result = mycursor.fetchone()
    db.close()

    if result:
        return result[0]
    else:
        return None

# Create Tabview
tabs = ctk.CTkTabview(root,
	width=780,
	height=500,
	corner_radius=10,
	fg_color="#fff",
	segmented_button_fg_color="#5790DF",
	segmented_button_selected_color="#424141",
	segmented_button_selected_hover_color="#5790DF",
	segmented_button_unselected_color="#5790DF",
	text_color="#fff",
	state="normal",
		)
def on_tab_change(event):
    currentTab = tabs.get()
    if currentTab == "Credit Card" or currentTab == "Debit Card":
        gen_card_info(currentTab, type = currentTab)
    if currentTab == "UPI":
        gen_upi_info(currentTab, type = currentTab)

tabs.pack(pady=100)
debitCard = tabs.add("Debit Card")
debitCard.bind("<Map>", on_tab_change)
creditCard = tabs.add("Credit Card")
creditCard.bind("<Map>", on_tab_change)
upi = tabs.add("UPI")
upi.bind("<Map>", on_tab_change)

tabs.set("UPI")






def gen_card_info(frame, type = "DEBIT Card"):
        
    def format_card_number(event):
        card_number = cardNumber.get()
        card_number = card_number.replace(" ", "")
        card_number = ''.join(char for char in card_number if char.isdigit())
        card_number = card_number[:16]
        formatted_card_number = ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])
        cardNumber.delete(0, 'end')
        cardNumber.insert(0, formatted_card_number)


    def format_card_expiry(event):
        card_expiry = cardExpiry.get()
        card_expiry = card_expiry.replace(" ", "")
        card_expiry_digits = ''.join(char for char in card_expiry if char.isdigit())

        card_expiry_digits = card_expiry_digits[:4]

        formatted_card_expiry = '/'.join([card_expiry_digits[i:i+2] for i in range(0, len(card_expiry_digits), 2)])

        cardExpiry.delete(0, 'end')
        cardExpiry.insert(0, formatted_card_expiry)

    def format_card_cvv(event):
        card_cvv = cardCVV.get()
        card_cvv_digits = "".join(char for char in card_cvv if char.isdigit())
        card_cvv_digits = card_cvv_digits[:3]
        cardCVV.delete(0, "end")
        cardCVV.insert(0, card_cvv_digits)

    def validate_payment():
        cardnumber = cardNumber.get().replace(' ', "")
        cardname = cardName.get()
        cardcvv = cardCVV.get()
        cardexpiry = cardExpiry.get()

        if not cardnumber or cardname or cardcvv or cardexpiry:
            error_label.configure(text="Invalid Field(s)")
        else:
            error_label.configure(text="")
            error_label.grid_forget()
            pass
    
    CardLabel = ctk.CTkLabel(tabs.tab(frame), text="{}".format(type), font=('Poppins Bold', 27), text_color="#000")

    CardLabel.grid(row=2, column=0, pady=(20, 0), padx=(190, 0), sticky="e")

    cardNumber = ctk.CTkEntry(master=tabs.tab(frame) ,placeholder_text=f"CARD NUMBER", width=450, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    cardNumber.grid(row=3, column=0, sticky="w", padx=(20,0) , pady=(30, 0))
    cardNumber.bind("<KeyRelease>", format_card_number)

    cardName = ctk.CTkEntry(master=tabs.tab(frame) ,placeholder_text=f"NAME ON CARD", width=450, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    cardName.grid(row=4, column=0, sticky="w", padx=(20,0) , pady=(20, 0))

    cardCVV = ctk.CTkEntry(master=tabs.tab(frame) ,placeholder_text="CVV", width=80, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000", show="*")
    cardCVV.grid(row=5, column=0, sticky="w", padx=(20,0), pady=(20,0))
    cardCVV.bind("<KeyRelease>", format_card_cvv)

    cardExpiry = ctk.CTkEntry(master=tabs.tab(frame) ,placeholder_text="mm/yy", width=100, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    cardExpiry.grid(row=5, column=0, sticky="w", padx=(120,0), pady=(20,0))
    cardExpiry.bind("<KeyRelease>", format_card_expiry)

    finalFair = ctk.CTkLabel(tabs.tab(frame), text=f"Amount Payable: {get_selected_fair()} ", font=('Poppins Bold', 20), text_color="#000")
    finalFair.grid(row=6, column=0, pady=(20, 0), padx=(20, 0), sticky="w")

    payButton = ctk.CTkButton(tabs.tab(frame), text="Pay",fg_color="#5790DF" ,text_color="white", font=('Inter', 18), corner_radius=25, width=120, height=40, command=validate_payment)
    payButton.grid(row=7, column=0, pady=(20, 50), padx=(20,0), sticky="w")


    error_label = ctk.CTkLabel(tabs.tab(frame), text="", text_color="red",  font=('Inter', 15))
    error_label.grid(row=8, column=0, pady=(0, 0), padx=(250,0)) 



def gen_upi_info(frame, type = "UPI"):
    def validate_payment():
        upi_number = upiNumber.get()

        if not upiNumber:
            error_label.configure(text="Invalid Field(s)")
        elif not len(upi_number) in [8,9,10]:
            error_label.configure(text="Invalid UPI No.")
        else:
            error_label.configure(text="")
            error_label.grid_forget()
            pass

    def format_upi_number(event):
        upi_number = upiNumber.get()
        upi_number_digits = ''.join(char for char in upi_number if char.isdigit())

        upiNumber.delete(0, 'end')
        upiNumber.insert(0, upi_number_digits)

    upiLabel = ctk.CTkLabel(tabs.tab(frame), text="{}".format(type), font=('Poppins Bold', 27), text_color="#000")
    upiLabel.grid(row=2, column=0, pady=(20, 0), padx=(360, 0), sticky="w")

    upiNumber = ctk.CTkEntry(master=tabs.tab(frame) ,placeholder_text=f"UPI NO / Contact No.", width=450, font=('Inter', 22), corner_radius=8, border_color="#000", fg_color="#fff", border_width=1, height=40, text_color="#000")
    upiNumber.grid(row=3, column=0, sticky="w", padx=(20,0) , pady=(20, 0))
    upiNumber.bind("<KeyRelease>", format_upi_number)

    finalFair = ctk.CTkLabel(tabs.tab(frame), text=f"Amount Payable: {get_selected_fair()} ", font=('Poppins Bold', 20), text_color="#000")
    finalFair.grid(row=6, column=0, pady=(20, 0), padx=(20, 0), sticky="w")

    payButton = ctk.CTkButton(tabs.tab(frame), text="Pay",fg_color="#5790DF" ,text_color="white", font=('Inter', 18), corner_radius=25, width=120, height=40, command=validate_payment)
    payButton.grid(row=7, column=0, pady=(20, 50), padx=(20,0), sticky="w")
    

    error_label = ctk.CTkLabel(tabs.tab(frame), text="", text_color="red",  font=('Inter', 15))
    error_label.grid(row=8, column=0, pady=(0, 0), padx=(250,0)) 
# Debit Card Tab 
root.mainloop()
