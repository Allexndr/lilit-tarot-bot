import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    User,
    History,
    Star,
    Zap,
    Calendar,
    Clock,
    MapPin,
    ChevronRight,
    Search,
    Filter,
    Compass,
    Sparkles
} from 'lucide-react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { GlassCard } from '../components/UI';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const Profile = () => {
    const { t } = useTranslation();
    const [user, setUser] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('history'); // history, stats, settings

    useEffect(() => {
        fetchProfileData();
    }, []);

    const fetchProfileData = async () => {
        try {
            setLoading(true);
            // endpoints now use current_user from JWT
            const userRes = await axios.get(`${API_URL}/user/me`);
            setUser(userRes.data);

            const historyRes = await axios.get(`${API_URL}/user/all-history`);
            setHistory(historyRes.data);
        } catch (error) {
            console.error("Error fetching profile:", error);
        } finally {
            setLoading(false);
        }
    };

    const getTypeIcon = (type) => {
        switch (type) {
            case 'tarot': return <Sparkles className="w-5 h-5 text-purple-400" />;
            case 'matrix': return <Compass className="w-5 h-5 text-gold-400" />;
            case 'astrology': return <Star className="w-5 h-5 text-blue-400" />;
            case 'psychomatrix': return <Search className="w-5 h-5 text-green-400" />;
            case 'runes': return <Zap className="w-5 h-5 text-amber-500" />;
            default: return <History className="w-5 h-5" />;
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="relative">
                    <div className="w-12 h-12 border-4 border-purple-500/20 border-t-purple-500 rounded-full animate-spin"></div>
                    <div className="absolute inset-0 flex items-center justify-center">
                        <Star className="w-4 h-4 text-purple-500 animate-pulse" />
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8 max-w-6xl">
            {/* Header / Basic Info */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-12">
                <div className="lg:col-span-1">
                    <div className="flex flex-col items-center text-center">
                        <div className="relative group mb-6">
                            <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                            <div className="relative w-32 h-32 rounded-full overflow-hidden border-2 border-white/10 p-1 bg-[#0a0a0f]">
                                {user?.username ? (
                                    <div className="w-full h-full rounded-full bg-gradient-to-br from-purple-500/30 to-blue-500/30 flex items-center justify-center text-5xl font-serif text-white uppercase">
                                        {user.username[0]}
                                    </div>
                                ) : (
                                    <User className="w-full h-full p-6 text-gray-400" />
                                )}
                            </div>
                            <div className="absolute bottom-1 right-1 bg-green-500 w-5 h-5 rounded-full border-4 border-[#0a0a0f]" title="Active"></div>
                        </div>

                        <h1 className="text-3xl font-serif text-white mb-2">{user?.first_name || t('profile.rank_value')}</h1>
                        <p className="text-purple-400/80 mb-6">@{user?.username || 'anonymous'}</p>

                        <div className="flex gap-4 w-full overflow-x-auto pb-2 no-scrollbar">
                            <div className="flex-1 min-w-[100px] p-3 rounded-2xl bg-white/5 border border-white/10 text-center">
                                <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">{t('profile.energy')}</p>
                                <div className="flex items-center justify-center gap-1">
                                    <Zap className="w-4 h-4 text-amber-400 fill-amber-400" />
                                    <span className="text-xl font-bold text-white">{user?.energy || 0}</span>
                                </div>
                            </div>
                            <div className="flex-1 min-w-[100px] p-3 rounded-2xl bg-white/5 border border-white/10 text-center">
                                <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">{t('profile.rank')}</p>
                                <div className="flex items-center justify-center gap-1">
                                    <Star className="w-4 h-4 text-gold-400 fill-gold-400" />
                                    <span className="text-lg font-bold text-white">{t('profile.rank_value')}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Personal Data Card */}
                <div className="lg:col-span-3">
                    <GlassCard className="h-full p-8 border-purple-500/10">
                        <div className="flex items-center justify-between mb-8">
                            <h2 className="text-xl font-serif text-white flex items-center gap-3">
                                <Calendar className="w-5 h-5 text-purple-400" />
                                {t('profile.birth_data_title')}
                            </h2>
                            <button className="text-sm text-purple-400 hover:text-white transition-colors flex items-center gap-1">
                                {t('profile.change')} <ChevronRight className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            <div className="space-y-1">
                                <p className="text-xs text-gray-500 uppercase">{t('profile.date')}</p>
                                <div className="flex items-center gap-3 text-white">
                                    <Calendar className="w-4 h-4 text-gray-400" />
                                    <span>{user?.birth_date || t('profile.not_specified')}</span>
                                </div>
                            </div>
                            <div className="space-y-1">
                                <p className="text-xs text-gray-500 uppercase">{t('profile.time')}</p>
                                <div className="flex items-center gap-3 text-white">
                                    <Clock className="w-4 h-4 text-gray-400" />
                                    <span>{user?.birth_time || '--:--'}</span>
                                </div>
                            </div>
                            <div className="space-y-1">
                                <p className="text-xs text-gray-500 uppercase">{t('profile.place')}</p>
                                <div className="flex items-center gap-3 text-white">
                                    <MapPin className="w-4 h-4 text-gray-400" />
                                    <span className="truncate">{user?.birth_place || t('profile.not_specified_f')}</span>
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 pt-8 border-t border-white/5 overflow-x-auto">
                            <div className="flex items-center justify-between min-w-[280px]">
                                <div className="text-center">
                                    <p className="text-2xl font-bold text-white">{history.length}</p>
                                    <p className="text-[10px] text-gray-500 uppercase tracking-widest">{t('profile.sessions')}</p>
                                </div>
                                <div className="h-8 w-px bg-white/10"></div>
                                <div className="text-center">
                                    <p className="text-2xl font-bold text-white">{user?.total_readings || 0}</p>
                                    <p className="text-[10px] text-gray-500 uppercase tracking-widest">{t('profile.predictions')}</p>
                                </div>
                                <div className="h-8 w-px bg-white/10"></div>
                                <div className="text-center">
                                    <p className="text-2xl font-bold text-white">22%</p>
                                    <p className="text-[10px] text-gray-500 uppercase tracking-widest">{t('profile.match')}</p>
                                </div>
                            </div>
                        </div>
                    </GlassCard>
                </div>
            </div>

            {/* History Feed */}
            <div className="space-y-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-2xl font-serif text-white">{t('profile.history_calculations')}</h3>
                    <div className="flex gap-2">
                        <button className="p-2 rounded-lg bg-white/5 border border-white/10 text-gray-400 hover:text-white transition-colors">
                            <Filter className="w-4 h-4" />
                        </button>
                    </div>
                </div>

                {history.length > 0 ? (
                    <div className="grid gap-4">
                        {history.map((item, index) => (
                            <motion.div
                                key={item.id + item.type}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.05 }}
                            >
                                <GlassCard className="p-4 hover:border-purple-500/30 transition-all cursor-pointer group">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-4">
                                            <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center group-hover:scale-110 transition-transform">
                                                {getTypeIcon(item.type)}
                                            </div>
                                            <div>
                                                <h4 className="text-white font-medium">{item.title}</h4>
                                                <p className="text-xs text-gray-500 flex items-center gap-2">
                                                    <Calendar className="w-3 h-3" />
                                                    {new Date(item.date).toLocaleDateString()}
                                                    <span className="opacity-30">•</span>
                                                    <Clock className="w-3 h-3" />
                                                    {new Date(item.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                </p>
                                            </div>
                                        </div>
                                        <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-purple-400 transition-colors" />
                                    </div>
                                    <div className="mt-3 text-sm text-gray-400 line-clamp-1 italic opacity-60">
                                        "{item.interpretation?.replace(/<[^>]*>?/gm, '').substring(0, 100)}..."
                                    </div>
                                </GlassCard>
                            </motion.div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-20 bg-white/5 rounded-3xl border border-dashed border-white/10">
                        <History className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                        <h4 className="text-white font-medium mb-1">{t('profile.empty_history')}</h4>
                        <p className="text-gray-500 text-sm">{t('profile.empty_history_desc')}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Profile;
