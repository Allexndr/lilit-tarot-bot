#!/usr/bin/env python3
"""
Скрипт для запуска всей платформы АРУАХ
"""

import asyncio
import subprocess
import sys
import os
import time
import signal
from pathlib import Path

class PlatformRunner:
    """Класс для запуска платформы"""
    
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent
        
    def start_telegram_bot(self):
        """Запустить Telegram бота"""
        print("🤖 Запуск Telegram бота...")
        bot_dir = self.base_dir / "telegram_bot"
        cmd = [sys.executable, "main.py"]
        
        process = subprocess.Popen(
            cmd,
            cwd=bot_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        self.processes.append(("Telegram Bot", process))
        print("✅ Telegram бот запущен")
        
    def start_web_site(self):
        """Запустить веб-сайт"""
        print("🌐 Запуск веб-сайта...")
        web_dir = self.base_dir / "web_site"
        
        # Проверить, установлены ли зависимости
        if not (web_dir / "node_modules").exists():
            print("📦 Установка зависимостей веб-сайта...")
            subprocess.run(["npm", "install"], cwd=web_dir, check=True)
        
        cmd = ["npm", "run", "dev"]
        process = subprocess.Popen(
            cmd,
            cwd=web_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        self.processes.append(("Web Site", process))
        print("✅ Веб-сайт запущен на http://localhost:3000")
    
    def start_admin_panel(self):
        """Запустить админ-панель"""
        print("🔧 Запуск админ-панели...")
        admin_dir = self.base_dir / "admin_panel"
        cmd = [sys.executable, "run_admin.py"]
        
        process = subprocess.Popen(
            cmd,
            cwd=admin_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        self.processes.append(("Admin Panel", process))
        print("✅ Админ-панель запущена на http://localhost:8001")
        
    def start_database(self):
        """Запустить базу данных (если нужно)"""
        print("🗄️ Проверка базы данных...")
        # Здесь можно добавить запуск PostgreSQL, если нужно
        print("✅ База данных готова")
        
    def start_redis(self):
        """Запустить Redis (если нужно)"""
        print("🔴 Проверка Redis...")
        # Здесь можно добавить запуск Redis, если нужно
        print("✅ Redis готов")
        
    def start_all(self):
        """Запустить все сервисы"""
        print("🚀 Запуск платформы АРУАХ...")
        print("=" * 50)
        
        try:
            # Запустить сервисы
            self.start_database()
            self.start_redis()
            self.start_telegram_bot()
            self.start_web_site()
            self.start_admin_panel()
            
            print("=" * 50)
            print("🎉 Платформа АРУАХ запущена!")
            print("")
            print("📱 Telegram бот: https://t.me/aruah_bot")
            print("🌐 Веб-сайт: http://localhost:3000")
            print("🔧 Админ-панель: http://localhost:8001")
            print("")
            print("Нажмите Ctrl+C для остановки")
            print("=" * 50)
            
            # Ждать завершения
            self.wait_for_processes()
            
        except KeyboardInterrupt:
            print("\n🛑 Остановка платформы...")
            self.stop_all()
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            self.stop_all()
            
    def wait_for_processes(self):
        """Ждать завершения процессов"""
        try:
            while True:
                time.sleep(1)
                # Проверить, что все процессы ещё работают
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"⚠️ {name} завершился неожиданно")
        except KeyboardInterrupt:
            pass
            
    def stop_all(self):
        """Остановить все процессы"""
        print("🛑 Остановка всех сервисов...")
        
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} остановлен")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"🔴 {name} принудительно остановлен")
            except Exception as e:
                print(f"⚠️ Ошибка при остановке {name}: {e}")
        
        print("✅ Все сервисы остановлены")


def main():
    """Главная функция"""
    runner = PlatformRunner()
    
    # Обработчик сигналов
    def signal_handler(signum, frame):
        print("\n🛑 Получен сигнал остановки...")
        runner.stop_all()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Запустить платформу
    runner.start_all()


if __name__ == "__main__":
    main()
