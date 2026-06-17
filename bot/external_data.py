"""
Внешние данные: луна, нумерология
"""
from datetime import datetime, date
import ephem

class MoonService:
    """Сервис для работы с лунными фазами"""
    
    @staticmethod
    def get_moon_phase() -> dict:
        """Получить текущую фазу луны"""
        now = datetime.now()
        moon = ephem.Moon(now)
        phase = moon.phase
        
        # Определяем фазу
        if phase < 1:
            phase_name = "Новолуние"
            emoji = "🌑"
            meaning = "Время начинаний и новых планов"
        elif phase < 25:
            phase_name = "Растущая луна"
            emoji = "🌒"
            meaning = "Время роста и накопления энергии"
        elif phase < 50:
            phase_name = "Первая четверть"
            emoji = "🌓"
            meaning = "Время действий и преодоления препятствий"
        elif phase < 75:
            phase_name = "Растущая луна"
            emoji = "🌔"
            meaning = "Пик энергии, время достижений"
        elif phase < 99:
            phase_name = "Полнолуние"
            emoji = "🌕"
            meaning = "Кульминация, раскрытие тайн"
        elif phase < 125:
            phase_name = "Убывающая луна"
            emoji = "🌖"
            meaning = "Время отпускания и очищения"
        elif phase < 150:
            phase_name = "Последняя четверть"
            emoji = "🌗"
            meaning = "Время завершения дел"
        else:
            phase_name = "Убывающая луна"
            emoji = "🌘"
            meaning = "Подготовка к новому циклу"
        
        return {
            "phase": phase,
            "name": phase_name,
            "emoji": emoji,
            "meaning": meaning
        }


class NumerologyService:
    """Сервис для нумерологических расчетов"""
    
    @staticmethod
    def get_day_number(date_obj: date = None) -> dict:
        """Получить число дня"""
        if date_obj is None:
            date_obj = date.today()
        
        # Складываем день, месяц, год
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year
        
        # Суммируем цифры
        total = day + month + year
        
        # Сводим к одной цифре
        while total > 9 and total not in [11, 22, 33]:  # Мастер-числа
            total = sum(int(digit) for digit in str(total))
        
        # Значения чисел
        meanings = {
            1: "День лидерства и новых начинаний",
            2: "День гармонии и партнерства",
            3: "День творчества и самовыражения",
            4: "День стабильности и труда",
            5: "День перемен и свободы",
            6: "День любви и ответственности",
            7: "День мудрости и самопознания",
            8: "День силы и достижений",
            9: "День завершения и отпускания",
            11: "День интуиции и духовности (мастер-число)",
            22: "День воплощения мечты (мастер-число)",
            33: "День служения и учительства (мастер-число)"
        }
        
        return {
            "number": total,
            "meaning": meanings.get(total, "День возможностей")
        }
