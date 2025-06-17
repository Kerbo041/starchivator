import os
from struct import pack
from model.TDateTime import TDateTime
from model.Logger import Logger
from model.Config import Config
from datetime import datetime, timedelta
from model.TechnologicalParametersArray import TechnologicalParametersArray
from model.TechnologicalParameter import TechnologicalParameter
from model.BufferArray import BufferArray


def check_old_archives(config: Config, logger: Logger):
    max_archive_file_age = 7
    for archive_file_name in os.listdir(config.file_paths.path_arc_folder):
        try:
            try:
                archive_file_date = datetime.strptime(archive_file_name, "%Y%m%d.VO3")
            except:
                continue
            archive_file_timedelta = (datetime.now() - archive_file_date) / timedelta(
                days=1
            )
            if archive_file_timedelta > max_archive_file_age:
                os.remove(
                    os.path.join(config.file_paths.path_arc_folder, archive_file_name)
                )
        except Exception as exception:
            logger.log(exception)


def archive_file_write(
    current_parameters_array: TechnologicalParametersArray,
    buffer_parameters_array: BufferArray,
    config: Config,
    logger: Logger,
):
    old_current_time = buffer_parameters_array.get_time()
    buffer_parameters_array.set_time()
    current_time = datetime.now()
    if old_current_time.hour != current_time.hour:
        is_new_hour = True
    else:
        is_new_hour = False
    if old_current_time.day != current_time.day:
        is_new_day = True
        check_old_archives(config, logger)
    else:
        is_new_day = False

    try:
        file_name_archive = f"{current_time.strftime("%Y%m%d")}.VO{config.program_parameters.block_number}"
        # file_name_archive = (
        #     f"{current_time.year}{current_time.month}{current_time.day}.VO{BLOCK_NUMBER}"
        # )
        archive_file_path = os.path.join(
            config.file_paths.path_arc_folder, file_name_archive
        )
        if not os.path.isdir(config.file_paths.path_arc_folder):
            os.makedirs(config.file_paths.path_arc_folder, exist_ok=True)
            logger.log("archive:\tfolder created")
        if not os.path.isfile(archive_file_path):
            with open(archive_file_path, "wb+") as archive_file:
                logger.log("archive:\tfile created")
                write_header_to_archive_file(
                    archive_file,
                    config.header_texts.archive,
                    current_time,
                    config.program_parameters.total_number_of_values,
                    config.program_parameters.total_number_of_analog_values,
                    logger
                )
    except Exception as exception:
        logger.log(f"error:\tarchvie file creation: {exception}")

    try:
        with open(archive_file_path, "rb+") as archive_file:
            current_cursor_position = os.path.getsize(archive_file_path)  # + 1
            set_header_time_of_archive_file(
                archive_file, current_time, current_cursor_position, logger
            )
            if is_new_hour or is_new_day:
                set_hour_photo_index_in_header(
                    archive_file, current_cursor_position, current_time.hour, logger
                )
                write_photo_of_all_parameters(
                    archive_file,
                    current_parameters_array.parameters_array,
                    current_time,
                    logger
                )
            elif buffer_parameters_array.buffer_length > 10000:
                write_photo_of_all_parameters(
                    archive_file,
                    current_parameters_array.parameters_array,
                    current_time,
                    logger
                )
            elif buffer_parameters_array.buffer_length > 0:
                write_array_of_changed_parameters(
                    archive_file,
                    buffer_parameters_array.buffer_array,
                    current_time,
                    logger
                )
            else:
                logger.log("archive:\tfile not change", debug=True)
    except Exception as exception:
        logger.log(f"error:\tarchvie file writing: {exception}")


def write_header_to_archive_file(
    archive_file,
    header_text,
    current_time,
    number_of_all_values,
    number_of_analog_values,
    logger: Logger
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
        logger.log("archive:\theader written", debug=True)
    except Exception as exception:
        logger.log(f"error:\tarchive header writing: {exception}")


def set_header_time_of_archive_file(
    archive_file, current_time, current_cursor_position, logger: Logger
):
    try:
        archive_file.seek(16)
        archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
        archive_file.seek(current_cursor_position)
        logger.log("archive:\theader time written", debug=True)
    except Exception as exception:
        logger.log(f"error: archive file time writing: {exception}")


def set_hour_photo_index_in_header(
    archive_file, current_cursor_position, current_time_hour, logger: Logger
):
    try:
        archive_file.seek(24 + 4 * current_time_hour)
        archive_file.write(pack("<i", current_cursor_position))
        archive_file.seek(current_cursor_position)
        logger.log("archive:\thour index added", debug=True)
    except Exception as exception:
        logger.log(f"error:\tarchive file header writing: {exception}")


def write_photo_of_all_parameters(
    archive_file, current_values, current_time, logger: Logger
):
    try:
        archive_file.write(b"\x00")
        archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
        for paramater in current_values:
            if type(paramater) == TechnologicalParameter:
                archive_file.write(paramater.get_value())
                archive_file.write(paramater.get_signal())
        logger.log("archive:\thour photo")
    except Exception as exception:
        logger.log(f"error:\tarchive hour photo writing: {exception}")


def write_array_of_changed_parameters(
    archive_file, changed_values, current_time, logger: Logger
):
    try:
        archive_file.write(b"\x01")
        archive_file.write(pack("<d", TDateTime.datetime_to_tdatetime(current_time)))
        archive_file.write(pack("<i", len(changed_values)))
        for paramater in changed_values:
            if type(paramater) == TechnologicalParameter:
                archive_file.write(pack("<i", paramater.get_number()))
                archive_file.write(paramater.get_value())
                archive_file.write(paramater.get_signal())
        logger.log(f"archive:\t{len(changed_values)} changed_parameters", debug=True)
    except Exception as exception:
        logger.log(f"error:\tarchive changed_parameters writing: {exception}")
