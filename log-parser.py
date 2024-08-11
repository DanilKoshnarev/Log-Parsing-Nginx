import os
import re
from glob import glob

# Функция получения списка файлов из директории
def get_log_files(log_dir="/var/log/nginx"):
    return sorted(glob(os.path.join(log_dir, "access.log*")), reverse=True)

# Функция для чтения строк из лог-файла
def read_lines_from_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield line

# Функция для фильтрации строк на основе регулярного выражения
def filter_lines(pattern, lines):
    regex = re.compile(pattern)
    for line in lines:
        if regex.search(line):
            yield line

# Функция для записи строк в файл с ротацией по размеру
def write_lines_to_file(lines, output_dir="/var/log/nginx/parsed", max_size=200*1024):
    output_file = os.path.join(output_dir, "lines.txt")
    os.makedirs(output_dir, exist_ok=True)
    
    def rotate_files():
        index = 1
        while os.path.exists(f"{output_file}.{index}"):
            index += 1
        os.rename(output_file, f"{output_file}.{index}")
    
    with open(output_file, "a") as output:
        for line in lines:
            output.write(line)
            if output.tell() >= max_size:
                output.close()
                rotate_files()
                output = open(output_file, "a")

# Главная функция для обработки логов
def parse_logs(data_source, filter_func, storage_func):
    for log_file in data_source():
        lines = read_lines_from_file(log_file)
        filtered_lines = filter_func(lines)
        storage_func(filtered_lines)

# Пример использования с дефолтными функциями
if __name__ == "__main__":
    data_source = lambda: get_log_files("/var/log/nginx")
    filter_func = lambda lines: filter_lines("favicon.ico", lines)
    storage_func = lambda lines: write_lines_to_file(lines, "/var/log/nginx/parsed")

    parse_logs(data_source, filter_func, storage_func)