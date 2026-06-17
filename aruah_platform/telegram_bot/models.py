"""
Модели базы данных для платформы АРУАХ
"""

from datetime import datetime, date
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date, ForeignKey, JSON, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    
    # Персональные данные
    birth_date = Column(Date, nullable=True)
    birth_time = Column(String(8), nullable=True)  # HH:MM:SS
    birth_place = Column(String(255), nullable=True)
    timezone = Column(String(50), default="Asia/Almaty")
    
    # Подписка
    subscription_type = Column(String(20), default="free")  # free, premium, vip
    subscription_start = Column(DateTime, nullable=True)
    subscription_end = Column(DateTime, nullable=True)
    
    # Лимиты
    daily_requests = Column(Integer, default=0)
    daily_limit = Column(Integer, default=3)
    total_spent = Column(Integer, default=0)  # в тиынах
    
    # Реферальная система
    referral_code = Column(String(20), unique=True, nullable=True)
    referred_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_earnings = Column(Integer, default=0)
    
    # Статистика
    total_requests = Column(Integer, default=0)
    registration_date = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now())
    
    # Настройки
    notifications_enabled = Column(Boolean, default=True)
    language = Column(String(5), default="ru")  # ru, kz, en
    
    # Связи
    readings = relationship("Reading", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    referrals = relationship("User", backref="referrer")


class TarotCard(Base):
    """Модель карты Таро"""
    __tablename__ = "tarot_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    name_kz = Column(String(255), nullable=True)
    
    # Тип карты
    arcana_type = Column(String(20), nullable=False)  # major, minor
    suit = Column(String(20), nullable=True)  # cups, wands, swords, pentacles
    number = Column(Integer, nullable=True)
    
    # Интерпретации
    upright_meaning = Column(Text, nullable=False)
    reversed_meaning = Column(Text, nullable=False)
    upright_short = Column(Text, nullable=False)
    reversed_short = Column(Text, nullable=False)
    
    # Контекстные значения
    love_meaning = Column(Text, nullable=True)
    career_meaning = Column(Text, nullable=True)
    health_meaning = Column(Text, nullable=True)
    spiritual_meaning = Column(Text, nullable=True)
    
    # AI-диалог
    arcana_personality = Column(Text, nullable=True)
    arcana_voice_phrases = Column(JSON, nullable=True)
    
    # Метаданные
    element = Column(String(20), nullable=True)
    planet = Column(String(20), nullable=True)
    zodiac_sign = Column(String(20), nullable=True)


class Spread(Base):
    """Модель расклада Таро"""
    __tablename__ = "spreads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_kz = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    description_kz = Column(Text, nullable=True)
    
    # Параметры
    card_count = Column(Integer, nullable=False)
    positions = Column(JSON, nullable=False)  # Список позиций
    is_premium = Column(Boolean, default=False)
    category = Column(String(50), nullable=False)  # daily, relationship, deep, etc.
    
    # Метаданные
    difficulty = Column(String(20), default="easy")  # easy, medium, hard
    duration_minutes = Column(Integer, default=5)


class Reading(Base):
    """Модель расклада пользователя"""
    __tablename__ = "readings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    spread_id = Column(Integer, ForeignKey("spreads.id"), nullable=False)
    
    # Данные расклада
    question = Column(Text, nullable=True)
    cards_drawn = Column(JSON, nullable=False)  # Список карт с позициями
    interpretation = Column(Text, nullable=False)
    ai_model = Column(String(50), default="gpt-4")
    tokens_used = Column(Integer, default=0)
    cost = Column(DECIMAL(10, 4), default=0)
    
    # Совместные расклады
    is_shared = Column(Boolean, default=False)
    share_token = Column(String(50), nullable=True, unique=True)
    partner_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User", back_populates="readings", foreign_keys=[user_id])
    partner_user = relationship("User", foreign_keys=[partner_user_id])
    spread = relationship("Spread")


class DestinyMatrix(Base):
    """Модель матрицы судьбы"""
    __tablename__ = "destiny_matrices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    birth_date = Column(Date, nullable=False)
    
    # Данные матрицы
    matrix_data = Column(JSON, nullable=False)  # 40+ точек
    interpretation = Column(Text, nullable=False)
    ai_model = Column(String(50), default="gpt-4")
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User")


class Numerology(Base):
    """Модель нумерологических расчётов"""
    __tablename__ = "numerology"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Основные числа
    life_path_number = Column(Integer, nullable=False)
    destiny_number = Column(Integer, nullable=False)
    soul_number = Column(Integer, nullable=False)
    personality_number = Column(Integer, nullable=False)
    
    # Квадрат Пифагора
    pythagorean_square = Column(JSON, nullable=False)
    
    # Персональные годы
    personal_year = Column(Integer, nullable=False)
    personal_month = Column(Integer, nullable=False)
    
    # Интерпретация
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User")


class Astrology(Base):
    """Модель астрологических данных"""
    __tablename__ = "astrology"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Натальная карта
    birth_date = Column(Date, nullable=False)
    birth_time = Column(String(8), nullable=True)
    birth_place = Column(String(255), nullable=True)
    
    # Планеты
    sun_sign = Column(String(20), nullable=False)
    moon_sign = Column(String(20), nullable=False)
    rising_sign = Column(String(20), nullable=False)
    natal_chart = Column(JSON, nullable=False)
    
    # Прогнозы
    daily_forecast = Column(Text, nullable=True)
    weekly_forecast = Column(Text, nullable=True)
    monthly_forecast = Column(Text, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    last_forecast_update = Column(DateTime, nullable=True)
    
    # Связи
    user = relationship("User")


class Chakra(Base):
    """Модель диагностики чакр"""
    __tablename__ = "chakras"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Состояние чакр
    chakra_data = Column(JSON, nullable=False)  # 7 чакр с уровнями
    interpretation = Column(Text, nullable=False)
    
    # Рекомендации
    meditation_advice = Column(Text, nullable=True)
    color_therapy = Column(Text, nullable=True)
    crystal_advice = Column(Text, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User")


class HumanDesign(Base):
    """Модель Human Design"""
    __tablename__ = "human_design"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Основные данные
    hd_type = Column(String(30), nullable=False)  # generator, manifestor, projector, reflector
    profile = Column(String(10), nullable=False)  # 1/3, 2/4, etc.
    authority = Column(String(30), nullable=False)
    strategy = Column(Text, nullable=False)
    
    # Центры
    defined_centers = Column(JSON, nullable=False)
    undefined_centers = Column(JSON, nullable=False)
    
    # Ворота
    defined_gates = Column(JSON, nullable=False)
    
    # Интерпретация
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User")


class Payment(Base):
    """Модель платежей"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Сумма и валюта
    amount = Column(Integer, nullable=False)  # в тиынах
    currency = Column(String(3), default="KZT")
    
    # Тип платежа
    payment_type = Column(String(20), nullable=False)  # subscription, consultation, one_time
    subscription_type = Column(String(20), nullable=True)  # premium, vip
    
    # Статус
    status = Column(String(20), default="pending")  # pending, completed, failed, refunded
    
    # Платёжная система
    provider = Column(String(50), nullable=True)  # robokassa, telegram_stars
    provider_payment_id = Column(String(255), nullable=True)
    provider_response = Column(JSON, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Связи
    user = relationship("User", back_populates="payments")


class Subscription(Base):
    """Модель подписок"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # План
    plan_type = Column(String(20), nullable=False)  # premium, vip
    price = Column(Integer, nullable=False)  # в тиынах
    
    # Период
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    auto_renew = Column(Boolean, default=True)
    
    # Платеж
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User")
    payment = relationship("Payment")


class AISession(Base):
    """Модель AI-сессий"""
    __tablename__ = "ai_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Данные сессии
    session_type = Column(String(50), nullable=False)  # tarot, numerology, etc.
    messages = Column(JSON, nullable=False)
    
    # Использование AI
    ai_model = Column(String(50), nullable=False)
    tokens_used = Column(Integer, default=0)
    cost = Column(DECIMAL(10, 4), default=0)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User")


class Analytics(Base):
    """Модель аналитики"""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Событие
    event_type = Column(String(50), nullable=False)  # reading, payment, subscription, etc.
    event_data = Column(JSON, nullable=True)
    
    # Метаданные
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User")

