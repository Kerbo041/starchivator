from tkinter import *
from tkinter import ttk


root = Tk()
root.title("decoder")
root.geometry("400x100") 

# декодирование числа
label_int_entry = ttk.Label()
label_int_entry.grid(row=1, column=1)
label_int_entry["text"] = "введите целочисленное число"

entry_int = ttk.Entry()
entry_int.grid(row=1, column=2)

label_int = ttk.Label()
label_int.grid(row=2, column=2)

btn_int = ttk.Button(text="Int decode")
btn_int.grid(row=2, column=1)

#
label_data_entry = ttk.Label()
label_data_entry.grid(row=3, column=1)
label_data_entry["text"] = "введите дату"

entry_data = ttk.Entry()
entry_data.grid(row=3, column=2)

btn_date = ttk.Button(text="date")
btn_date.grid(row=4, column=1)

label_date = ttk.Label()
label_date.grid(row=4, column=2)

root.mainloop()