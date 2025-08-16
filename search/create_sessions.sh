#!/bin/bash

# Путь к директории с файлами credentials
CREDENTIALS_DIR="./credentials"
SESSIONS_DIR="./sessions"

# Путь к исполняемому файлу Python
PYTHON_SCRIPT="create_session.py"

# Проверяем, существует ли директория с credentials
if [ ! -d "$CREDENTIALS_DIR" ]; then
  echo "Директория с credentials не найдена: $CREDENTIALS_DIR"
  exit 1
fi

# Проверяем, существует ли исполняемый файл Python
if [ ! -x "$PYTHON_SCRIPT" ]; then
  echo "Исполняемый файл Python не найден или недостаточно прав: $PYTHON_SCRIPT"
  exit 1
fi

# Перебираем файлы в директории credentials и запускаем Python-скрипт с каждым из них
for file in "$CREDENTIALS_DIR"/*.json; do
  if [ -f "$file" ]; then
    # Получаем имя файла без расширения
    filename=$(basename -- "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"
    
    # Формируем имя выходного файла
    output_file="$SESSIONS_DIR/$filename.pickle"
    
    echo "Запуск Python-скрипта с параметрами: $file -o $output_file"
    echo -e "\n"
    python3 "$PYTHON_SCRIPT" "$file" -o "$output_file"
  fi
done

exit 0