from tkinter import *
from tkinter import ttk
from json import load, dump
from codecoder import *
import os
from tkinter import *
from tkinter import ttk


def saveconfig():
    variant = variant_combobox.get()
    decs = desc_combobox.get()
    type = type_combobox.get()

    windows["save_window"] = Tk()
    windows["save_window"].title("Сохранение")
    windows["save_window"].geometry("250x200")
    entry_save = ttk.Entry()
    entry_save.grid()
    entry_save["text"] = "сохранить"
    create_save_button = ttk.Button(
        windows["save_window"], text="сохранение", command=save_new_config
    )


def save_new_config():
    save_name = entry_save.get()
    saveobj = {"save"}
    save_window.destroy()


def read_config():
    with open(
        os.path.dirname(os.path.abspath(__file__)) + "/savefile.json", "r"
    ) as savefile:
        save_data = load(savefile)
    return save_data


def config_load():
    pass


windows = {}
windows["root"] = Tk()
windows["root"].title("decoder")
windows["root"].geometry("400x100")
labels = {}
comboboxes = {}
entrys = {}
buttons = {}

saves = read_config()

# Выбор настроек
labels["label_config"] = ttk.Label()
labels["label_config"].grid(row=1, column=1)
labels["label_config"]["text"] = "варианты настроек"

config_all = [key for key in saves.keys()]
config_var = StringVar(value=config_all[0])

comboboxes["config_combobox"] = ttk.Combobox(
    textvariable=config_var, values=config_all, state="readonly"
)
comboboxes["config_combobox"].grid(row=1, column=2)

comboboxes["config_combobox"].bind("<<ComboboxSelected>>", config_load)

btn_save = ttk.Button(text="Сохранить настрйки", command=saveconfig)
btn_save.grid(row=1, column=3)

# Выбор системы измерения декодирования
labels["label_decode_var"] = ttk.Label()
labels["label_decode_var"].grid(row=2, column=1)
labels["label_decode_var"] = "выберите тип декодирования"

variant_of_decode = ["hex_to_dec", "dec_to_hex"]
variant_of_decode_var = StringVar(value=variant_of_decode[0])

variant_combobox = ttk.Combobox(
    textvariable=variant_of_decode_var, values=variant_of_decode, state="readonly"
)
variant_combobox.grid(row=2, column=2)


# Выбор типа декодирования
labels["label_decode_type"] = ttk.Label()
labels["label_decode_type"].grid(row=3, column=1)
labels["label_decode_type"]["text"] = "выберите тип данных"

types_of_decode = ["int", "double", "float", "char", "TDatetime"]
types_of_decode_var = StringVar(value=types_of_decode[0])

type_combobox = ttk.Combobox(
    textvariable=types_of_decode_var, values=types_of_decode, state="readonly"
)
type_combobox.grid(row=3, column=2)

# Выбор направления декодирования
labels["label_desc"] = ttk.Label()
labels["label_desc"].grid(row=4, column=1)
labels["label_desc"]["text"] = "введите дату"

destinations = ["little-endian", "big-endian"]
destination_var = StringVar(value=destinations[0])

desc_combobox = ttk.Combobox(
    textvariable=destination_var, values=destinations, state="readonly"
)
desc_combobox.grid(row=4, column=2)

# Декодирование
btn_date = ttk.Button(text="date", command=decode)
btn_date.grid(row=5, column=1)

# Результат
labels["label_data"] = ttk.Label()
labels["label_data"].grid(row=6, column=6)


windows["root"].mainloop()
