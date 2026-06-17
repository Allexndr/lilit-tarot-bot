import React, { useState } from 'react';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import { Sparkles, Calendar, ArrowRight } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const MatrixDestiny = () => {
    const [birthDate, setBirthDate] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const calculateMatrix = async () => {
        if (!birthDate) return setError('Пожалуйста, введите дату рождения');

        // Basic format check DD.MM.YYYY
        if (!/^\d{2}\.\d{2}\.\d{4}$/.test(birthDate)) {
            return setError('Формат даты должен быть ДД.ММ.ГГГГ');
        }

        setLoading(true);
        setError('');
        try {
            const response = await axios.post(`${API_URL}/services/matrix`, {
                birth_date: birth_date
            });
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка при расчете');
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageTransition>
            <div className="max-w-4xl mx-auto">
                <div className="mb-8 text-center">
                    <h2 className="text-4xl font-bold mb-2 flex items-center justify-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                        <Sparkles className="text-yellow-400 w-8 h-8" />
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-yellow-200 via-yellow-400 to-yellow-200">
                            Матрица Судьбы
                        </span>
                    </h2>
                    <p className="text-purple-200/60 font-light">
                        Кармический паспорт вашей души.
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-8 items-start">
                    {/* Input Section - Left Column on Desktop */}
                    <div className="md:col-span-1">
                        <GlassCard className="sticky top-24">
                            <div className="space-y-6">
                                <div>
                                    <label className="block text-xs text-purple-300 mb-2 uppercase tracking-wider font-bold">Дата рождения</label>
                                    <div className="relative">
                                        <input
                                            type="text"
                                            placeholder="15.03.1994"
                                            value={birthDate}
                                            onChange={(e) => setBirthDate(e.target.value)}
                                            className="w-full bg-black/40 border border-purple-500/30 rounded-xl py-3 px-10 text-white focus:outline-none focus:border-purple-500 transition-all shadow-inner"
                                        />
                                        <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 text-purple-400 w-5 h-5" />
                                    </div>
                                </div>

                                {error && <div className="p-3 bg-red-900/20 border border-red-500/30 rounded-lg text-red-300 text-xs text-center">{error}</div>}

                                <MysticButton
                                    onClick={calculateMatrix}
                                    loading={loading}
                                    className="w-full justify-center shadow-lg shadow-purple-900/20"
                                >
                                    Рассчитать
                                </MysticButton>
                            </div>
                        </GlassCard>
                    </div>

                    {/* Results Section - Right Columns on Desktop */}
                    <div className="md:col-span-2">
                        {result ? (
                            <div className="space-y-6 animate-fade-in">
                                {/* Core Grid */}
                                <div className="grid grid-cols-2 gap-4">
                                    <GlassCard className="text-center relative overflow-hidden group">
                                        <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                                        <p className="text-[10px] text-purple-300 uppercase tracking-widest mb-2">Личность (A)</p>
                                        <p className="text-4xl font-black text-white font-cinzel">{result.data.main.A}</p>
                                    </GlassCard>
                                    <GlassCard className="text-center relative overflow-hidden group">
                                        <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                                        <p className="text-[10px] text-yellow-300 uppercase tracking-widest mb-2">Комфорт (E)</p>
                                        <p className="text-4xl font-black text-white font-cinzel">{result.data.main.E}</p>
                                    </GlassCard>
                                </div>

                                {/* Destiny Card */}
                                <GlassCard className="border-l-4 border-l-purple-500">
                                    <h4 className="font-bold text-white mb-4 flex items-center gap-2 font-cinzel">
                                        <ArrowRight className="w-4 h-4 text-purple-400" /> Предназначение
                                    </h4>
                                    <div className="grid grid-cols-3 gap-4 text-center">
                                        <div className="bg-white/5 p-3 rounded-lg">
                                            <span className="block text-[10px] text-gray-400 uppercase mb-1">Личное</span>
                                            <span className="text-lg font-bold text-purple-200">{result.data.destiny.personal}</span>
                                        </div>
                                        <div className="bg-white/5 p-3 rounded-lg">
                                            <span className="block text-[10px] text-gray-400 uppercase mb-1">Социум</span>
                                            <span className="text-lg font-bold text-blue-200">{result.data.destiny.social}</span>
                                        </div>
                                        <div className="bg-white/5 p-3 rounded-lg border border-purple-500/30">
                                            <span className="block text-[10px] text-gray-400 uppercase mb-1">Дух</span>
                                            <span className="text-lg font-bold text-white">{result.data.destiny.spiritual}</span>
                                        </div>
                                    </div>
                                </GlassCard>

                                {/* Channels */}
                                <GlassCard>
                                    <div className="grid grid-cols-2 gap-8 text-center divide-x divide-white/10">
                                        <div>
                                            <p className="text-xs text-green-300 uppercase tracking-widest mb-2">💰 Деньги</p>
                                            <p className="text-3xl font-bold text-white">{result.data.channels.money}</p>
                                        </div>
                                        <div>
                                            <p className="text-xs text-pink-300 uppercase tracking-widest mb-2">❤️ Любовь</p>
                                            <p className="text-3xl font-bold text-white">{result.data.channels.love}</p>
                                        </div>
                                    </div>
                                </GlassCard>

                                {/* Interpretation Text */}
                                <div className="prose prose-invert max-w-none">
                                    <div
                                        dangerouslySetInnerHTML={{ __html: result.interpretation.replace(/\n/g, '<br/>') }}
                                        className="bg-black/40 backdrop-blur-sm p-6 rounded-2xl text-sm leading-7 text-gray-300 border border-white/5 shadow-inner"
                                    />
                                </div>
                            </div>
                        ) : (
                            <div className="h-64 flex flex-col items-center justify-center text-gray-500 border-2 border-dashed border-white/5 rounded-2xl bg-white/5">
                                <Sparkles className="w-12 h-12 mb-4 opacity-20" />
                                <p>Введите дату рождения для расчета</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </PageTransition>
    );
};

export default MatrixDestiny;
