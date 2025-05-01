import os
import subprocess

ROOT_DIR = os.path.abspath(os.getcwd())
MAX_DEPTH = 2
EXCLUDED_FILES = ['project_summary.py']

def filter_file_content(filename):
    """Читает файл и возвращает его содержимое, исключая закомментированные строки."""
    filtered_lines = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.lstrip()
                if not stripped_line.startswith('#'):
                    filtered_lines.append(line.rstrip())
    except Exception as e:
        filtered_lines.append(f"# Ошибка чтения файла: {e}")
    return "\n".join(filtered_lines)

def find_valid_files(root_dir, extensions=['.py', '.ini']):
    """Ищет файлы с заданными расширениями в пределах указанной глубины, исключая заданные файлы."""
    valid_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        depth = dirpath[len(root_dir)+len(os.sep):].count(os.sep)
        if depth <= MAX_DEPTH:
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if ext.lower() in extensions and filename not in EXCLUDED_FILES:
                    valid_files.append(os.path.join(dirpath, filename))
    return valid_files

def main():
    # Получаем вывод команды tree -L 2
    tree_output = subprocess.check_output(["tree", "-L", str(MAX_DEPTH)], cwd=ROOT_DIR, text=True)
    
    # Собираем все подходящие файлы
    valid_files = find_valid_files(ROOT_DIR)
    
    # Чтение содержимого файлов
    contents = ["# Содержимое файлов:"]
    for file in sorted(valid_files):
        relative_path = os.path.relpath(file, ROOT_DIR)
        contents.append(f"\n# === {relative_path} ===")
        contents.append(filter_file_content(file))
    
    # Объединяем структуру и содержимое файлов
    final_result = f"# Структура проекта:\n{tree_output}\n{' '.join(contents)}"
    
    # Отправляем результат в буфер обмена
    subprocess.run(['xclip', '-selection', 'clipboard'], input=final_result.encode('utf-8'))

    print("✅ Структура и содержимое выбранных файлов скопированы в буфер обмена.")

if __name__ == "__main__":
    main()