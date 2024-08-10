import os
import re
from glob import glob

# Путь к директории с лог-файлами Nginx
log_dir = "/var/log/nginx"
parsed_dir = "/var/log/nginx/parsed"
output_file = os.path.join(parsed_dir, "lines.txt")
max_size = 200 * 1024  # 200 КБ

# Функция для ротации файлов
def rotate_files():
    index = 1
    while os.path.exists(f"{output_file}.{index}"):
        index += 1
    os.rename(output_file, f"{output_file}.{index}")

# Функция для поиска и записи строк по маске
def parse_logs(pattern):
    # Создаем директорию для парсенных файлов, если ее нет
    os.makedirs(parsed_dir, exist_ok=True)

    # Открываем файл для записи найденных строк
    with open(output_file, "a") as output:
        # Проходим по всем лог-файлам
        for log_file in sorted(glob(os.path.join(log_dir, "access.log*")), reverse=True):
            with open(log_file, "r") as f:
                for line in f:
                    if re.search(pattern, line):
                        output.write(line)
                        
                        # Если размер файла превышает лимит, ротация
                        if output.tell() >= max_size:
                            output.close()
                            rotate_files()
                            output = open(output_file, "a")

# Пример использования функции с маской "favicon.ico"
if __name__ == "__main__":
    parse_logs("favicon.ico")