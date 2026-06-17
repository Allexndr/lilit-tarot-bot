from kerykeion import AstrologicalSubject, NatalAspects
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import logging
import traceback

logger = logging.getLogger(__name__)

class AstroEngine:
    @staticmethod
    def get_location_data(city_name: str):
        """
        Gets coordinates and timezone for a given city name.
        """
        try:
            geolocator = Nominatim(user_agent="lilit_astro_bot")
            location = geolocator.geocode(city_name)
            if location:
                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
                return {
                    "lat": location.latitude,
                    "lng": location.longitude,
                    "tz": timezone_str or "UTC",
                    "address": location.address
                }
            return None
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return None

    @staticmethod
    def calculate_natal_chart(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
        """
        Calculates the natal chart using Kerykeion v5+ API.
        Bypasses GeoNames using local geocoding and timezone resolution.
        """
        try:
            loc = AstroEngine.get_location_data(city)
            if not loc:
                return {"error": f"Could not find coordinates for city: {city}"}
            
            # Use the AstrologicalSubject wrapper with manual coordinates and timezone
            subject = AstrologicalSubject(
                name=name,
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                city=city,
                lng=loc['lng'],
                lat=loc['lat'],
                tz_str=loc['tz'],
                online=False
            )
            
            # Planets data
            planets_data = []
            planet_names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Lilith']
            
            for p_name in planet_names:
                p_attr = p_name.lower().replace(' ', '_')
                if hasattr(subject, p_attr):
                    p_obj = getattr(subject, p_attr)
                    planets_data.append({
                        "name": p_name,
                        "sign": p_obj.sign,
                        "house": p_obj.house,
                        "retrograde": getattr(p_obj, 'retrograde', False),
                        "abs_pos": p_obj.abs_pos
                    })
            
            # Houses
            houses_data = []
            for i in range(1, 13):
                h_attr = f"house_{i}"
                if hasattr(subject, h_attr):
                    h_obj = getattr(subject, h_attr)
                    houses_data.append({
                        "name": f"House {i}",
                        "sign": h_obj.sign,
                        "abs_pos": h_obj.abs_pos
                    })
            
            # Aspects in v5
            aspects_data = []
            natal_aspects = NatalAspects(subject)
            # all_aspects is a list of AspectModel objects
            for a in natal_aspects.all_aspects:
                aspects_data.append({
                    "p1": a.p1_name,
                    "p2": a.p2_name,
                    "aspect": a.aspect,
                    "orb": a.orbit
                })
                
            return {
                "info": {
                    "name": name,
                    "date": f"{day}.{month}.{year}",
                    "time": f"{hour:02d}:{minute:02d}",
                    "city": city,
                    "lat": loc['lat'],
                    "lng": loc['lng'],
                    "tz": loc['tz']
                },
                "planets": planets_data,
                "houses": houses_data,
                "aspects": aspects_data
            }
        except Exception as e:
            logger.error(f"Astrology calculation error: {e}")
            logger.error(traceback.format_exc())
            return {"error": str(e)}

if __name__ == "__main__":
    # Test
    res = AstroEngine.calculate_natal_chart("Test User", 1994, 3, 15, 12, 0, "Moscow")
    if "error" not in res:
        print(f"Natal Chart for {res['info']['name']} ({res['info']['city']}):")
        if res['planets']:
            print(f"Sun: {res['planets'][0]['sign']} in house {res['planets'][0]['house']}")
        if res['houses']:
            print(f"Ascendant: {res['houses'][0]['sign']}")
        print(f"Found {len(res['aspects'])} aspects.")
        if res['aspects']:
            print(f"Sample aspect: {res['aspects'][0]['p1']} {res['aspects'][0]['aspect']} {res['aspects'][0]['p2']} (orb {res['aspects'][0]['orb']:.2f})")
    else:
        print(f"Error: {res['error']}")
