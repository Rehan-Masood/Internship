from tkinter import *

def miles_to_km():
    miles = float(miles_input.get())
    km = miles * 1.609
    kilometer_result_label.config(text=f"{km:.2f}")

window = Tk()
window.title("Mile to Km Converter")
window.geometry("500x350") 

content_frame = Frame(window)
content_frame.place(relx=0.5, rely=0.5, anchor="center")

# ----------------- Input Field -----------------
miles_input = Entry(content_frame, width=7)
miles_input.grid(column=1, row=0, padx=10, pady=10)

# ----------------- Labels -----------------
miles_label = Label(content_frame, text="Miles")
miles_label.grid(column=2, row=0)

is_equal_label = Label(content_frame, text="is equal to")
is_equal_label.grid(column=0, row=1)

kilometer_result_label = Label(content_frame, text="0")
kilometer_result_label.grid(column=1, row=1)

km_label = Label(content_frame, text="Km")
km_label.grid(column=2, row=1)

# ----------------- Calculate Button -----------------
calculate_button = Button(content_frame, text="Calculate", command=miles_to_km)
calculate_button.grid(column=1, row=2, pady=10)

window.mainloop()