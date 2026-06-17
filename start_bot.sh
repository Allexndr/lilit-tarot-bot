#!/bin/bash
# Скрипт для безопасного запуска бота

# Убить все старые процессы
pkill -9 -f "python3 main.py"
sleep 2

# Проверить, что все убиты
if pgrep -f "python3 main.py" > /dev/null; then
    echo "❌ Не удалось убить старые процессы"
    exit 1
fi

# Запустить один экземпляр
nohup python3 main.py > bot.log 2>&1 &

echo "✅ Бот запущен (PID: $!)"
