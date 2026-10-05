#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт собирает все текстовые файлы проекта в один bundle-файл.
Удобно для отправки кода нейросети одним файлом.

Использование:
    python pack_project.py [путь_к_проекту] [имя_выходного_файла]

По умолчанию:
    путь_к_проекту = текущая папка
    имя_выходного_файла = project_bundle.txt
"""
import os
import sys
from pathlib import Path

# Папки, которые нужно игнорировать
IGNORE_DIRS = {
    '.git', '__pycache__', '.venv', 'venv', 'env',
    '.idea', '.vscode', 'node_modules', 'dist', 'build',
    '.pytest_cache', '.mypy_cache', '.tox',
}

# Расширения бинарных файлов, которые не нужно включать
IGNORE_EXTENSIONS = {
    '.dat', '.bin', '.exe', '.dll', '.so', '.dylib',
    '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar',
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.pyc', '.pyo', '.whl', '.egg',
    '.db', '.sqlite', '.sqlite3', '.txt',
}

# Максимальный размер файла для включения (1 МБ)
MAX_FILE_SIZE = 1 * 1024 * 1024


def should_include(path: Path) -> bool:
    """Проверяет, нужно ли включать файл в бандл."""
    # Игнорируем сам bundle-файл и этот скрипт
    if path.name in ('project_bundle.txt', 'pack_project.py'):
        return False

    # Проверяем размер
    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return False
    except OSError:
        return False

    # Проверяем расширение
    if path.suffix.lower() in IGNORE_EXTENSIONS:
        return False

    # Пытаемся прочитать как текст — если не получается, пропускаем
    try:
        with open(path, 'r', encoding='utf-8', errors='strict') as f:
            f.read(1024)
        return True
    except (UnicodeDecodeError, OSError):
        # Пробуем cp1251 для старых файлов
        try:
            with open(path, 'r', encoding='cp1251', errors='strict') as f:
                f.read(1024)
            return True
        except (UnicodeDecodeError, OSError):
            return False


def collect_files(root: Path) -> list[Path]:
    """Рекурсивно собирает все подходящие файлы."""
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_file():
            # Проверяем, нет ли в пути игнорируемой папки
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            if should_include(path):
                result.append(path)
    return result


def build_bundle(root: Path, output: Path) -> None:
    """Собирает все файлы в один bundle."""
    files = collect_files(root)
    
    with open(output, 'w', encoding='utf-8') as out:
        out.write(f"# Project Bundle\n")
        out.write(f"# Root: {root.resolve()}\n")
        out.write(f"# Files: {len(files)}\n")
        out.write(f"# {'=' * 70}\n\n")

        for file_path in files:
            rel_path = file_path.relative_to(root)
            size = file_path.stat().st_size
            
            # Определяем кодировку
            encoding = 'utf-8'
            try:
                with open(file_path, 'r', encoding='utf-8', errors='strict') as f:
                    content = f.read()
            except UnicodeDecodeError:
                encoding = 'cp1251'
                with open(file_path, 'r', encoding='cp1251', errors='replace') as f:
                    content = f.read()

            out.write(f"## File: {rel_path}\n")
            out.write(f"## Size: {size} bytes | Encoding: {encoding}\n")
            out.write(f"## {'=' * 70}\n\n")
            out.write(content)
            out.write(f"\n\n## {'=' * 70}\n\n")

    total_size = output.stat().st_size
    print(f"Bundle создан: {output}")
    print(f"Файлов включено: {len(files)}")
    print(f"Размер bundle: {total_size / 1024:.1f} КБ")


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('project_bundle.txt')

    if not root.exists():
        print(f"Ошибка: папка {root} не существует")
        sys.exit(1)

    print(f"Сборка проекта из: {root.resolve()}")
    print(f"Игнорируемые папки: {', '.join(sorted(IGNORE_DIRS))}")
    print(f"Игнорируемые расширения: {', '.join(sorted(IGNORE_EXTENSIONS))}")
    print()

    build_bundle(root, output)


if __name__ == '__main__':
    main()