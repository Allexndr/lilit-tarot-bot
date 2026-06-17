import React, { useState } from 'react';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import AdBanner from '../components/AdBanner';
import { Sparkles, MessageSquare, Gem, Snowflake } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const RuneCasting = () => {
    const [spreadType, setSpreadType] = useState('single_rune');
    const [question, setQuestion] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const [isCasting, setIsCasting] = useState(false);

    const castRunes = async () => {
        setLoading(true);
        setError('');
        setIsCasting(true);

        try {
            // Fake casting delay
            await new Promise(resolve => setTimeout(resolve, 2000));
            const response = await axios.post(`${API_URL}/services/runes`, {
                spread_type: spreadType,
                question: question
            });
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка при броске рун');
        } finally {
            setLoading(false);
            setIsCasting(false);
        }
    };

    return (
        <PageTransition>
            <div className="mb-8">
                <h2 className="text-2xl font-bold mb-2 flex items-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                    <Snowflake className="text-blue-400 w-8 h-8" />
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-200 to-cyan-200">
                        Древние Руны
                    </span>
                </h2>
                <p className="text-blue-200/60 text-sm font-light">
                    Прикоснитесь к мудрости предков через священные символы Старшего Футарка.
                </p>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
                <button
                    onClick={() => setSpreadType('single_rune')}
                    className={`p-3 rounded-xl border transition-all ${spreadType === 'single_rune' ? 'bg-blue-500/20 border-blue-500 text-white' : 'bg-black/40 border-white/10 text-gray-400'}`}
                >
                    <p className="font-bold text-sm">Одна руна</p>
                    <p className="text-[10px]">Совет на момент</p>
                </button>
                <button
                    onClick={() => setSpreadType('norns')}
                    className={`p-3 rounded-xl border transition-all ${spreadType === 'norns' ? 'bg-blue-500/20 border-blue-500 text-white' : 'bg-black/40 border-white/10 text-gray-400'}`}
                >
                    <p className="font-bold text-sm">Три Норны</p>
                    <p className="text-[10px]">Прошлое-Наст-Будущее</p>
                </button>
            </div>

            <GlassCard className="mb-8 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-blue-900/10 to-transparent pointer-events-none" />

                {isCasting ? (
                    <div className="h-64 flex flex-col items-center justify-center relative overflow-hidden">
                        {[...Array(6)].map((_, i) => (
                            <motion.div
                                key={i}
                                initial={{ y: -50, opacity: 0, rotate: 0 }}
                                animate={{
                                    y: [0, 150 + Math.random() * 50],
                                    opacity: [0, 1, 0],
                                    rotate: Math.random() * 360
                                }}
                                transition={{
                                    duration: 1.5 + Math.random(),
                                    repeat: Infinity,
                                    ease: "linear",
                                    delay: Math.random() * 0.5
                                }}
                                className="absolute text-blue-300/30 text-2xl font-serif"
                                style={{ left: `${20 + Math.random() * 60}%` }}
                            >
                                ᚠ
                            </motion.div>
                        ))}
                        <div className="relative z-10 w-20 h-20 bg-blue-500/10 rounded-full border-2 border-blue-400/30 flex items-center justify-center animate-pulse shadow-[0_0_30px_rgba(59,130,246,0.2)]">
                            <Gem className="w-8 h-8 text-blue-300 animate-spin-slow" />
                        </div>
                        <p className="text-blue-300 animate-pulse text-sm font-cinzel mt-4">Руны шепчут...</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        <div>
                            <label className="block text-[10px] text-blue-300/80 mb-2 uppercase tracking-widest font-bold">
                                Ваш вопрос (необязательно)
                            </label>
                            <input
                                type="text"
                                placeholder="О чем спросить у рун?"
                                value={question}
                                onChange={(e) => setQuestion(e.target.value)}
                                className="w-full bg-black/40 border border-blue-500/20 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-blue-500/60 focus:ring-1 focus:ring-blue-500/40 transition-all placeholder:text-blue-500/20"
                            />
                        </div>
                        <MysticButton
                            onClick={castRunes}
                            loading={loading}
                            className="w-full justify-center bg-gradient-to-r from-blue-900 to-cyan-900 hover:from-blue-800 hover:to-cyan-800 border-blue-500/30"
                        >
                            <div className="flex items-center gap-2">
                                <Gem className="w-4 h-4" />
                                <span>Бросить Руны</span>
                            </div>
                        </MysticButton>
                    </div>
                )}
                {error && <p className="text-red-400 text-xs mt-2 text-center">{error}</p>}
            </GlassCard>

            {result && (
                <div className="space-y-6 animate-fade-in pb-20">
                    <AdBanner variant="native" className="mb-6" />
                    <div className="flex justify-center gap-6 py-4 flex-wrap">
                        {result.runes.map((rune, i) => (
                            <div key={i} className="flex flex-col items-center gap-2">
                                <p className="text-[10px] text-gray-500 uppercase">{result.spread.positions[i]}</p>
                                <div className={`w-16 h-20 bg-[#1a1a2e] border-2 border-blue-500/30 rounded-lg flex items-center justify-center text-4xl shadow-lg shadow-blue-500/10 ${rune.is_reversed ? 'rotate-180' : ''}`}>
                                    <span className="text-white drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]" style={{ fontFamily: 'Georgia' }}>
                                        {/* Simplified rune display using letters if no font, but let's assume it looks okay */}
                                        {rune.key.slice(0, 1).toUpperCase()}
                                    </span>
                                </div>
                                <p className="text-xs font-bold text-blue-300">{rune.name}</p>
                            </div>
                        ))}
                    </div>

                    <GlassCard className="border-blue-500/20 bg-blue-900/5">
                        <div className="flex gap-3">
                            <MessageSquare className="w-5 h-5 text-blue-400 shrink-0 mt-1" />
                            <div>
                                <h4 className="font-bold text-sm mb-2">Шепот Рун:</h4>
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

export default RuneCasting;
