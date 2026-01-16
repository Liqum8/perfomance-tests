#!/usr/bin/env python3
"""
Утилита для автоматического создания __init__.py файлов во всех Python пакетах.
Запускается автоматически через git hook или может быть вызвана вручную.
"""
import os
from pathlib import Path


def ensure_init_files(root_dir: str = ".") -> int:
    """
    Проверяет все папки в проекте и создает __init__.py файлы там, где их нет.
    
    Args:
        root_dir: Корневая директория проекта
        
    Returns:
        Количество созданных файлов
    """
    root = Path(root_dir).resolve()
    created_count = 0
    
    # Игнорируем эти директории
    ignore_dirs = {
        '__pycache__',
        '.git',
        'venv',
        'env',
        '.venv',
        'node_modules',
        '.pytest_cache',
        '.mypy_cache',
        'build',
        'dist',
        'scripts',  # Игнорируем папку со скриптами
        '*.egg-info'
    }
    
    # Рекурсивно обходим все директории
    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        
        # Пропускаем игнорируемые директории
        if any(ignore in dir_path.parts for ignore in ignore_dirs):
            continue
        
        # Проверяем, есть ли в этой директории Python файлы или поддиректории с Python файлами
        has_py_files = any(f.endswith('.py') for f in filenames)
        has_py_subdirs = any(
            (dir_path / d).is_dir() and 
            any((dir_path / d).rglob('*.py'))
            for d in dirnames
            if d not in ignore_dirs
        )
        
        # Если есть Python файлы или поддиректории с Python файлами, создаем __init__.py
        if (has_py_files or has_py_subdirs) and dir_path != root:
            init_file = dir_path / '__init__.py'
            if not init_file.exists():
                init_file.touch()
                print(f"Создан: {init_file.relative_to(root)}")
                created_count += 1
    
    return created_count


if __name__ == '__main__':
    import sys
    
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    count = ensure_init_files(root)
    
    if count > 0:
        print(f"\n[OK] Создано {count} файл(ов) __init__.py")
    else:
        print("[OK] Все __init__.py файлы на месте")
