from misc.misc import *

def connect_values(analog_values, discrete_values):
    values_set = []
    for i in analog_values:
        values_set.append(i)
    length_analog_empty = 20000 - len(analog_values)
    empty_analog = [b"\xff"*17 for i in range(length_analog_empty)]
    for i in empty_analog:
        values_set.append(i)
        
    for i in discrete_values:
        values_set.append(i)
    length_discrete_empty = 180000 - len(discrete_values)
    empty_discrete = [b"\xff"*17 for i in range(length_discrete_empty)]
    for i in empty_discrete:
        values_set.append(i)
    return values_set

def apply_analog_and_discrets(analog_values, discrete_values, outdat_values):
    values_set = connect_values(analog_values, discrete_values)
    
    with open("D:\\work\\test.txt", "w") as f:
        print(f"analog values: {len(analog_values)}, discrete values: {len(discrete_values)}", file = f)
        for i in range(len(outdat_values)):
            print(i, file = f, end = "\t")
            try:
                print("outdat:\t", end="", file=f)
                print_byte_line(outdat_values[i], f)
            except:
                print("no outdat", end="", file=f)
            print("\t", end="", file = f)
            try:
                print("out_0_1:\t", end="", file=f)
                print_byte_line((values_set[i][12:17:]), f)
            except:
                print("no values", file=f, end = "")
            print("\t", end="", file = f)
            try:
                if outdat_values[i] == (values_set[i][12:17:]):
                    print("YES", file = f)
                else:
                    print("NO", file = f)
            except:
                print("NO", file = f)
                
                
def check_x_file(analog_values, discrete_values, out_dat_values, x_dat_values):
    values_set = connect_values(analog_values, discrete_values)
    