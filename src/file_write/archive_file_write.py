import os
from struct import pack
from model.TDateTime import TDateTime
from model.logger import logger
from shutil import copy2

def archive_file_write(
    folder_path,
    default_folder_path,
    header_text,
    current_values,
    changed_values,
    current_time,
    is_new_hour,
    is_new_day,
    BLOCK_NUMBER,
    number_of_all_values=200000,
    number_of_analog_values=20000,
    copy_file = False
):
    try:
        file_name_archive = (f"{current_time.strftime("%Y%m%d")}.VO{BLOCK_NUMBER}")
        # file_name_archive = (
        #     f"{current_time.year}{current_time.month}{current_time.day}.VO{BLOCK_NUMBER}"
        # )
        if copy_file:
            default_archive_file_path = os.path.join(default_folder_path, file_name_archive)
            if not os.path.isdir(default_folder_path):
                os.makedirs(default_folder_path, exist_ok=True) 
        archive_file_path = os.path.join(folder_path, file_name_archive)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            logger.log("archive:\tfolder created")
            
        if copy_file:
            if not os.path.isfile(default_archive_file_path):
                with open(default_archive_file_path, "wb+") as archive_file:
                    logger.log("archive:\tfile created")
                    write_header_to_archive_file(
                        archive_file,
                        header_text,
                        current_time,
                        number_of_all_values,
                        number_of_analog_values,
                )
                copy2(default_archive_file_path, archive_file_path)
        else:
            if not os.path.isfile(archive_file_path):
                with open(archive_file_path, "wb+") as archive_file:
                    logger.log("archive:\tfile created")
                    write_header_to_archive_file(
                        archive_file,
                        header_text,
                        current_time,
                        number_of_all_values,
                        number_of_analog_values,
                )
    except Exception as exception:
        logger.log(f"error:\tarchvie file creation: {exception}")

    try:
        if copy_file:
            with open(default_archive_file_path, "rb+") as archive_file:
                current_cursor_position = os.path.getsize(archive_file_path)  # + 1
                set_header_time_of_archive_file(
                    archive_file, current_time, current_cursor_position
                )
                if is_new_hour or is_new_day:
                    set_hour_photo_index_in_header(
                        archive_file, current_cursor_position, current_time.hour
                    )
                    write_photo_of_all_parameters(archive_file, current_values, current_time)
                elif len(changed_values) > 10000:
                    write_photo_of_all_parameters(archive_file, current_values, current_time)
                elif len(changed_values) > 0:
                    write_array_of_changed_parameters(
                        archive_file, changed_values, current_time
                    )
                else:
                    logger.log("archive:\tfile not change" , debug = True)
            copy2(default_archive_file_path, archive_file_path)
        else:
            with open(archive_file_path, "rb+") as archive_file:
                current_cursor_position = os.path.getsize(archive_file_path)  # + 1
                set_header_time_of_archive_file(
                    archive_file, current_time, current_cursor_position
                )
                if is_new_hour or is_new_day:
                    set_hour_photo_index_in_header(
                        archive_file, current_cursor_position, current_time.hour
                    )
                    write_photo_of_all_parameters(archive_file, current_values, current_time)
                elif len(changed_values) > 10000:
                    write_photo_of_all_parameters(archive_file, current_values, current_time)
                elif len(changed_values) > 0:
                    write_array_of_changed_parameters(
                        archive_file, changed_values, current_time
                    )
                else:
                    logger.log("archive:\tfile not change" , debug = True)
    except Exception as exception:
        logger.log(f"error:\tarchvie file writing: {exception}")

def write_header_to_archive_file(
    archive_file,
    header_text,
    current_time,
    number_of_all_values,
    number_of_analog_values,
):
    try:
        length_of_one_value = 5
        size_of_all_parameters_photo = number_of_all_values * length_of_one_value
        size_of_analog_values_photo = number_of_analog_values * length_of_one_value
        archive_file.write(header_text.encode())
        archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
        archive_file.write(b"\xff\xff\xff\xff" * 24)
        archive_file.write(pack("<i", size_of_all_parameters_photo))
        archive_file.write(pack("<i", size_of_analog_values_photo))
        logger.log("archive:\theader written", debug = True)
    except Exception as exception:
        logger.log(f"error:\tarchive header writing: {exception}")


def set_header_time_of_archive_file(
    archive_file, current_time, current_cursor_position
):
    try:
        archive_file.seek(16)
        archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
        archive_file.seek(current_cursor_position)
        logger.log("archive:\theader time written", debug = True)
    except Exception as exception:
        logger.log(f"error: archive file time writing: {exception}")


def set_hour_photo_index_in_header(
    archive_file, current_cursor_position, current_time_hour
):
    try:
        archive_file.seek(24 + 4 * current_time_hour)
        archive_file.write(pack("<i", current_cursor_position))
        archive_file.seek(current_cursor_position)
        logger.log("archive:\thour index added", debug = True)
    except Exception as exception:
        logger.log(f"error:\tarchive file header writing: {exception}")


def write_photo_of_all_parameters(archive_file, current_values, current_time):
    try:
        archive_file.write(b"\x00")
        archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
        for value_number in current_values:
            archive_file.write(current_values[value_number]["Value"])
            archive_file.write(current_values[value_number]["Signal"])
        logger.log("archive:\thour photo")
    except Exception as exception:
        logger.log(f"error:\tarchive hour photo writing: {exception}")

def write_array_of_changed_parameters(archive_file, changed_values, current_time):
    try:
        archive_file.write(b"\x01")
        archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
        archive_file.write(pack("<i", len(changed_values)))
        for value in changed_values:
            archive_file.write(pack("<i", value["Number"]))
            archive_file.write(value["Value"])
            archive_file.write(value["Signal"])
        logger.log(f"archive:\t{len(changed_values)} changed_parameters", debug = True)
    except Exception as exception:
        logger.log(f"error:\tarchive changed_parameters writing: {exception}")
