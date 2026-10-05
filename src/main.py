import json
import sys
from datetime import datetime
from pathlib import Path

import starchivator
from model.logger import logger

BLOCK_NUMBER = 3
TOTAL_PARAMETER_COUNT = 200_000
EMPTY_VALUE = b"\xff\xff\xff\xff"
EMPTY_SIGNAL = b"\xff"

REQUIRED_PATH_KEYS = (
    "Path_out_dat",
    "Path_x_dat",
    "Path_out_0",
    "Path_out_1",
    "Path_arc_folder",
)

REQUIRED_HEADER_KEYS = (
    "OutDat",
    "XDat",
    "Archive",
)

REQUIRED_LOG_KEYS = (
    "console_logging_enabled",
    "file_logging_enabled",
    "debug_logging_enabled",
    "Path_log_folder_path",
)


def get_config_path() -> Path:
    """
    Возвращает путь к конфигурации.

    Если передан аргумент командной строки — используем его.
    Иначе используем config.json рядом с main.py.
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    return Path(__file__).resolve().parent / "config.json"


def load_config(config_path: Path) -> dict:
    """Читает JSON-конфигурацию."""
    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}", file=sys.stderr)
        raise SystemExit(1)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {config_path}: {exc}", file=sys.stderr)
        raise SystemExit(1)


def validate_config(config: dict) -> None:
    """Проверяет обязательные секции и ключи конфигурации."""
    for section in ("Paths", "HeaderTexts", "Logs"):
        if section not in config:
            raise SystemExit(f"Config section '{section}' not found")

    missing_paths = [
        key
        for key in REQUIRED_PATH_KEYS
        if key not in config["Paths"]
    ]
    if missing_paths:
        raise SystemExit(f"Missing Paths keys: {', '.join(missing_paths)}")

    missing_headers = [
        key
        for key in REQUIRED_HEADER_KEYS
        if key not in config["HeaderTexts"]
    ]
    if missing_headers:
        raise SystemExit(f"Missing HeaderTexts keys: {', '.join(missing_headers)}")

    missing_logs = [
        key
        for key in REQUIRED_LOG_KEYS
        if key not in config["Logs"]
    ]
    if missing_logs:
        raise SystemExit(f"Missing Logs keys: {', '.join(missing_logs)}")


def make_default_paths(paths_config: dict) -> dict:
    """
    Добавляет служебные DefaultPath_*.

    Они используются только если включено копирование файлов.
    """
    script_dir = Path(__file__).resolve().parent
    files_dir = script_dir / "files"

    paths = dict(paths_config)

    paths.update(
        {
            "DefaultPath_out_dat": str(files_dir / "out.dat"),
            "DefaultPath_x_dat": str(files_dir / "x.dat"),
            "DefaultPath_out_0": str(files_dir / "out.0"),
            "DefaultPath_out_1": str(files_dir / "out.1"),
            "DefaultPath_arc_folder": str(files_dir / "arc"),
        }
    )

    return paths


def make_initial_values() -> dict:
    """Создает начальное состояние всех параметров."""
    return {
        i: {
            "Value": EMPTY_VALUE,
            "Signal": EMPTY_SIGNAL,
            "Status": False,
        }
        for i in range(TOTAL_PARAMETER_COUNT)
    }


def working(config_path: Path) -> None:
    """Основной рабочий цикл."""
    config = load_config(config_path)
    validate_config(config)

    file_paths = make_default_paths(config["Paths"])
    headers = config["HeaderTexts"]
    log_config = config["Logs"]

    logger.set_log_config(log_config)
    logger.log(f"Starting starchivator, config: {config_path}")

    current_time = datetime(1, 1, 1)
    special_buffer_signal = 0
    current_parameter_index = 0
    current_values = make_initial_values()
    array_of_buffered_parameters = {}
    old_total_number_of_values = 0

    while True:
        (
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            old_total_number_of_values,
        ) = starchivator.do_archivation_iteration(
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            file_paths,
            headers,
            BLOCK_NUMBER,
            old_total_number_of_values,
        )


def main() -> None:
    try:
        working(get_config_path())
    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    main()