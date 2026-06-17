import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Trash2, Sparkles } from 'lucide-react';
import axios from 'axios';
import { GlassCard } from '../components/UI';

const ConsultantChat = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', text: '🔮 Приветствую! Я — Лилит, ваш консультант по Таро. Задавайте вопросы о картах, раскладах, мистике...' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const sendMessage = async () => {
        if (!input.trim() || loading) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', text: userMessage }]);
        setLoading(true);

        try {
            const response = await axios.post('/api/consultant/chat', {
                telegram_id: 123456, // TODO: Get from auth
                message: userMessage
            });

            setMessages(prev => [...prev, { role: 'assistant', text: response.data.response }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'assistant', text: '😔 Произошла ошибка. Попробуйте еще раз.' }]);
        } finally {
            setLoading(false);
        }
    };

    const clearHistory = async () => {
        try {
            await axios.delete('/api/consultant/history/123456');
            setMessages([{ role: 'assistant', text: '✅ История очищена. Начнем с начала!' }]);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="h-screen flex flex-col page-container pb-0 pt-4">
            {/* Header */}
            <div className="flex justify-between items-center mb-4 px-4">
                <div>
                    <h2 className="text-xl font-bold flex items-center gap-2">
                        <Sparkles className="text-yellow-400" size={20} />
                        Консультант 24/7
                    </h2>
                    <p className="text-xs text-gray-400">Лилит в сети</p>
                </div>
                <button onClick={clearHistory} className="p-2 rounded-full hover:bg-purple-900/30 transition">
                    <Trash2 size={20} className="text-gray-400" />
                </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 pb-4 space-y-3">
                <AnimatePresence>
                    {messages.map((msg, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] p-3 rounded-2xl ${msg.role === 'user'
                                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white'
                                        : 'glass-panel'
                                    }`}
                            >
                                <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {loading && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                        <div className="glass-panel p-3 rounded-2xl">
                            <div className="flex gap-1">
                                <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                                <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                                <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                            </div>
                        </div>
                    </motion.div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-800">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                        placeholder="Спросите о Таро..."
                        className="flex-1 bg-gray-900/50 text-white rounded-full px-4 py-3 outline-none focus:ring-2 focus:ring-purple-500 border border-gray-700"
                        disabled={loading}
                    />
                    <button
                        onClick={sendMessage}
                        disabled={loading || !input.trim()}
                        className="mystic-btn p-3 rounded-full disabled:opacity-50"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ConsultantChat;
