import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, useNavigate, Navigate } from 'react-router-dom';
import { Home, User, Sparkles, History, Menu, Star } from 'lucide-react';
import { AnimatePresence } from 'framer-motion';
import { PageTransition, GlassCard, MysticButton } from './components/UI';
import ConsultantChat from './pages/ConsultantChat';
import MatrixDestiny from './pages/MatrixDestiny';
import Astrology from './pages/Astrology';
import RuneCasting from './pages/RuneCasting';
import Psychomatrix from './pages/Psychomatrix';
import DreamInterpreter from './pages/DreamInterpreter';
import IChing from './pages/IChing';
import MoonWidget from './components/MoonWidget';
import TarotReading from './pages/TarotReading';
import Profile from './pages/Profile';
import Compatibility from './pages/Compatibility';
import Login from './pages/Login';
import DesktopHeader from './components/DesktopHeader';
import BackgroundEffect from './components/BackgroundEffect';
import Footer from './components/Footer';
import AdBanner from './components/AdBanner';
import { motion } from 'framer-motion';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { useTheme } from './context/ThemeContext';
import ThemeToggle from './components/ThemeToggle';
import LanguageSwitcher from './components/LanguageSwitcher';

// API Configuration
const API_URL = 'http://localhost:8000/api';

import AppShell from './components/AppShell';

// --- Pages ---

