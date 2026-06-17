from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Date, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)  # male, female, other
    city = Column(String(255), nullable=True)
    timezone = Column(String(50), default="Asia/Almaty")
    
    # Astrology data
    birth_time = Column(String(10), nullable=True) # HH:MM format
    birth_place = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Subscription info
    subscription_type = Column(String(20), default="free")  # free, basic, premium
    subscription_end = Column(DateTime, nullable=True)
    daily_readings_count = Column(Integer, default=0)
    daily_readings_limit = Column(Integer, default=1)
    
    # Statistics
    total_readings = Column(Integer, default=0)
    registration_date = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now())
    
    # Settings
    notifications_enabled = Column(Boolean, default=True)
    daily_card_time = Column(String(5), default="09:00")  # HH:MM format
    
    # Monetization (Energy System)
    energy = Column(Integer, default=1)
    stars_balance = Column(Integer, default=0)
    last_energy_refill = Column(Date, default=func.current_date())
    
    # Relationships
    readings = relationship("Reading", back_populates="user", foreign_keys="Reading.user_id")
    destiny_matrices = relationship("DestinyMatrix", back_populates="user")
    astro_charts = relationship("AstroChart", back_populates="user")
    psychomatrix_results = relationship("PsychomatrixResult", back_populates="user")
    rune_readings = relationship("RuneReading", back_populates="user")
    compatibility_results = relationship("CompatibilityResult", back_populates="user", foreign_keys="CompatibilityResult.user_id")


class TarotCard(Base):
    __tablename__ = "tarot_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_en = Column(String(255), nullable=True)
    arcana_type = Column(String(20), nullable=False)  # major, minor
    suit = Column(String(20), nullable=True)  # cups, wands, swords, pentacles
    number = Column(Integer, nullable=True)
    
    # Interpretations
    upright_meaning = Column(Text, nullable=False)
    reversed_meaning = Column(Text, nullable=False)
    upright_short = Column(Text, nullable=False)
    reversed_short = Column(Text, nullable=False)
    
    # Additional meanings for different contexts
    love_meaning = Column(Text, nullable=True)
    career_meaning = Column(Text, nullable=True)
    health_meaning = Column(Text, nullable=True)
    spiritual_meaning = Column(Text, nullable=True)
    
    # Arcana dialogue
    arcana_personality = Column(Text, nullable=True)
    arcana_voice_phrases = Column(JSON, nullable=True)  # List of phrases for dialogue


class Spread(Base):
    __tablename__ = "spreads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    card_count = Column(Integer, nullable=False)
    positions = Column(JSON, nullable=False)  # List of position descriptions
    is_premium = Column(Boolean, default=False)
    category = Column(String(50), nullable=False)  # daily, relationship, deep, etc.


class Reading(Base):
    __tablename__ = "readings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    spread_id = Column(Integer, ForeignKey("spreads.id"), nullable=False)
    
    # Reading data
    question = Column(Text, nullable=True)
    cards_drawn = Column(JSON, nullable=False)  # List of card IDs with positions
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Shared readings
    is_shared = Column(Boolean, default=False)
    share_token = Column(String(50), nullable=True, unique=True)
    partner_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="readings", foreign_keys=[user_id])
    partner_user = relationship("User", foreign_keys=[partner_user_id])
    spread = relationship("Spread")


class DestinyMatrix(Base):
    __tablename__ = "destiny_matrices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    birth_date = Column(Date, nullable=False)
    
    # Matrix positions (22 arcana positions)
    matrix_data = Column(JSON, nullable=False)
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="destiny_matrices")


class AstroForecast(Base):
    __tablename__ = "astro_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    zodiac_sign = Column(String(20), nullable=False)
    forecast_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    forecast_date = Column(Date, nullable=False)
    
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())


class AstroChart(Base):
    __tablename__ = "astro_charts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    birth_date = Column(Date, nullable=False)
    birth_time = Column(String(10), nullable=True)
    birth_place = Column(String(255), nullable=True)
    
    chart_data = Column(JSON, nullable=False)  # Full calculation result
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="astro_charts")


class PsychomatrixResult(Base):
    __tablename__ = "psychomatrix_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    birth_date = Column(Date, nullable=False)
    
    matrix_data = Column(JSON, nullable=False)
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="psychomatrix_results")


class RuneReading(Base):
    __tablename__ = "rune_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    spread_type = Column(String(50), nullable=False)
    question = Column(Text, nullable=True)
    runes_drawn = Column(JSON, nullable=False)
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="rune_readings")


class CompatibilityResult(Base):
    __tablename__ = "compatibility_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    partner_name = Column(String(255), nullable=True)
    partner_birth_date = Column(Date, nullable=False)
    
    compatibility_data = Column(JSON, nullable=False)
    interpretation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="compatibility_results", foreign_keys=[user_id])


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    amount = Column(Integer, nullable=False)  # in tenge
    payment_type = Column(String(20), nullable=False)  # subscription, one_time
    subscription_type = Column(String(20), nullable=True)  # basic, premium
    
    payment_provider_id = Column(String(255), nullable=True)
    status = Column(String(20), default="pending")  # pending, completed, failed
    
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User")


class Trigger(Base):
    __tablename__ = "triggers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    trigger_text = Column(String(255), nullable=False)
    trigger_condition = Column(Text, nullable=False)
    spread_id = Column(Integer, ForeignKey("spreads.id"), nullable=False)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_triggered = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User")
    spread = relationship("Spread")


class Tarologist(Base):
    __tablename__ = "tarologists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    photo_url = Column(String(512), nullable=True)
    description = Column(Text, nullable=False)
    specialization = Column(String(255), nullable=True)
    rating = Column(Float, default=5.0)
    review_count = Column(Integer, default=0)
    price = Column(Integer, default=1000)  # Price in Stars or currency
    experience = Column(String(50), nullable=True)
    
    # Relationships
    reviews = relationship("Review", back_populates="tarologist")


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    tarologist_id = Column(Integer, ForeignKey("tarologists.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    tarologist = relationship("Tarologist", back_populates="reviews")
    user = relationship("User") 