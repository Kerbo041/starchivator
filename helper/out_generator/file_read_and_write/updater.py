import file_read_and_write.bytecoder as bytecoder


def write_new_values(write_path, byte_values, start_byte):
    with open(write_path, "rb+") as wf:
        wf.seek(start_byte * 17)
        for value in byte_values:
            wf.write(value)
