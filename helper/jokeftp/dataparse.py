import asyncio
import time
from pynput.keyboard import Listener, Key
from pynput import keyboard

db_a_path = "C:\\spd3\\sg3\\DB_A.CSV"

def reader_db_a(db_a_path):
    
    fin = open(db_a_path, "r")
    values = []
    for line in fin.readlines():
        line_splited = line.split(";")
        values.append(
            {
                "номер": line_splited[0],
                "min": line_splited[2],
                "max": line_splited[3]
                }
            )
    return values


values = reader_db_a(db_a_path)

def 