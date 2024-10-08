☆Этот скрипт разбирает строки
из лог-файла, извлекает информацию
о запросах (IP-адрес, время, код 
состояния, запрошенный URL и User-Agent)
и создает DataFrame. Вы можете дополнить
его, чтобы сохранять найденные строки в 
файл /var/log/nginx/parsed/lines.txt и 
выполнять ротацию, если размер файла 
превышает 2006 строк.

●Описание работы программы:

■Функция rotate_files:
Проверяет наличие 
ротационных файлов (lines.txt.1, lines.
txt.2 и т.д.).Переименовывает текущий 
файл lines.txt в следующий по очереди.

■Функция parse_logs:
Проходит по всем лог-файлам в директории
/var/log/nginx, включая ротационные файлы
(access.log, access.log.1, access.log.2 и т.д.).
Ищет строки, соответствующие заданной маске (pattern)
.Записывает найденные строки в файл lines.txt.
При достижении размера файла 200 КБ происходит ротация
файла.

■Основная часть программы:
Задает маску для поиска ("favicon.ico") и вызывает функцию
parse_logs.Программа будет последовательно искать строки,
удовлетворяющие условию, и записывать их в файл с учетом 
ограничения по размеру.
●Описание работы:

◇Функция get_log_files:Возвращает список лог-файлов из указанной директории.

◇Функция read_lines_from_file:Читает строки из лог-файла и возвращает их в виде генератора.

◇Функция filter_lines:Принимает регулярное выражение и генератор строк, возвращает только те строки, которые соответствуют шаблону.

◇Функция write_lines_to_file:Записывает строки в файл и производит ротацию при достижении заданного размера файла (200 КБ по умолчанию).

◇Функция parse_logs:Является основной функцией, которая соединяет все остальные. Она последовательно:Получает лог-файлы от data_source.Читает строки из каждого файла.Применяет фильтр к строкам.Записывает отфильтрованные строки в файл через storage_func.

■Гибкость подхода:"data_source может быть заменен на любую другую функцию, которая возвращает строки, например, данные из сети или базы данных.filter_func также можно заменить на другую функцию, если необходимо реализовать другую логику фильтрации.storage_func может быть заменен на любую функцию, которая сохраняет данные, например, отправляет их в базу данных или по сети.Такой подход позволяет легко изменять функциональность программы без необходимости переписывать основную логику, и код становится более читаемым и поддерживаемым."
