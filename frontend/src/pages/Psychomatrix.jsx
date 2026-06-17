import React, { useState } from 'react';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import { Calendar, Hash } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const Psychomatrix = () => {
    const [birthDate, setBirthDate] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const calculate = async () => {
        if (!birthDate) return setError('Введите дату рождения');
        setLoading(true);
        setError('');
        try {
            const response = await axios.post(`${API_URL}/services/psychomatrix`, { birth_date: birthDate });
            setResult(response.data);
        } catch (err) {
            setError('Ошибка расчета');
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageTransition>
            <div className="max-w-4xl mx-auto">
                <div className="mb-8 text-center">
                    <h2 className="text-4xl font-bold mb-2 flex items-center justify-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                        <Hash className="text-green-400 w-8 h-8" />
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-green-200 via-green-100 to-white">
                            Психоматрица
                        </span>
                    </h2>
                    <p className="text-green-200/60 text-sm font-light">
                        Квадрат Пифагора — код вашей личности.
                    </p>
                </div>

                <div className="grid md:grid-cols-3 gap-8 items-start">
                    {/* Input Column */}
                    <div className="md:col-span-1">
                        <GlassCard className="sticky top-24 border-green-500/20">
                            <h3 className="text-lg font-bold text-white mb-4 border-b border-white/5 pb-2">Расчет</h3>
                            <div className="space-y-4">
                                <div className="relative">
                                    <input
                                        type="text"
                                        placeholder="15.03.1994"
                                        value={birthDate}
                                        onChange={(e) => setBirthDate(e.target.value)}
                                        className="w-full bg-black/40 border border-green-500/20 rounded-xl py-3 px-10 text-white focus:outline-none focus:border-green-500 transition-colors shadow-inner"
                                    />
                                    <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 text-green-400 w-5 h-5" />
                                </div>

                                {error && <div className="p-2 bg-red-900/20 border border-red-500/30 rounded-lg text-red-300 text-xs text-center">{error}</div>}

                                <MysticButton onClick={calculate} loading={loading} className="w-full justify-center bg-green-600 hover:bg-green-500 shadow-lg shadow-green-900/20">
                                    Рассчитать
                                </MysticButton>
                            </div>
                        </GlassCard>
                    </div>

                    {/* Results Column */}
                    <div className="md:col-span-2">
                        {result ? (
                            <div className="space-y-6 animate-fade-in">
                                <div className="grid md:grid-cols-2 gap-6">
                                    {/* Matrix Grid */}
                                    <div className="aspect-square max-w-[300px] mx-auto bg-black/20 border border-green-500/20 rounded-2xl overflow-hidden shadow-[0_0_30px_rgba(34,197,94,0.1)]">
                                        <div className="grid grid-cols-3 h-full">
                                            {['1', '4', '7', '2', '5', '8', '3', '6', '9'].map((key) => (
                                                <div key={key} className="border border-green-500/10 flex flex-col items-center justify-center hover:bg-green-500/5 transition-colors group relative">
                                                    <span className="absolute top-2 left-2 text-[8px] text-gray-600 group-hover:text-green-400/50">{key}</span>
                                                    <span className={`text-2xl font-bold ${result.data.matrix[key] === 0 ? 'text-gray-700' : 'text-green-400'} font-mono`}>
                                                        {result.data.matrix[key] === 0 ? '—' : '1'.repeat(result.data.matrix[key])}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Key Numbers */}
                                    <GlassCard className="border-green-500/20 flex flex-col justify-center">
                                        <h4 className="font-bold text-green-300 mb-4 text-center uppercase tracking-widest text-xs">Ваши Числа</h4>
                                        <div className="grid grid-cols-2 gap-2 text-center">
                                            {result.data.numbers.map((n, i) => (
                                                <div key={i} className="bg-white/5 rounded-lg p-2 border border-white/5">
                                                    <span className="text-xl font-mono text-white font-bold">{n}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </GlassCard>
                                </div>

                                {/* Interpretation */}
                                <GlassCard className="border-green-500/20 bg-gradient-to-br from-[#052e16] to-black/80">
                                    <div className="prose prose-sm prose-invert max-w-none">
                                        <div
                                            dangerouslySetInnerHTML={{ __html: result.interpretation.replace(/\n/g, '<br/>') }}
                                            className="text-gray-300 leading-relaxed font-light pl-4 border-l-2 border-green-500/30"
                                        />
                                    </div>
                                </GlassCard>
                            </div>
                        ) : (
                            <div className="h-64 flex flex-col items-center justify-center text-gray-500 border-2 border-dashed border-white/5 rounded-2xl bg-white/5">
                                <Hash className="w-16 h-16 mb-4 opacity-20" />
                                <p className="text-sm tracking-widest uppercase">Введите дату рождения</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </PageTransition>
    );
};

export default Psychomatrix;
