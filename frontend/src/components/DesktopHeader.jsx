import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Moon, Star, Menu as MenuIcon, User, Sparkles } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../context/ThemeContext';
import ThemeToggle from './ThemeToggle';
import LanguageSwitcher from './LanguageSwitcher';

const DesktopHeader = () => {
    const { t } = useTranslation();
    const location = useLocation();

    const { theme } = useTheme();

    const isActive = (path) => location.pathname === path;
    const linkClasses = (path) =>
        `flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-300 ${isActive(path)
            ? 'bg-purple-500/20 text-[var(--color-primary)] font-bold shadow-[0_0_15px_rgba(168,85,247,0.3)]'
            : 'text-[var(--color-text-muted)] hover:text-[var(--color-primary)] hover:bg-purple-500/5'
        }`;

    return (
        <header className="hidden md:flex fixed top-0 left-0 right-0 z-50 h-20 px-8 items-center justify-between glass-panel border-x-0 border-t-0 rounded-none backdrop-blur-md bg-opacity-80 transition-colors duration-300" style={{ backgroundColor: 'var(--color-bg-card)' }}>
            {/* Logo */}
            <Link to="/" className="flex items-center gap-3 group">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center shadow-lg group-hover:shadow-purple-500/50 transition-all duration-500">
                    <Moon className="text-white w-6 h-6" />
                </div>
                <div>
                    <h1 className={`text-2xl font-black bg-clip-text text-transparent font-cinzel tracking-wider ${theme === 'light'
                            ? 'bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600'
                            : 'bg-gradient-to-r from-purple-200 via-pink-200 to-white'
                        }`}>
                        {t('hero_title')}
                    </h1>
                </div>
            </Link>

            {/* Navigation */}
            <nav className="flex items-center gap-2">
                <Link to="/" className={linkClasses('/')}>
                    <MenuIcon className="w-4 h-4" /> {t('nav.home')}
                </Link>
                <Link to="/astrology" className={linkClasses('/astrology')}>
                    <Star className="w-4 h-4" /> {t('nav.stars')}
                </Link>
                <Link to="/matrix" className={linkClasses('/matrix')}>
                    <Sparkles className="w-4 h-4" /> {t('nav.matrix')}
                </Link>
                <Link to="/profile" className={linkClasses('/profile')}>
                    <User className="w-4 h-4" /> {t('nav.profile')}
                </Link>
            </nav>

            {/* User/Actions */}
            <div className="flex items-center gap-4">
                <LanguageSwitcher />
                <ThemeToggle />

                <Link to="/consultant">
                    <button className="px-5 py-2 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold text-sm shadow-lg hover:shadow-purple-500/40 hover:scale-105 transition-all duration-300">
                        {t('refill')}
                    </button>
                </Link>
                <div className="w-10 h-10 rounded-full p-[2px] bg-gradient-to-r from-purple-400 to-pink-400">
                    <img
                        src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                        alt="Profile"
                        className="w-full h-full rounded-full bg-black object-cover"
                    />
                </div>
            </div>
        </header>
    );
};

export default DesktopHeader;
