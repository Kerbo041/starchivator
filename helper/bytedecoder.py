from tkinter import *
from tkinter import ttk
from struct import unpack
from datetime import datetime, timedelta

def decode_int_bytes(entered_string):
    data = bytes.fromhex(entered_string.replace(" ", ""))
    return unpack("<i", data)

def show_int():
    label_int["text"] = decode_int_bytes(entry_int.get())     # получаем введенный текст

def decode_date_bytes(entered_string):
    return tdatetime_to_datetime(bytes.fromhex(entered_string.replace(" ", "")))

def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
    tdatetime = unpack("<d", tdatetime_in_bytes)[0]
    return datetime(1899, 12, 30) + timedelta(days=tdatetime)

def show_date():
    label_date["text"] = decode_date_bytes(entry_data.get())     # получаем введенный текст

root = Tk()
root.title("METANIT.COM")
root.geometry("400x100") 

# декодирование числа
label_int_entry = ttk.Label()
label_int_entry.grid(row=1, column=1)
label_int_entry["text"] = "введите целочисленное число"

entry_int = ttk.Entry()
entry_int.grid(row=1, column=2)

label_int = ttk.Label()
label_int.grid(row=2, column=2)

btn_int = ttk.Button(text="Int decode", command=show_int)
btn_int.grid(row=2, column=1)

#
label_data_entry = ttk.Label()
label_data_entry.grid(row=3, column=1)
label_data_entry["text"] = "введите дату"

entry_data = ttk.Entry()
entry_data.grid(row=3, column=2)

btn_date = ttk.Button(text="date", command=show_date)
btn_date.grid(row=4, column=1)

label_date = ttk.Label()
label_date.grid(row=4, column=2)

root.mainloop()