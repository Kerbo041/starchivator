

def reader_db_a(db_path):
    db_file = open(db_path, "r")
    db_values = []
    for line in db_file.readlines():
        line_splited = line.split(";")
        db_values.append(
            {
                "number": int(line_splited[0]),
                "min": float(line_splited[2]),
                "max": float(line_splited[3]),
            }
        )
    return db_values


def reader_db_d(db_path):
    fin = open(db_path, "r")
    db_values = []
    for line in fin.readlines():
        line_splited = line.split(";")
        db_values.append(
            {
                "number": int(line_splited[0]), 
                "length": int(line_splited[1])}
        )
    return db_values