import React, { useState } from 'react';
import { GlassCard, MysticButton, PageTransition } from '../components/UI';
import AdBanner from '../components/AdBanner';
import { Moon, Sparkles, MessageSquare, CloudMoon } from 'lucide-react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const DreamInterpreter = () => {
    const [description, setDescription] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const interpretDream = async () => {
        if (!description.trim()) return setError('Опишите ваш сон');
        setLoading(true);
        setError('');
        try {
            const response = await axios.post(`${API_URL}/services/dream`, { description });
            setResult(response.data.interpretation);
        } catch (err) {
            setError('Ошибка толкования');
        } finally {
            setLoading(false);
        }
    };

    return (
        <PageTransition>
            <div className="mb-8">
                <h2 className="text-2xl font-bold mb-2 flex items-center gap-3" style={{ fontFamily: 'Cinzel' }}>
                    <CloudMoon className="text-purple-400 w-8 h-8" />
                    <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-200 to-pink-200">
                        Толкование Снов
                    </span>
                </h2>
                <p className="text-purple-200/60 text-sm font-light">
                    Погрузитесь в тайны подсознания. Опишите свой сон, и оракул раскроет его скрытый смысл.
                </p>
            </div>

            <GlassCard className="mb-8 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-b from-purple-900/10 to-transparent pointer-events-none" />
                <div className="space-y-4 relative z-10">
                    <div>
                        <label className="block text-[10px] text-purple-300/80 mb-2 uppercase tracking-widest font-bold">
                            Что вам приснилось?
                        </label>
                        <textarea
                            placeholder="Опишите сюжет сна, чувства и яркие детали. Например: Я летал над ночным городом..."
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            rows={5}
                            className="w-full bg-black/40 border border-purple-500/20 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-purple-500/60 focus:ring-1 focus:ring-purple-500/40 transition-all resize-none text-sm placeholder:text-purple-500/20"
                        />
                    </div>

                    {error && (
                        <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-3 text-red-300 text-xs">
                            {error}
                        </div>
                    )}

                    <MysticButton
                        onClick={interpretDream}
                        loading={loading}
                        className="w-full justify-center bg-gradient-to-r from-purple-900 to-indigo-900 hover:from-purple-800 hover:to-indigo-800 border-purple-500/30"
                    >
                        <div className="flex items-center gap-2">
                            <Moon className="w-4 h-4" />
                            <span>Раскрыть Тайну Сна</span>
                        </div>
                    </MysticButton>
                </div>
            </GlassCard>

            {result && (
                <div className="animate-fade-in pb-20 space-y-6">
                    <AdBanner variant="native" className="mb-6" />
                    <GlassCard className="border-purple-500/20 bg-purple-900/5 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-4 opacity-10">
                            <Sparkles className="w-12 h-12 text-purple-400" />
                        </div>
                        <div className="flex gap-3">
                            <MessageSquare className="w-5 h-5 text-purple-400 shrink-0 mt-1" />
                            <div>
                                <h4 className="font-bold text-sm mb-3">Послание из бездны сна:</h4>
                                <div
                                    dangerouslySetInnerHTML={{ __html: result.replace(/\n\g/, '<br/>') }}
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

export default DreamInterpreter;
