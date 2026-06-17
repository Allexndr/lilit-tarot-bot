import React, { useState } from 'react';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import { MapPin, Clock, Calendar, Star, Info } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const Astrology = () => {
    const [formData, setFormData] = useState({
        name: '',
        birth_date: '',
        birth_time: '12:00',
        birth_place: 'Almaty'
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const calculateChart = async () => {
        if (!formData.birth_date || !formData.name) {
            return setError('Пожалуйста, заполните имя и дату рождения');
        }

        setLoading(true);
        setError('');
        try {
            const response = await axios.post(`${API_URL}/services/astrology`, formData);
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка при расчете');
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageTransition>
            <div className="max-w-6xl mx-auto">
                <div className="mb-12 text-center">
                    <h2 className="text-4xl font-bold mb-2 flex items-center justify-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                        <Star className="text-blue-400 w-8 h-8" />
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-200 via-blue-100 to-white">
                            Натальная Карта
                        </span>
                    </h2>
                    <p className="text-blue-200/60 text-sm font-light">
                        Звездный паспорт вашей души.
                    </p>
                </div>

                <div className="grid lg:grid-cols-3 gap-8 items-start">
                    {/* Input Column */}
                    <div className="lg:col-span-1">
                        <GlassCard className="sticky top-24 border-blue-500/20">
                            <h3 className="text-lg font-bold text-white mb-6 border-b border-white/5 pb-2">Данные рождения</h3>
                            <div className="space-y-5">
                                <div>
                                    <label className="block text-[10px] text-blue-300 mb-1 uppercase tracking-widest font-bold">Ваше Имя</label>
                                    <input
                                        type="text"
                                        placeholder="Александр"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        className="w-full bg-black/40 border border-blue-500/20 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-blue-500 transition-colors shadow-inner"
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-[10px] text-blue-300 mb-1 uppercase tracking-widest font-bold">Дата</label>
                                        <div className="relative">
                                            <input
                                                type="text"
                                                placeholder="DD.MM.YYYY"
                                                value={formData.birth_date}
                                                onChange={(e) => setFormData({ ...formData, birth_date: e.target.value })}
                                                className="w-full bg-black/40 border border-blue-500/20 rounded-xl py-3 pl-9 text-white focus:outline-none focus:border-blue-500 transition-colors"
                                            />
                                            <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400 w-4 h-4" />
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-[10px] text-blue-300 mb-1 uppercase tracking-widest font-bold">Время</label>
                                        <div className="relative">
                                            <input
                                                type="text"
                                                placeholder="HH:MM"
                                                value={formData.birth_time}
                                                onChange={(e) => setFormData({ ...formData, birth_time: e.target.value })}
                                                className="w-full bg-black/40 border border-blue-500/20 rounded-xl py-3 pl-9 text-white focus:outline-none focus:border-blue-500 transition-colors"
                                            />
                                            <Clock className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400 w-4 h-4" />
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-[10px] text-blue-300 mb-1 uppercase tracking-widest font-bold">Город</label>
                                    <div className="relative">
                                        <input
                                            type="text"
                                            placeholder="Напр: Москва"
                                            value={formData.birth_place}
                                            onChange={(e) => setFormData({ ...formData, birth_place: e.target.value })}
                                            className="w-full bg-black/40 border border-blue-500/20 rounded-xl py-3 pl-9 text-white focus:outline-none focus:border-blue-500 transition-colors"
                                        />
                                        <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-blue-400 w-4 h-4" />
                                    </div>
                                </div>

                                {error && <div className="p-3 bg-red-900/20 border border-red-500/30 rounded-lg text-red-300 text-xs text-center">{error}</div>}

                                <MysticButton
                                    onClick={calculateChart}
                                    loading={loading}
                                    className="w-full justify-center bg-gradient-to-r from-blue-900 to-indigo-900 hover:from-blue-800 hover:to-indigo-800"
                                >
                                    Рассчитать Карту
                                </MysticButton>
                            </div>
                        </GlassCard>
                    </div>

                    {/* Results Column */}
                    <div className="lg:col-span-2">
                        {result ? (
                            <div className="space-y-6 animate-fade-in">
                                {/* Summary Card */}
                                <GlassCard className="bg-gradient-to-r from-[#0f172a] to-[#1e1b4b] border-blue-500/20 relative overflow-hidden">
                                    <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
                                        <Star className="w-32 h-32 text-blue-400" />
                                    </div>
                                    <div className="flex gap-6 items-start relative z-10">
                                        <Info className="text-blue-400 w-6 h-6 mt-1 shrink-0" />
                                        <div>
                                            <h4 className="text-xl font-bold mb-4 font-cinzel text-blue-100">Астрологический Портрет</h4>
                                            <div
                                                dangerouslySetInnerHTML={{ __html: result.interpretation.replace(/\n/g, '<br/>') }}
                                                className="text-sm text-gray-300 leading-relaxed font-light"
                                            />
                                        </div>
                                    </div>
                                </GlassCard>

                                <div className="grid md:grid-cols-2 gap-6">
                                    {/* Planets List */}
                                    <div className="space-y-3">
                                        <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                                            <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                                            Планеты
                                        </h3>
                                        {result.chart.planets.slice(0, 10).map((p, i) => (
                                            <div key={i} className="flex items-center justify-between bg-white/5 p-4 rounded-xl border border-white/5 hover:border-blue-500/30 transition-all group">
                                                <div className="flex items-center gap-4">
                                                    <div className="w-10 h-10 rounded-full bg-blue-900/30 flex items-center justify-center text-blue-400 font-bold group-hover:bg-blue-600 group-hover:text-white transition-colors">
                                                        {p.name[0]}
                                                    </div>
                                                    <div>
                                                        <p className="font-bold text-sm tracking-wide text-gray-200">{p.name}</p>
                                                        <p className="text-xs text-blue-300/80">{p.sign}</p>
                                                    </div>
                                                </div>
                                                <div className="text-right">
                                                    <p className="text-[10px] text-gray-500 uppercase tracking-wider">Дом</p>
                                                    <p className="text-sm font-bold text-white">{p.house.replace('_House', '')}</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>

                                    {/* Aspects List */}
                                    <div className="space-y-3">
                                        <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                                            <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
                                            Аспекты
                                        </h3>
                                        {result.chart.aspects.slice(0, 10).map((a, i) => (
                                            <div key={i} className="flex items-center justify-between bg-indigo-900/10 p-4 rounded-xl text-xs border border-indigo-500/10 hover:bg-indigo-900/20 transition-colors">
                                                <div className="flex items-center gap-2">
                                                    <span className="font-bold text-indigo-300 text-sm">{a.p1}</span>
                                                    <span className="text-gray-500 text-[10px] uppercase">{a.aspect}</span>
                                                    <span className="font-bold text-indigo-300 text-sm">{a.p2}</span>
                                                </div>
                                                <span className="text-gray-600 font-mono">{a.orb.toFixed(1)}°</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="h-full min-h-[400px] flex flex-col items-center justify-center text-gray-500 border-2 border-dashed border-white/5 rounded-2xl bg-white/5">
                                <Star className="w-16 h-16 mb-4 opacity-20 animate-pulse" />
                                <p className="text-sm tracking-widest uppercase">Заполните форму для расчета</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </PageTransition>
    );
};

export default Astrology;
