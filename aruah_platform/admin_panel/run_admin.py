#!/usr/bin/env python3
"""
Скрипт для запуска админ-панели АРУАХ
"""

import uvicorn
import logging
from pathlib import Path
import sys

# Добавить путь к модулям
sys.path.append(str(Path(__file__).parent.parent))

from admin_panel.web_admin import app

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Запуск админ-панели"""
    logger.info("🚀 Запуск админ-панели АРУАХ...")
    logger.info("🌐 Админ-панель будет доступна по адресу: http://localhost:8001")
    logger.info("🔑 Пароль по умолчанию: aruah_admin_2024")
    logger.info("⚠️  Не забудьте изменить пароль в продакшене!")
    
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            log_level="info",
            reload=True
        )
    except KeyboardInterrupt:
        logger.info("🛑 Админ-панель остановлена")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске админ-панели: {e}")

if __name__ == "__main__":
    main()

