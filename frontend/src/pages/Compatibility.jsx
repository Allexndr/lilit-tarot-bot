import React, { useState } from 'react';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import AdBanner from '../components/AdBanner';
import { Heart, Users, MessageSquare, Infinity } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const Compatibility = () => {
    const [date1, setDate1] = useState('');
    const [date2, setDate2] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const checkCompatibility = async () => {
        if (!date1 || !date2) return setError('Введите обе даты рождения');
        setLoading(true);
        setError('');
        try {
            const response = await axios.post(`${API_URL}/services/compatibility`, { date1, date2 });
            setResult(response.data);
        } catch (err) {
            setError('Ошибка расчета совместимости');
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageTransition>
            <div className="mb-8">
                <h2 className="text-2xl font-bold mb-2 flex items-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                    <Infinity className="text-pink-400 w-8 h-8" />
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-pink-200 to-rose-200">
                        Матрица Любви
                    </span>
                </h2>
                <p className="text-pink-200/60 text-sm font-light">
                    Узнайте кармические задачи вашей пары и потенциал союза.
                </p>
            </div>

            <GlassCard className="mb-8 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-pink-900/10 to-transparent pointer-events-none" />

                <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="block text-[10px] text-pink-300/80 uppercase tracking-widest font-bold">Партнер 1</label>
                            <input
                                type="text"
                                placeholder="ДД.ММ.ГГГГ"
                                value={date1}
                                onChange={(e) => setDate1(e.target.value)}
                                className="w-full bg-black/40 border border-pink-500/20 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-pink-500/60 focus:ring-1 focus:ring-pink-500/40 transition-all text-center placeholder:text-pink-500/20"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="block text-[10px] text-pink-300/80 uppercase tracking-widest font-bold">Партнер 2</label>
                            <input
                                type="text"
                                placeholder="ДД.ММ.ГГГГ"
                                value={date2}
                                onChange={(e) => setDate2(e.target.value)}
                                className="w-full bg-black/40 border border-pink-500/20 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-pink-500/60 focus:ring-1 focus:ring-pink-500/40 transition-all text-center placeholder:text-pink-500/20"
                            />
                        </div>
                    </div>

                    <MysticButton
                        onClick={checkCompatibility}
                        loading={loading}
                        className="w-full justify-center bg-gradient-to-r from-pink-900 to-rose-900 hover:from-pink-800 hover:to-rose-800 border-pink-500/30"
                    >
                        <div className="flex items-center gap-2">
                            <Heart className="w-4 h-4" />
                            <span>Рассчитать Совместимость</span>
                        </div>
                    </MysticButton>
                </div>
                {error && <p className="text-red-400 text-xs mt-4 text-center bg-red-900/20 p-2 rounded-lg border border-red-500/20">{error}</p>}
            </GlassCard>

            {result && (
                <div className="space-y-6 animate-fade-in pb-20">
                    <AdBanner variant="native" className="mb-6" />
                    <div className="flex justify-center items-center gap-8 py-6">
                        <div className="flex flex-col items-center">
                            <div className="w-16 h-16 rounded-full border-2 border-pink-500/30 flex items-center justify-center text-2xl font-bold text-pink-400 shadow-lg shadow-pink-500/10">
                                {result.data.center}
                            </div>
                            <p className="text-[10px] text-gray-400 mt-2 uppercase">Душа пары</p>
                        </div>
                        <div className="w-px h-12 bg-gray-800"></div>
                        <div className="flex flex-col items-center">
                            <div className="w-16 h-16 rounded-full border-2 border-purple-500/30 flex items-center justify-center text-2xl font-bold text-purple-400 shadow-lg shadow-purple-500/10">
                                {result.data.purpose}
                            </div>
                            <p className="text-[10px] text-gray-400 mt-2 uppercase">Цель</p>
                        </div>
                    </div>

                    <GlassCard className="border-pink-500/20 bg-pink-900/5">
                        <div className="flex gap-3">
                            <MessageSquare className="w-5 h-5 text-pink-400 shrink-0 mt-1" />
                            <div>
                                <h4 className="font-bold text-sm mb-2">Вердикт Судьбы:</h4>
                                <div
                                    dangerouslySetInnerHTML={{ __html: result.interpretation.replace(/\n/g, '<br/>') }}
                                    className="text-xs text-gray-300 leading-relaxed italic"
                                />
                            </div>
                        </div>
                    </GlassCard>
                </div>
            )}
        </PageTransition>
    );
};

export default Compatibility;
