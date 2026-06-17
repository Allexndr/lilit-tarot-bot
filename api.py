"""
FastAPI Backend for Tarot Platform
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import asyncio
from datetime import datetime

from bot.database import DatabaseManager
from bot.models import User, Reading, Spread
from bot.consultant_ai import ConsultantAI
from bot.services import (
    UserService, TarotService, DestinyMatrixService, AstroService, 
    RuneService, PsychomatrixService, DreamService, 
    MoonService, IChingService, CompatibilityService
)
from bot.ai_service import GeminiAI
from bot.external_data import NumerologyService
from sqlalchemy import select

app = FastAPI(title="Lilit Tarot API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserAuth(BaseModel):
    telegram_id: int
    first_name: str
    username: Optional[str] = None
    photo_url: Optional[str] = None

class UserProfile(BaseModel):
    id: int
    telegram_id: int
    first_name: Optional[str]
    energy: int
    stars_balance: int
    subscription_type: str
    total_readings: int

class ChatMessage(BaseModel):
    telegram_id: int
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str

class ReadingRequest(BaseModel):
    telegram_id: Optional[int] = None
    spread_type: str
    question: Optional[str] = None

class ReadingResponse(BaseModel):
    id: int
    spread_name: str
    cards: List[Dict[str, Any]]
    interpretation: str
    created_at: datetime
    spread: Optional[Dict[str, Any]] = None

class BirthData(BaseModel):
    birth_date: str # DD.MM.YYYY
    birth_time: Optional[str] = "12:00"
    birth_place: Optional[str] = "Almaty"

class MatrixRequest(BaseModel):
    birth_date: str

class AstroRequest(BaseModel):
    name: str = "Путник"
    birth_date: str
    birth_time: str
    birth_place: str

class RuneRequest(BaseModel):
    telegram_id: Optional[int] = None
    spread_type: str # single_rune, norns
    question: Optional[str] = None

class PsychomatrixRequest(BaseModel):
    birth_date: str

class DreamRequest(BaseModel):
    description: str

class IChingRequest(BaseModel):
    question: Optional[str] = None

class CompatibilityRequest(BaseModel):
    date1: str
    date2: str

# Dependencies
async def get_user(telegram_id: int):
    user = await UserService.get_or_create_user(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Endpoints

from bot.auth import verify_telegram_auth, check_auth_date, create_access_token, get_current_user, Token

# ... existing code ...

class TelegramAuth(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str

@app.post("/api/auth/login", response_model=Token)
async def login_via_telegram(auth_data: TelegramAuth):
    """
    Authenticate user via Telegram Widget data.
    """
    data_dict = auth_data.dict(exclude_none=True)
    # The widget returns 'id', but verify_telegram_auth expects keys exactly as received.
    # We might need to handle this carefully if pydantic changes types.
    # For now, let's convert back to dict with string values where necessary if verification fails.
    
    # Verify hash
    # Note: Pydantic model might convert int to int, but telegram hash uses strings.
    # We need to ensure we pass the data exactly as Telegram sent it (or close enough).
    # Ideally, receive raw dict, but Pydantic is safer.
    # Let's reconstruct the dict for verification:
    check_data = {
        "id": str(auth_data.id),
        "first_name": auth_data.first_name,
        "auth_date": str(auth_data.auth_date),
        "hash": auth_data.hash
    }
    if auth_data.last_name: check_data["last_name"] = auth_data.last_name
    if auth_data.username: check_data["username"] = auth_data.username
    if auth_data.photo_url: check_data["photo_url"] = auth_data.photo_url
    
    from config import settings
    if not verify_telegram_auth(check_data, settings.bot_token):
         raise HTTPException(status_code=400, detail="Invalid Telegram data hash")
         
    if not check_auth_date(auth_data.auth_date):
         raise HTTPException(status_code=400, detail="Auth data is outdated")
         
    # Get or create user
    user = await UserService.get_or_create_user(
        telegram_id=auth_data.id,
        username=auth_data.username,
        first_name=auth_data.first_name,
        last_name=auth_data.last_name
    )
    
    # Create JWT
    access_token = create_access_token(data={"sub": str(user.telegram_id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependencies
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/user/me", response_model=UserProfile)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get current logged in user profile"""
    return UserProfile(
        id=current_user.id,
        telegram_id=current_user.telegram_id,
        first_name=current_user.first_name,
        energy=current_user.energy,
        stars_balance=current_user.stars_balance,
        subscription_type=current_user.subscription_type,
        total_readings=current_user.total_readings
    )

