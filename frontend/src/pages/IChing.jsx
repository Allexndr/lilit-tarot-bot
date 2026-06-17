import React, { useState } from 'react';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import AdBanner from '../components/AdBanner';
import { Circle, MessageSquare, GripHorizontal, Coins } from 'lucide-react';
import { motion } from 'framer-motion';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const IChing = () => {
    const [question, setQuestion] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const [coinAnimation, setCoinAnimation] = useState(false);

    const performReading = async () => {
        setLoading(true);
        setError('');
        setCoinAnimation(true);

        try {
            // Delay to show animation
            await new Promise(resolve => setTimeout(resolve, 2000));
            const response = await axios.post(`${API_URL}/services/iching`, { question });
            setResult(response.data);
        } catch (err) {
            setError('Ошибка гадания');
        } finally {
            setLoading(false);
            setCoinAnimation(false);
        }
    };

    return (
        <PageTransition>
            <div className="mb-8">
                <h2 className="text-2xl font-bold mb-2 flex items-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                    <GripHorizontal className="text-orange-400 w-8 h-8" />
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-orange-200 to-amber-200">
                        И-Цзин: Книга Перемен
                    </span>
                </h2>
                <p className="text-orange-200/60 text-sm font-light">
                    Задайте вопрос и подбросьте монеты. Древняя мудрость укажет путь.
                </p>
            </div>

            <GlassCard className="mb-8 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-orange-900/10 to-transparent pointer-events-none" />

                {coinAnimation ? (
                    <div className="h-48 flex flex-col items-center justify-center gap-4">
                        <div className="flex gap-4">
                            {[1, 2, 3].map(i => (
                                <motion.div
                                    key={i}
                                    animate={{
                                        rotateY: [0, 720, 1440],
                                        y: [0, -50, 0]
                                    }}
                                    transition={{
                                        duration: 1.5,
                                        repeat: Infinity,
                                        ease: "easeInOut"
                                    }}
                                    className="w-12 h-12 rounded-full border-2 border-orange-400/50 bg-orange-500/10 flex items-center justify-center relative shadow-[0_0_15px_rgba(251,146,60,0.3)]"
                                >
                                    <div className="w-8 h-8 border border-orange-400/30 rounded-sm rotate-45"></div>
                                </motion.div>
                            ))}
                        </div>
                        <p className="text-orange-300 animate-pulse text-sm font-cinzel">Монеты падают...</p>
                    </div>
                ) : (
                    <div className="space-y-4">
                        <div>
                            <label className="block text-[10px] text-orange-300/80 mb-2 uppercase tracking-widest font-bold">О чем вы хотите знать?</label>
                            <input
                                type="text"
                                placeholder="Ваш вопрос Вселенной..."
                                value={question}
                                onChange={(e) => setQuestion(e.target.value)}
                                className="w-full bg-black/40 border border-orange-500/20 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-orange-500/60 focus:ring-1 focus:ring-orange-500/40 transition-all placeholder:text-orange-500/20"
                            />
                        </div>
                        <MysticButton
                            onClick={performReading}
                            loading={loading}
                            className="w-full justify-center bg-gradient-to-r from-orange-800 to-amber-900 hover:from-orange-700 hover:to-amber-800 border-orange-500/30"
                        >
                            <div className="flex items-center gap-2">
                                <Coins className="w-4 h-4" />
                                <span>Бросить монеты</span>
                            </div>
                        </MysticButton>
                    </div>
                )}
                {error && <p className="text-red-400 text-xs mt-2 text-center">{error}</p>}
            </GlassCard>

            {result && (
                <div className="space-y-6 animate-fade-in pb-20">
                    <AdBanner variant="native" className="mb-6" />
                    <div className="flex flex-col gap-1 items-center py-4">
                        {[...result.hexagram].reverse().map((line, i) => (
                            <div key={i} className="flex gap-2">
                                {line % 2 === 0 ? (
                                    <>
                                        <div className="w-12 h-2 bg-orange-500/80 rounded-sm"></div>
                                        <div className="w-12 h-2 bg-orange-500/80 rounded-sm"></div>
                                    </>
                                ) : (
                                    <div className="w-26 h-2 bg-orange-500 rounded-sm" style={{ width: '104px' }}></div>
                                )}
                            </div>
                        ))}
                    </div>

                    <GlassCard className="border-orange-500/20 bg-orange-900/5">
                        <div className="flex gap-3">
                            <MessageSquare className="w-5 h-5 text-orange-400 shrink-0 mt-1" />
                            <div>
                                <h4 className="font-bold text-sm mb-2">Мудрость Книги Перемен:</h4>
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

export default IChing;
