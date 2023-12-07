from tkinter import font
import customtkinter as ctk
from screeninfo import get_monitors
import ttkbootstrap as ttk
root = ctk.CTk()

resoultion = get_monitors()[0]
screenWidth = resoultion.width
screenHeight = resoultion.height


root.geometry(f"{screenWidth}x{screenHeight}")
root.title("Payment")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

payment = ctk.CTkFrame(master=root, fg_color="white", border_color="#fff", border_width=2, corner_radius=10)
payment.grid(row=1, column=1, sticky="nsew", padx=(15, 15), pady=20)





paymentLabel = ctk.CTkLabel(payment, text="Payment", font=('Poppins Bold', 30), text_color="#000")
paymentLabel.grid(row=0, column=0, pady=(20, 0), padx=(20, 0), sticky="nsew")
notebook = ttk.Notebook(payment)
notebook.grid(pady=10)

# create frames
frame1 = ttk.Frame(notebook, width=400, height=280)
frame2 = ttk.Frame(notebook, width=400, height=280)

frame1.grid()
frame2.grid()

# add frames to notebook

notebook.add(frame1, text='General Information')
notebook.add(frame2, text='Profile')

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)



root.mainloop()