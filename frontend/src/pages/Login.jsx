import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { GlassCard } from '../components/UI';
import { Moon, Star } from 'lucide-react';

const Login = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();

    useEffect(() => {
        // Load Telegram Widget Script
        const script = document.createElement('script');
        script.src = "https://telegram.org/js/telegram-widget.js?22";
        script.setAttribute('data-telegram-login', 'lilit_tarot_bot'); // Replace with your actual bot username
        script.setAttribute('data-size', 'large');
        script.setAttribute('data-radius', '10');
        script.setAttribute('data-userpic', 'false');
        script.setAttribute('data-request-access', 'write');
        script.setAttribute('data-onauth', 'onTelegramAuth(user)');
        script.async = true;

        const container = document.getElementById('telegram-login-container');
        if (container) container.appendChild(script);

        // Define callback function globally
        window.onTelegramAuth = async (user) => {
            try {
                const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
                const res = await axios.post(`${API_URL}/auth/login`, user);

                if (res.data.access_token) {
                    localStorage.setItem('token', res.data.access_token);
                    // Redirect to profile or home
                    navigate('/profile');
                }
            } catch (error) {
                console.error("Login failed:", error);
                alert(t('login.error'));
            }
        };

        return () => {
            // Cleanup if needed
            window.onTelegramAuth = undefined;
        };
    }, [navigate, t]);

    return (
        <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden transition-colors duration-500" style={{ backgroundColor: 'var(--color-bg-dark)' }}>
            {/* Background Elements */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-900/10 rounded-full blur-[120px] -z-10 animate-pulse"></div>

            <GlassCard className="max-w-md w-full p-8 text-center border-purple-500/20">
                <div className="flex justify-center mb-6">
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center shadow-[0_0_30px_rgba(147,51,234,0.5)]">
                        <Moon className="text-white w-8 h-8" />
                    </div>
                </div>

                <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-200 via-pink-200 to-white bg-clip-text text-transparent font-cinzel mb-2">
                    {t('hero_title')}
                </h1>
                <p className="text-gray-400 mb-8 text-sm">
                    {t('login.desc')}
                </p>

                <div className="flex justify-center min-h-[50px]" id="telegram-login-container">
                    {/* Widget renders here */}
                </div>

                <div className="mt-8 pt-6 border-t border-white/10 flex items-center justify-center gap-2 text-xs text-gray-500">
                    <Star className="w-3 h-3 text-gold-400" />
                    <span>{t('login.secure_auth')}</span>
                </div>
            </GlassCard>
        </div>
    );
};

export default Login;
