import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import TarotCard from '../components/TarotCard';
import { Sparkles, MessageSquare } from 'lucide-react';
import AdBanner from '../components/AdBanner';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const TarotReading = () => {
    const { spreadType } = useParams();
    const [question, setQuestion] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [revealedCards, setRevealedCards] = useState([]); // Track which cards are flipped

    const performReading = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.post(`${API_URL}/services/tarot/reading`, {
                spread_type: spreadType || 'three_cards',
                question: question
            });
            setResult(response.data);
            // Start reveal animation sequence
            setRevealedCards([]);
            // Reveal cards one by one with delay
            response.data.cards.forEach((_, index) => {
                setTimeout(() => {
                    setRevealedCards(prev => [...prev, index]);
                }, 500 + (index * 800)); // First delay + stagger
            });
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка при гадании');
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageTransition>
            <div className="max-w-6xl mx-auto">
                <div className="text-center mb-8">
                    <div className="inline-block px-3 py-1 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-300 text-[10px] font-bold tracking-widest uppercase mb-2">
                        {spreadType === 'daily_card' ? 'Карта Дня' : 'Таро Расклад'}
                    </div>
                    <h2 className="text-3xl font-bold mb-2 flex items-center justify-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-200 to-white">
                            {result ? result.spread.name : 'Спросите у Таро'}
                        </span>
                    </h2>
                    <p className="text-gray-400 text-sm font-light max-w-lg mx-auto">
                        Сосредоточьтесь на своем вопросе. Карты покажут путь, но выбор всегда за вами.
                    </p>
                </div>

                {!result ? (
                    <div className="max-w-xl mx-auto">
                        <GlassCard className="p-8 backdrop-blur-xl border-purple-500/20">
                            <div className="space-y-6">
                                <div>
                                    <label className="block text-xs text-purple-300 mb-2 uppercase tracking-widest font-bold">Ваш вопрос</label>
                                    <input
                                        type="text"
                                        placeholder="О чем вы хотите знать?"
                                        value={question}
                                        onChange={(e) => setQuestion(e.target.value)}
                                        className="w-full bg-black/40 border border-purple-500/30 rounded-xl py-4 px-6 text-white focus:outline-none focus:border-purple-500 transition-all shadow-inner placeholder:text-gray-600"
                                    />
                                </div>
                                <MysticButton
                                    onClick={performReading}
                                    loading={loading}
                                    className="w-full justify-center py-4 bg-gradient-to-r from-purple-900 to-indigo-900 hover:from-purple-800 hover:to-indigo-800 border-purple-500/30 shadow-lg shadow-purple-900/30"
                                >
                                    <div className="flex items-center gap-2">
                                        <Sparkles className="w-5 h-5" />
                                        <span className="tracking-widest font-bold">НАЧАТЬ ГАДАНИЕ</span>
                                    </div>
                                </MysticButton>
                            </div>
                        </GlassCard>
                    </div>
                ) : (
                    <div className="animate-fade-in space-y-12">
                        {/* Cards Section */}
                        <div className="flex flex-wrap justify-center gap-8 py-8 min-h-[400px]">
                            {result.cards.map((card, i) => (
                                <div key={i} className="flex flex-col items-center gap-4 group">
                                    <div className="relative">
                                        <p className="absolute -top-8 left-1/2 -translate-x-1/2 text-[10px] text-gray-400 uppercase tracking-widest font-medium whitespace-nowrap opacity-60 group-hover:opacity-100 transition-opacity">
                                            {result.spread.positions[i]}
                                        </p>
                                        <TarotCard
                                            card={card}
                                            isReversed={card.is_reversed}
                                            index={i}
                                            isRevealed={revealedCards.includes(i)}
                                            onReveal={() => {
                                                if (!revealedCards.includes(i)) {
                                                    setRevealedCards(prev => [...prev, i]);
                                                }
                                            }}
                                        />
                                    </div>
                                    <p className={`text-sm font-bold text-white font-cinzel max-w-[150px] text-center transition-all duration-700 ${revealedCards.includes(i) ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
                                        {card.name}
                                    </p>
                                </div>
                            ))}
                        </div>

                        {/* Interpretation Section */}
                        <div className="grid md:grid-cols-12 gap-8 items-start">
                            <div className="md:col-span-8 md:col-start-3">
                                <AdBanner variant="native" className="mb-8" />

                                <GlassCard className="relative overflow-hidden border-purple-500/20 bg-[#1a103c]/40">
                                    <div className="absolute top-0 right-0 p-6 opacity-5">
                                        <MessageSquare className="w-24 h-24 text-white" />
                                    </div>

                                    <div className="relative z-10 px-4 md:px-8 py-4">
                                        <h3 className="text-2xl font-bold font-cinzel mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-200 to-white border-b border-white/5 pb-4">
                                            Толкование Расклада
                                        </h3>
                                        <div
                                            dangerouslySetInnerHTML={{ __html: result.interpretation.replace(/\n/g, '<br/>') }}
                                            className="text-base text-gray-300 leading-8 font-light tracking-wide space-y-4"
                                            style={{ fontFamily: 'Inter' }}
                                        />
                                    </div>
                                </GlassCard>

                                <div className="mt-8 text-center">
                                    <button
                                        onClick={() => { setResult(null); setRevealedCards([]); }}
                                        className="text-gray-500 hover:text-white transition-colors text-sm uppercase tracking-widest border-b border-transparent hover:border-white pb-1"
                                    >
                                        Сделать новый расклад
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </PageTransition>
    );
};

export default TarotReading;
