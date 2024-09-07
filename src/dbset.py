dba_path = "DB_A.CSV"
dbd_path = "DB_D.CSV"

import random
def choose():
    if random.randint(0,1) == 0:
        return 1
    else:
        return 16

def fill_dba(dba_path, number_of_values):
    f_dba = open(dba_path, "w")
    for i in range(number_of_values):
        print(f"{i};{0};{1000}",file = f_dba)
    f_dba.close()
    
def fill_dbd(dbd_path, number_of_values):
    f_dbd = open(dbd_path, "w")
    for i in range(number_of_values):
        print(f"{i};{choose()}",file = f_dbd)
    f_dbd.close()

fill_dba(dba_path, 100000)

fill_dbd(dbd_path, 100000)