import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources: {
            ru: {
                translation: {
                    "hero_title": "ЛИЛИТ ТАРО",
                    "hero_subtitle": "Погрузитесь в мир древних знаний",
                    "hero_desc": "Погрузитесь в мир древних знаний. Таро, Астрология и Руны — инструменты самопознания в современной интерпретации.",
                    "start_divination": "Начать Гадание",
                    "card_of_day": "Карта Дня",
                    "platform_badge": "Мистическая Платформа №1",
                    "popular_services": "Популярные расклады",
                    "services": {
                        "daily_card": "Карта Дня",
                        "love_spread": "Отношения",
                        "sex_spread": "Секс и Страсть",
                        "three_cards": "Путь",
                        "matrix": "Матрица Судьбы",
                        "astrology": "Астрология",
                        "runes": "Руны",
                        "psychomatrix": "Психоматрица",
                        "dreams": "Сны",
                        "iching": "И-Цзин",
                        "compatibility": "Совместимость"
                    },
                    "nav": {
                        "home": "Главная",
                        "stars": "Звезды",
                        "matrix": "Матрица",
                        "profile": "Профиль"
                    },
                    "profile": {
                        "energy": "Ваша Энергия",
                        "refill": "Пополнить",
                        "history": "История раскладов",
                        "rank": "Ранг",
                        "rank_value": "Новичок",
                        "birth_date": "Дата рождения",
                        "birth_data_title": "Данные рождения",
                        "change": "Изменить",
                        "date": "Дата",
                        "time": "Время",
                        "place": "Место",
                        "not_specified": "Не указана",
                        "not_specified_f": "Не указано",
                        "sessions": "Сеансов",
                        "predictions": "Прогнозов",
                        "match": "Совпадение",
                        "history_calculations": "История расчетов",
                        "empty_history": "История пуста",
                        "empty_history_desc": "Ваши первые расчеты появятся здесь"
                    },
                    "login": {
                        "title": "Вход",
                        "desc": "Войдите через Telegram, чтобы сохранить историю раскладов и получить доступ к матрице судьбы.",
                        "error": "Ошибка входа. Попробуйте снова.",
                        "secure_auth": "Безопасная авторизация через Telegram"
                    }
                }
            },
            en: {
                translation: {
                    "hero_title": "LILIT TAROT",
                    "hero_subtitle": "Dive into the world of ancient knowledge",
                    "hero_desc": "Explore the depths of your soul. Tarot, Astrology, and Runes — tools for self-discovery in a modern interpretation.",
                    "start_divination": "Start Reading",
                    "card_of_day": "Daily Card",
                    "platform_badge": "The #1 Mystical Platform",
                    "popular_services": "Popular Spreads",
                    "services": {
                        "daily_card": "Daily Card",
                        "love_spread": "Relationships",
                        "sex_spread": "Sex & Passion",
                        "three_cards": "The Path",
                        "matrix": "Destiny Matrix",
                        "astrology": "Astrology",
                        "runes": "Runes",
                        "psychomatrix": "Psychomatrix",
                        "dreams": "Dreams",
                        "iching": "I-Ching",
                        "compatibility": "Compatibility"
                    },
                    "nav": {
                        "home": "Home",
                        "stars": "Stars",
                        "matrix": "Matrix",
                        "profile": "Profile"
                    },
                    "profile": {
                        "energy": "Your Energy",
                        "refill": "Refill",
                        "history": "Reading History",
                        "rank": "Rank",
                        "rank_value": "Beginner",
                        "birth_date": "Birth Date",
                        "birth_data_title": "Birth Data",
                        "change": "Change",
                        "date": "Date",
                        "time": "Time",
                        "place": "Place",
                        "not_specified": "Not specified",
                        "not_specified_f": "Not specified",
                        "sessions": "Sessions",
                        "predictions": "Predictions",
                        "match": "Match",
                        "history_calculations": "Calculation History",
                        "empty_history": "History is empty",
                        "empty_history_desc": "Your first calculations will appear here"
                    },
                    "login": {
                        "title": "Login",
                        "desc": "Log in via Telegram to save your reading history and access the destiny matrix.",
                        "error": "Login failed. Please try again.",
                        "secure_auth": "Secure authorization via Telegram"
                    }
                }
            },
            kk: {
                translation: {
                    "hero_title": "ЛИЛИТ ТАРО",
                    "hero_subtitle": "Ежелгі білім әлеміне еніңіз",
                    "hero_desc": "Өз жаныңызды таныңыз. Таро, Астрология және Руналар — заманауи интерпретациядағы өзін-өзі тану құралдары.",
                    "start_divination": "Бал ашу",
                    "card_of_day": "Күн картасы",
                    "platform_badge": "№1 Мистикалық платформа",
                    "popular_services": "Танымал есептеулер",
                    "services": {
                        "daily_card": "Күн картасы",
                        "love_spread": "Қарым-қатынас",
                        "sex_spread": "Секс және Құмарлық",
                        "three_cards": "Жол",
                        "matrix": "Тағдыр матрицасы",
                        "astrology": "Астрология",
                        "runes": "Руналар",
                        "psychomatrix": "Психоматрица",
                        "dreams": "Түстер",
                        "iching": "И-Цзин",
                        "compatibility": "Үйлесімділік"
                    },
                    "nav": {
                        "home": "Басты",
                        "stars": "Жұлдыздар",
                        "matrix": "Матрица",
                        "profile": "Профиль"
                    },
                    "profile": {
                        "energy": "Сіздің Энергияңыз",
                        "refill": "Толықтыру",
                        "history": "Тарих",
                        "rank": "Ранк",
                        "rank_value": "Жаңадан бастаушы",
                        "birth_date": "Туған күні",
                        "birth_data_title": "Туған күнінің деректері",
                        "change": "Өзгерту",
                        "date": "Күні",
                        "time": "Уақыты",
                        "place": "Орны",
                        "not_specified": "Көрсетілмеген",
                        "not_specified_f": "Көрсетілмеген",
                        "sessions": "Сеанстар",
                        "predictions": "Божамдар",
                        "match": "Үйлесімділік",
                        "history_calculations": "Есептеулер тарихы",
                        "empty_history": "Тарих бос",
                        "empty_history_desc": "Бірінші есептеулер осында пайда болады"
                    },
                    "login": {
                        "title": "Кіру",
                        "desc": "Тарихыңызды сақтау және тағдыр матрицасына қол жеткізу үшін Telegram арқылы кіріңіз.",
                        "error": "Кіру қатесі. Қайтадан байқап көріңіз.",
                        "secure_auth": "Telegram арқылы қауіпсіз авторизация"
                    }
                }
            }
        },
        fallbackLng: "ru",
        interpolation: {
            escapeValue: false
        }
    });

export default i18n;
