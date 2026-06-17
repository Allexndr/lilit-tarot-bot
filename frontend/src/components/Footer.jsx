import React from 'react';
import { Moon, Instagram, Twitter, MessageCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
    return (
        <footer className="hidden md:block w-full border-t border-white/10 bg-[#020205] pt-16 pb-8 mt-20 relative z-10">
            <div className="container mx-auto px-8 max-w-7xl">
                <div className="grid grid-cols-4 gap-12 mb-12">
                    {/* Brand */}
                    <div className="col-span-1">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center">
                                <Moon className="text-white w-5 h-5" />
                            </div>
                            <h3 className="text-xl font-black font-cinzel text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
                                LILIT TAROT
                            </h3>
                        </div>
                        <p className="text-gray-500 text-sm leading-relaxed mb-6">
                            Древние знания в современном формате. Познай себя через Таро, Руны и Астрологию.
                        </p>
                        <div className="flex gap-4">
                            <a href="#" className="w-10 h-10 roounded-full bg-white/5 flex items-center justify-center rounded-full hover:bg-purple-500/20 hover:text-purple-300 transition-all">
                                <Instagram size={18} />
                            </a>
                            <a href="#" className="w-10 h-10 roounded-full bg-white/5 flex items-center justify-center rounded-full hover:bg-purple-500/20 hover:text-purple-300 transition-all">
                                <Twitter size={18} />
                            </a>
                            <a href="#" className="w-10 h-10 roounded-full bg-white/5 flex items-center justify-center rounded-full hover:bg-purple-500/20 hover:text-purple-300 transition-all">
                                <MessageCircle size={18} />
                            </a>
                        </div>
                    </div>

                    {/* Links */}
                    <div className="col-span-1">
                        <h4 className="text-white font-bold mb-6 font-cinzel tracking-wider">Услуги</h4>
                        <ul className="space-y-3 text-sm text-gray-400">
                            <li><Link to="/services/tarot/three_cards" className="hover:text-purple-300 transition-colors">Таро Расклады</Link></li>
                            <li><Link to="/matrix" className="hover:text-purple-300 transition-colors">Матрица Судьбы</Link></li>
                            <li><Link to="/astrology" className="hover:text-purple-300 transition-colors">Натальная Карта</Link></li>
                            <li><Link to="/compatibility" className="hover:text-purple-300 transition-colors">Совместимость</Link></li>
                        </ul>
                    </div>

                    {/* Company */}
                    <div className="col-span-1">
                        <h4 className="text-white font-bold mb-6 font-cinzel tracking-wider">Проект</h4>
                        <ul className="space-y-3 text-sm text-gray-400">
                            <li><Link to="/about" className="hover:text-purple-300 transition-colors">О нас</Link></li>
                            <li><Link to="/contact" className="hover:text-purple-300 transition-colors">Контакты</Link></li>
                            <li><Link to="/privacy" className="hover:text-purple-300 transition-colors">Конфиденциальность</Link></li>
                            <li><Link to="/terms" className="hover:text-purple-300 transition-colors">Условия использования</Link></li>
                        </ul>
                    </div>

                    {/* Newsletter */}
                    <div className="col-span-1">
                        <h4 className="text-white font-bold mb-6 font-cinzel tracking-wider">Энергия Дня</h4>
                        <p className="text-gray-500 text-sm mb-4">Получайте "Карту Дня" каждое утро на почту.</p>
                        <div className="flex gap-2">
                            <input
                                type="email"
                                placeholder="Ваш Email"
                                className="bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-purple-500 w-full"
                            />
                            <button className="bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg text-sm font-bold transition-colors">
                                OK
                            </button>
                        </div>
                    </div>
                </div>

                <div className="border-t border-white/5 pt-8 flex justify-between items-center text-xs text-gray-600">
                    <p>&copy; 2024 Lilit Tarot Platform. Все права защищены.</p>
                    <div className="flex gap-6">
                        <span>Made with 💜 via Gemini</span>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
