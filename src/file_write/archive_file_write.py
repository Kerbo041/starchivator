import os
from struct import pack
from model.TDateTime import TDateTime
from model.logger import logger


def archive_file_write(
    folder_path,
    header_text,
    current_values,
    changed_values,
    current_time,
    is_new_hour,
    is_new_day,
    BLOCK_NUMBER,
    number_of_all_values=200000,
    number_of_analog_values=20000
):
    file_name_archive = (
        f"{current_time.year}{current_time.month}{current_time.day}.VO{BLOCK_NUMBER}"
    )
    archive_file_path = os.path.join(folder_path, file_name_archive)
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        logger.debug_log("archive folder created")
    if not os.path.isfile(archive_file_path):
        with open(archive_file_path, "wb+") as archive_file:
            logger.any_log("archive file created")
            write_header_to_archive_file(
                archive_file,
                header_text,
                current_time,
                number_of_all_values,
                number_of_analog_values,
            )
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


def write_header_to_archive_file(
    archive_file,
    header_text,
    current_time,
    number_of_all_values,
    number_of_analog_values,
):
    length_of_one_value = 5
    size_of_all_parameters_photo = number_of_all_values * length_of_one_value
    size_of_analog_values_photo = number_of_analog_values * length_of_one_value
    archive_file.write(header_text.encode())
    archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
    archive_file.write(b"\xff\xff\xff\xff" * 24)
    archive_file.write(pack("<i", size_of_all_parameters_photo))
    archive_file.write(pack("<i", size_of_analog_values_photo))
    logger.debug_log("archive header written")


def set_header_time_of_archive_file(
    archive_file, current_time, current_cursor_position
):
    archive_file.seek(16)
    archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
    archive_file.seek(current_cursor_position)
    logger.debug_log("archive header time written")


def set_hour_photo_index_in_header(
    archive_file, current_cursor_position, current_time_hour
):
    archive_file.seek(24 + 4 * current_time_hour)
    archive_file.write(pack("<i", current_cursor_position))
    archive_file.seek(current_cursor_position)
    logger.debug_log("archive hour index added")


def write_photo_of_all_parameters(archive_file, current_values, current_time):
    archive_file.write(b"\x00")
    archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
    for value_number in current_values:
        archive_file.write(current_values[value_number]["Value"])
        archive_file.write(current_values[value_number]["Signal"])
    logger.debug_log("archived photo of all parameters")


def write_array_of_changed_parameters(archive_file, changed_values, current_time):
    archive_file.write(b"\x01")
    archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
    archive_file.write(pack("<i", len(changed_values)))
    for value in changed_values:
        archive_file.write(pack("<i", value["Number"]))
        archive_file.write(value["Value"])
        archive_file.write(value["Signal"])
    logger.debug_log(f"archived {len(changed_values)} changed_parameters")