const HomePage = () => {
    const { t } = useTranslation();
    const { theme } = useTheme();
    const navigate = useNavigate();
    const services = [
        { id: 'daily_card', name: t('services.daily_card'), icon: '🔮', desc: t('hero_subtitle'), path: '/services/tarot/daily_card' },
        { id: 'love_spread', name: t('services.love_spread'), icon: '💖', desc: t('services.love_spread'), path: '/services/tarot/love_spread' },
        { id: 'sex_spread', name: t('services.sex_spread'), icon: '🔥', desc: t('services.sex_spread'), path: '/services/tarot/sex_spread' },
        { id: 'three_cards', name: t('services.three_cards'), icon: '🛤', desc: t('services.three_cards'), path: '/services/tarot/three_cards' },
        { id: 'matrix', name: t('services.matrix'), icon: '⭐️', desc: t('services.matrix'), path: '/matrix' },
        { id: 'astrology', name: t('services.astrology'), icon: '🪐', desc: t('services.astrology'), path: '/astrology' },
        { id: 'runes', name: t('services.runes'), icon: 'ᚠ', desc: t('services.runes'), path: '/runes' },
        { id: 'psychomatrix', name: t('services.psychomatrix'), icon: '🔢', desc: t('services.psychomatrix'), path: '/psychomatrix' },
        { id: 'dreams', name: t('services.dreams'), icon: '🌙', desc: t('services.dreams'), path: '/dreams' },
        { id: 'iching', name: t('services.iching'), icon: '🏮', desc: t('services.iching'), path: '/iching' },
        { id: 'compatibility', name: t('services.compatibility'), icon: '❤️', desc: t('services.compatibility'), path: '/compatibility' },
    ];

    return (
        <PageTransition>
            {/* Desktop Hero Section */}
            <div className="hidden md:flex items-center justify-between py-16 max-w-7xl mx-auto relative z-10 px-4">
                <div className="w-3/5 text-left space-y-6">
                    <div className="inline-block px-4 py-1.5 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-400 text-xs font-bold tracking-widest uppercase mb-2">
                        {t('platform_badge')}
                    </div>
                    <h1 className={`text-7xl font-black leading-[1.1] font-cinzel tracking-tight ${theme === 'light'
                        ? 'bg-gradient-to-r from-violet-600 via-indigo-600 to-purple-600'
                        : 'bg-gradient-to-r from-purple-200 via-white to-purple-200'
                        } bg-clip-text text-transparent`}>
                        {t('hero_title').split(' ')[0]} <br />
                        <span className="text-5xl md:text-7xl">{t('hero_title').slice(t('hero_title').indexOf(' ') + 1)}</span>
                    </h1>
                    <p className="text-xl text-[var(--text-secondary)] max-w-lg font-light leading-relaxed">
                        {t('hero_desc')}
                    </p>
                    <div className="flex gap-4 pt-4">
                        <MysticalButton onClick={() => navigate('/services')} icon={Sparkles}>
                            {t('start_divination')}
                        </MysticalButton>
                        <MysticalButton variant="secondary" onClick={() => navigate('/services/tarot/daily_card')} icon={Star}>
                            {t('card_of_day')}
                        </MysticalButton>
                    </div>
                </div>

                {/* 3D Visual Element */}
                <div className="w-2/5 flex justify-center relative">
                    <div className="absolute inset-0 bg-purple-500/10 blur-[120px] rounded-full" />
                    <motion.div
                        animate={{ y: [-20, 20, -20], rotate: [0, 2, -2, 0] }}
                        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
                        className="relative z-10 w-64 h-96 rounded-2xl bg-gradient-to-br from-white/10 to-transparent border border-white/20 shadow-2xl overflow-hidden backdrop-blur-sm"
                    >
                        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-30" />
                        <div className="absolute inset-0 flex flex-col items-center justify-center border-2 border-white/10 rounded-xl m-3">
                            <Sparkles className="w-20 h-20 text-purple-400 opacity-50 mb-4" />
                            <p className="font-cinzel text-xs tracking-[0.5em] text-white/40 uppercase">Ethereal Bond</p>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Mobile Header */}
            <header className="md:hidden flex justify-between items-center mb-8">
                <div>
                    <MoonWidget />
                    <h1 className="text-4xl font-black font-cinzel bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent">
                        Lilit
                    </h1>
                </div>
                <div className="flex gap-2">
                    <ThemeToggle />
                    <LanguageSwitcher />
                </div>
            </header>

            <section className="mb-12 max-w-4xl mx-auto">
                <GlassCard className="relative overflow-hidden group border-none">
                    <div className="flex justify-between items-center relative z-10">
                        <div>
                            <h2 className="text-sm font-medium opacity-60 mb-1">{t('profile.energy')}</h2>
                            <p className="text-3xl font-black text-[var(--color-secondary)]">⚡️ 5 / 5</p>
                        </div>
                        <MysticalButton variant="secondary" className="scale-90">{t('profile.refill')}</MysticalButton>
                    </div>
                </GlassCard>
            </section>

            <h2 className="text-xl font-bold mb-6 flex items-center gap-3 font-cinzel">
                <Sparkles className="w-5 h-5 text-[var(--color-secondary)]" /> {t('popular_services')}
            </h2>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5 mb-12">
                {services.map(service => (
                    <GlassCard
                        key={service.id}
                        onClick={() => navigate(service.path)}
                        className="flex flex-col items-center text-center gap-4 py-8"
                    >
                        <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-purple-500/50 transition-all duration-300">
                            <span className="text-4xl filter drop-shadow-[0_0_10px_rgba(139,92,246,0.3)]">{service.icon}</span>
                        </div>
                        <div>
                            <h3 className="font-bold text-lg mb-1">{service.name}</h3>
                            <p className="text-xs opacity-60 px-2">{service.desc}</p>
                        </div>
                    </GlassCard>
                ))}
            </div>

            <AdBanner variant="native" className="mb-8" />
            <AdBanner variant="sticky-bottom" />
        </PageTransition>
    );
};

// --- App ---

const AppContent = () => {
    const location = useLocation();

    return (
        <AppShell>
            <AnimatePresence mode="wait">
                <Routes location={location} key={location.pathname}>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/consultant" element={<ConsultantChat />} />
                    <Route path="/matrix" element={<MatrixDestiny />} />
                    <Route path="/astrology" element={<Astrology />} />
                    <Route path="/runes" element={<RuneCasting />} />
                    <Route path="/psychomatrix" element={<Psychomatrix />} />
                    <Route path="/dreams" element={<DreamInterpreter />} />
                    <Route path="/iching" element={<IChing />} />
                    <Route path="/services/tarot/:spreadType" element={<TarotReading />} />
                    <Route path="/compatibility" element={<Compatibility />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/profile" element={
                        <PrivateRoute>
                            <Profile />
                        </PrivateRoute>
                    } />
                    <Route path="/history" element={
                        <PrivateRoute>
                            <Profile />
                        </PrivateRoute>
                    } />
                    <Route path="/services" element={<HomePage />} />
                </Routes>
            </AnimatePresence>
        </AppShell>
    );
};

const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('token');
    return token ? children : <Navigate to="/login" replace />;
};

const App = () => {
    return (
        <Router>
            <AppContent />
        </Router>
    );
};

export default App;
