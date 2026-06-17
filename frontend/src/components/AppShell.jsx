import React from 'react';
import { useLocation } from 'react-router-dom';
import DesktopHeader from './DesktopHeader';
import Footer from './Footer';
import BackgroundEffect from './BackgroundEffect';
import { Home, User, Sparkles, Star, Menu } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../context/ThemeContext';

const MobileNavBar = () => {
    const { t } = useTranslation();
    const location = useLocation();
    const isActive = (path) => location.pathname === path;

    return (
        <nav className="md:hidden fixed bottom-0 left-0 right-0 glass-panel rounded-none border-x-0 border-b-0 px-6 py-4 z-50">
            <div className="flex justify-between items-center max-w-md mx-auto">
                <Link to="/" className={`flex flex-col items-center gap-1 transition-colors ${isActive('/') ? 'text-[var(--color-primary)]' : ''}`} style={{ color: isActive('/') ? '' : 'var(--text-tertiary)' }}>
                    <Home size={22} />
                    <span className="text-[10px] font-medium">{t('nav.home')}</span>
                </Link>
                <Link to="/astrology" className={`flex flex-col items-center gap-1 transition-colors ${isActive('/astrology') ? 'text-[var(--color-primary)]' : ''}`} style={{ color: isActive('/astrology') ? '' : 'var(--text-tertiary)' }}>
                    <Star size={22} />
                    <span className="text-[10px] font-medium">{t('nav.stars')}</span>
                </Link>
                <Link to="/consultant" className="relative -top-6">
                    <div className="w-14 h-14 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/50 border-4 border-[var(--bg)] transition-all active:scale-90">
                        <Sparkles className="text-white" size={24} />
                    </div>
                </Link>
                <Link to="/matrix" className={`flex flex-col items-center gap-1 transition-colors ${isActive('/matrix') ? 'text-[var(--color-primary)]' : ''}`} style={{ color: isActive('/matrix') ? '' : 'var(--text-tertiary)' }}>
                    <Menu size={22} />
                    <span className="text-[10px] font-medium">{t('nav.matrix')}</span>
                </Link>
                <Link to="/profile" className={`flex flex-col items-center gap-1 transition-colors ${isActive('/profile') ? 'text-[var(--color-primary)]' : ''}`} style={{ color: isActive('/profile') ? '' : 'var(--text-tertiary)' }}>
                    <User size={22} />
                    <span className="text-[10px] font-medium">{t('nav.profile')}</span>
                </Link>
            </div>
        </nav>
    );
};

const AppShell = ({ children }) => {
    const { theme } = useTheme();

    return (
        <div className="page-container min-h-screen pb-24 md:pb-12 md:pt-24 bg-transparent selection:bg-purple-500/30 font-sans" data-theme={theme}>
            <BackgroundEffect />
            <DesktopHeader />
            <main className="container mx-auto px-4 md:px-8 max-w-7xl pt-4 md:pt-8 min-h-[calc(100vh-200px)]">
                {children}
            </main>
            <MobileNavBar />
            <Footer />
        </div>
    );
};

export default AppShell;
