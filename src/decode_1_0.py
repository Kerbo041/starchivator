read_path = "files/out.1"
desc_path = "decoded_files/out_one.txt"
# read_path = "files/out.0"
# desc_path = "decoded_files/out_zero.txt"


def read_line(file):
    new_portion_of_data = bytearray(file.read(17))
    if new_portion_of_data == b"":
        return None
    number = new_portion_of_data[0:4]
    data1 = new_portion_of_data[4:8]
    data2 = new_portion_of_data[8:12]
    data3 = new_portion_of_data[12:16]
    return {"number": number, "data1": data1, "data2": data2, "data3": data3}


if __name__ == "__main__":

    read_file = open(read_path, "rb")
    data = []
    while True:
        new_line = read_line(read_file)
        if new_line == None:
            break
        data.append(new_line)

    desc_file = open(desc_path, "w")
    for value in data:
        for key in value:
            line = ""
            for i in value[key]:
                line += (hex(i).replace("0x", ""))
                line += " "
            line += " \t"
            print(line, end="", file=desc_file)
        print("", file=desc_file)
    desc_file.close()
