import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.database import DatabaseManager, init_db
from bot.models import TarotCard
from bot.tarot_data import MAJOR_ARCANA

async def seed_tarot_cards():
    print("Initializing DB...")
    await init_db()
    
    session = await DatabaseManager.get_session()
    try:
        print("Seeding Tarot Cards...")
        for card_id, data in MAJOR_ARCANA.items():
            # Check if card exists
            existing = await session.get(TarotCard, card_id)
            if existing:
                continue
                
            card = TarotCard(
                id=card_id,
                name=data['name'],
                name_en=data.get('name_en', ''),
                arcana_type="Major",
                upright_meaning=data.get('upright_meaning', data.get('upright_short', 'Значение карты...')),
                reversed_meaning=data.get('reversed_meaning', 'Обратное значение...'),
                upright_short=data.get('upright_short', 'Краткое значение'),
                reversed_short=data.get('reversed_short', 'Краткое обратное')
            )
            session.add(card)
        
        await session.commit()
        print("✅ Cards seeded successfully!")
    except Exception as e:
        print(f"❌ Error seeding cards: {e}")
        await session.rollback()
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(seed_tarot_cards())
