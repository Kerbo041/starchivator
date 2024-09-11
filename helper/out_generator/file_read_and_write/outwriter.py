
def outwriter(out_data, out_path):
    with open(out_path, "wb") as out_file:
        for line in out_data:
            out_file.write(line)
