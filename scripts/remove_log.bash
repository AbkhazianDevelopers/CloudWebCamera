#!/bin/bash

LOG_DIR="../data/logs/"

if [ -d "$LOG_DIR" ]; then
    # Удаляем все .log файлы в директории
    rm -f "$LOG_DIR"/*.log
    echo "Все .log файлы в директории $LOG_DIR были удалены."
else
    echo "Директория $LOG_DIR не существует."
fi