@app.get("/api/user/{telegram_id}/profile", response_model=UserProfile)
async def get_profile(telegram_id: int):
    """Get user profile stats"""
    user = await get_user(telegram_id)
    return UserProfile(
        id=user.id,
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        energy=user.energy,
        stars_balance=user.stars_balance,
        subscription_type=user.subscription_type,
        total_readings=user.total_readings
    )

@app.get("/api/user/history", response_model=List[ReadingResponse])
async def get_history(
    limit: int = 20, 
    offset: int = 0,
    current_user: User = Depends(get_current_user)
):
    """Get user reading history"""
    session = await DatabaseManager.get_session()
    try:
        # Fetch readings (simplified, normally would join with Spread)
        result = await session.execute(
            select(Reading)
            .where(Reading.user_id == current_user.id)
            .order_by(Reading.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        readings = result.scalars().all()
        
        history = []
        for r in readings:
            # Parse cards JSON if needed, or return as is
            # Assuming r.cards_drawn is already a dict/list or needs json.loads
            import json
            cards_data = r.cards_drawn if isinstance(r.cards_drawn, list) else json.loads(r.cards_drawn)
            
            history.append(ReadingResponse(
                id=r.id,
                spread_name="Tarot Spread", # Placeholder, ideally fetch spread name
                cards=cards_data,
                interpretation=r.interpretation,
                created_at=r.created_at
            ))
        return history
    finally:
        await session.close()

@app.get("/api/user/all-history")
async def get_all_history(current_user: User = Depends(get_current_user)):
    """Get all esoteric history for a user"""
    session = await DatabaseManager.get_session()
    try:
        from bot.models import DestinyMatrix, AstroChart, PsychomatrixResult, RuneReading, CompatibilityResult
        
        # This is a bit heavy, in production we might want to paginate or use a unified history table
        readings = await session.execute(select(Reading).where(Reading.user_id == current_user.id).order_by(Reading.created_at.desc()).limit(10))
        matrices = await session.execute(select(DestinyMatrix).where(DestinyMatrix.user_id == current_user.id).order_by(DestinyMatrix.created_at.desc()).limit(10))
        charts = await session.execute(select(AstroChart).where(AstroChart.user_id == current_user.id).order_by(AstroChart.created_at.desc()).limit(10))
        psychomatrices = await session.execute(select(PsychomatrixResult).where(PsychomatrixResult.user_id == current_user.id).order_by(PsychomatrixResult.created_at.desc()).limit(10))
        runes = await session.execute(select(RuneReading).where(RuneReading.user_id == current_user.id).order_by(RuneReading.created_at.desc()).limit(10))
        
        history = []
        
        # Helper to format
        for r in readings.scalars().all():
            history.append({"type": "tarot", "id": r.id, "title": "Расклад Таро", "date": r.created_at, "interpretation": r.interpretation})
        for m in matrices.scalars().all():
            history.append({"type": "matrix", "id": m.id, "title": "Матрица Судьбы", "date": m.created_at, "interpretation": m.interpretation})
        for c in charts.scalars().all():
            history.append({"type": "astrology", "id": c.id, "title": "Натальная карта", "date": c.created_at, "interpretation": c.interpretation})
        for p in psychomatrices.scalars().all():
            history.append({"type": "psychomatrix", "id": p.id, "title": "Психоматрица", "date": p.created_at, "interpretation": p.interpretation})
        for r in runes.scalars().all():
            history.append({"type": "runes", "id": r.id, "title": f"Руны: {r.spread_type}", "date": r.created_at, "interpretation": r.interpretation})
            
        # Sort by date
        history.sort(key=lambda x: x["date"], reverse=True)
        return history
    finally:
        await session.close()

@app.post("/api/services/tarot/reading", response_model=ReadingResponse)
async def perform_reading(request: ReadingRequest, current_user: User = Depends(get_current_user)):
    """Perform a tarot reading"""
    # Use current_user instead of user lookup
    user = current_user
    
    # Determine spread logic
    cards = []
    positions = None
    spread_name = "Расклад"
    
    if request.spread_type == "daily_card":
        existing = await TarotService.get_daily_card(user.id)
        if existing:
            import json
            return ReadingResponse(
                id=existing.id,
                spread_name="Карта дня",
                cards=json.loads(existing.cards_drawn) if isinstance(existing.cards_drawn, str) else existing.cards_drawn,
                interpretation=existing.interpretation,
                created_at=existing.created_at
            )
        card = TarotService.get_random_card()
        cards = [card]
        spread_name = "Карта дня"
    elif request.spread_type in ["love_spread", "sex_spread", "three_cards"]:
        for _ in range(3):
            cards.append(TarotService.get_random_card())
        spread_name = {
            "love_spread": "Отношения",
            "sex_spread": "Секс и Страсть",
            "three_cards": "Путь"
        }.get(request.spread_type, "Расклад")
        
        if request.spread_type == "love_spread":
            positions = ["Ваши чувства", "Чувства партнера", "Будущее"]
        elif request.spread_type == "sex_spread":
            positions = ["Ваши желания", "Желания партнера", "Совместимость"]
        elif request.spread_type == "three_cards":
            positions = ["Прошлое", "Настоящее", "Будущее"]
    else:
        raise HTTPException(status_code=400, detail="Unknown spread type")

    # Interpret
    full_interpretation = f"🔮 <b>{spread_name}</b>\n\n"
    if request.question:
        full_interpretation += f"❓ Вопрос: {request.question}\n\n"
        
    for i, card in enumerate(cards):
        pos = positions[i] if positions else None
        interp = await TarotService.interpret_card(card, position=pos, question=request.question)
        full_interpretation += interp + "\n\n"

    # Save reading properly
    session = await DatabaseManager.get_session()
    spread_result = await session.execute(select(Spread).where(Spread.name == spread_name))
    spread = spread_result.scalar_one_or_none()
    if not spread:
        spread = await TarotService._ensure_daily_spread_exists(session)
    await session.close()
    
    saved_reading = await TarotService.save_reading(
        user_id=user.id,
        spread_id=spread.id,
        cards=cards,
        interpretation=full_interpretation,
        question=request.question
    )
    
    return ReadingResponse(
        id=saved_reading.id,
        spread_name=spread_name,
        cards=cards,
        interpretation=full_interpretation,
        created_at=saved_reading.created_at,
        spread={
            "name": spread_name,
            "positions": positions or ["Карта"]
        }
    )

@app.post("/api/consultant/chat", response_model=ChatResponse)
async def consultant_chat(msg: ChatMessage):
    """Chat with AI consultant"""
    response = await ConsultantAI.chat(msg.telegram_id, msg.message)
    return ChatResponse(
        response=response,
        timestamp=datetime.now().isoformat()
    )

@app.delete("/api/consultant/history/{telegram_id}")
async def clear_consultant_history(telegram_id: int):
    """Clear conversation history"""
    ConsultantAI.clear_history(telegram_id)
    return {"status": "cleared"}

@app.get("/api/meta/daily")
async def get_daily_meta():
    """Get moon phase and day number"""
    moon = MoonService.get_moon_phase()
    day_num = NumerologyService.get_day_number()
    return {
        "moon": moon,
        "numerology": day_num
    }

@app.post("/api/services/matrix")
async def calculate_matrix(req: MatrixRequest, current_user: User = Depends(get_current_user)):
    """Calculate Matrix of Destiny"""
    try:
        # Parse date
        d, m, y = map(int, req.birth_date.split('.'))
        from datetime import date
        birth_date = date(y, m, d)
        
        matrix_data = DestinyMatrixService.calculate_matrix(birth_date)
        interpretation = DestinyMatrixService.interpret_matrix(matrix_data)
        
        # Save to DB
        await DestinyMatrixService.save_matrix(current_user.id, birth_date, matrix_data, interpretation)
        
        return {
            "data": matrix_data,
            "interpretation": interpretation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/services/astrology")
async def calculate_astrology(req: AstroRequest, current_user: User = Depends(get_current_user)):
    """Calculate Natal Chart"""
    try:
        # Parse date
        d, m, y = map(int, req.birth_date.split('.'))
        from datetime import date
        birth_date = date(y, m, d)
        
        chart = AstroService.calculate_natal_chart(
            user_name=req.name,
            birth_date=birth_date,
            birth_time=req.birth_time,
            birth_place=req.birth_place
        )
        
        if "error" in chart:
            raise HTTPException(status_code=400, detail=chart["error"])
            
        interpretation = AstroService.interpret_natal_chart(chart)
        
        # Save
        await AstroService.save_astro_chart(current_user.id, birth_date, req.birth_time, req.birth_place, chart, interpretation)
        
        return {
            "chart": chart,
            "interpretation": interpretation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/services/runes")
async def perform_rune_casting(req: RuneRequest, current_user: User = Depends(get_current_user)):
    """Cast runes and get interpretation"""
    from bot.divination_data import RUNE_SPREADS
    
    spread = RUNE_SPREADS.get(req.spread_type)
    if not spread:
        raise HTTPException(status_code=400, detail="Unknown rune spread")
        
    runes = RuneService.cast_runes(spread["rune_count"])
    interpretation = await RuneService.interpret_runes(runes, spread["name"], req.question)
    
    # Save
    await RuneService.save_rune_reading(current_user.id, req.spread_type, runes, interpretation, req.question)
    
    return {
        "runes": runes,
        "interpretation": interpretation,
        "spread": spread
    }

@app.post("/api/services/psychomatrix")
async def calculate_psychomatrix(req: PsychomatrixRequest, current_user: User = Depends(get_current_user)):
    """Calculate Psychomatrix (Pythagorean Square)"""
    try:
        data = PsychomatrixService.calculate(req.birth_date)
        interpretation = PsychomatrixService.interpret(data)
        
        # Save
        d, m, y = map(int, req.birth_date.split('.'))
        from datetime import date
        birth_date = date(y, m, d)
        await PsychomatrixService.save_psychomatrix_result(current_user.id, birth_date, data, interpretation)
        
        return {"data": data, "interpretation": interpretation}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/services/dream")
async def interpret_dream(req: DreamRequest):
    """Interpret a dream"""
    try:
        interpretation = await DreamService.interpret_dream(req.description)
        return {"interpretation": interpretation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/services/moon")
async def get_moon_advice():
    """Get today's moon advice"""
    try:
        return MoonService.get_todays_advice()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/services/iching")
async def perform_iching(req: IChingRequest):
    """Perform an I Ching reading"""
    try:
        hexagram = IChingService.throw_coins()
        interpretation = await IChingService.interpret_hexagram(hexagram, req.question)
        return {"hexagram": hexagram, "interpretation": interpretation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/services/compatibility")
async def check_compatibility(req: CompatibilityRequest, current_user: User = Depends(get_current_user)):
    """Check partner compatibility"""
    try:
        data = CompatibilityService.calculate_compatibility(req.date1, req.date2)
        interpretation = await CompatibilityService.interpret_compatibility(data)
        
        # Save
        # Parse date2 as partner birth date
        d, m, y = map(int, req.date2.split('.'))
        from datetime import date
        p_birth_date = date(y, m, d)
        await CompatibilityService.save_compatibility_result(current_user.id, "Партнер", p_birth_date, data, interpretation)
        
        return {"data": data, "interpretation": interpretation}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
